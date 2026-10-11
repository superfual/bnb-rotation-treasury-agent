import copy
import json
import tempfile
import unittest
from pathlib import Path

import test_service
from unittest.mock import patch
from bnb_rotation.termix import LISTING_ID, TermixReader, queue_draft, readiness


class Reader:
    def __init__(self):
        self.order = {"id": "TEST-001", "listingId": LISTING_ID,
                      "chainOrderId": "0xfixture", "escrowContract": "0xfixture",
                      "status": "IN_PROGRESS", "budget": "2", "currency": "USDC",
                      "deliveryDueAt": "2099-01-01T00:00:00Z", "redoUsed": False,
                      "availableActions": {"canSubmitDelivery": True}}
        self.member = True
        self.calls = 0
        self.change = False

    def orders(self):
        return [{"id": self.order["id"]}] if self.member else []

    def detail(self, identifier):
        self.calls += 1
        result = copy.deepcopy(self.order)
        if self.change and self.calls > 1:
            result["budget"] = "3"
        return result


class TermixTests(unittest.TestCase):
    def setUp(self):
        fixture = test_service.ServiceTests()
        fixture.setUp()
        self.fixture = fixture
        self.reader = Reader()
        self.intake = {"order_id": "TEST-001", "scope_reviewed": True, "request": fixture.request}
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.queue = Path(self.temporary.name)

    def draft(self):
        f = self.fixture
        return queue_draft(self.reader, self.intake, f.snapshot, f.config, self.queue, f.now)

    def test_real_report_queued_once_and_hashes_verified(self):
        self.assertEqual(self.draft()["status"], "DRAFT_REQUIRES_OPERATOR_REVIEW")
        self.assertEqual(self.draft()["status"], "ALREADY_QUEUED")
        manifest = json.loads((self.queue / "TEST-001/manifest.json").read_text())
        self.assertFalse(manifest["delivery_submitted"])
        (self.queue / "TEST-001/report.md").write_text("tampered")
        with self.assertRaisesRegex(ValueError, "artifact changed"):
            self.draft()

    def test_changed_intake_or_redo_requires_review(self):
        self.draft()
        original = self.intake["request"]["question"]
        self.intake["request"]["question"] = "New scope"
        with self.assertRaisesRegex(ValueError, "changed order, intake or config"):
            self.draft()
        self.intake["request"]["question"] = original
        self.reader.order["redoUsed"] = True
        with self.assertRaises(ValueError):
            self.draft()

    def test_unowned_or_other_listing_cannot_queue(self):
        self.reader.member = False
        with self.assertRaisesRegex(ValueError, "authenticated provider"):
            self.draft()
        self.reader.member = True
        self.reader.order["listingId"] = "other"
        with self.assertRaisesRegex(ValueError, "listing mismatch"):
            self.draft()
        self.assertEqual(list(self.queue.iterdir()), [])

    def test_pending_acceptance_and_no_permission_block(self):
        self.reader.order["status"] = "PENDING_ACCEPT"
        with self.assertRaisesRegex(ValueError, "NEEDS_WALLET_ACCEPTANCE"):
            self.draft()
        self.reader.order["status"] = "FUNDED"
        self.reader.order["availableActions"] = None
        with self.assertRaisesRegex(ValueError, "DELIVERY_NOT_AUTHORIZED"):
            self.draft()

    def test_expiry_and_unknown_deadline_fail_closed(self):
        for due, expected in (("1970-01-01T00:00:00Z", "DELIVERY_EXPIRED"),
                              (None, "MISSING_OR_INVALID_DEADLINE"),
                              ("2099-01-01", "MISSING_OR_INVALID_DEADLINE")):
            self.reader.order["deliveryDueAt"] = due
            self.assertEqual(readiness(self.reader.order, self.fixture.now), expected)

    def test_recheck_detects_change_before_persisting(self):
        self.reader.change = True
        with self.assertRaisesRegex(ValueError, "changed during analysis"):
            self.draft()
        self.assertEqual(list(self.queue.iterdir()), [])

    def test_structured_review_and_id_binding_required(self):
        self.intake["scope_reviewed"] = False
        with self.assertRaises(ValueError):
            self.draft()
        self.intake["scope_reviewed"] = True
        self.intake["request"]["request_id"] = "other"
        with self.assertRaisesRegex(ValueError, "match the real order"):
            self.draft()
        self.intake["order_id"] = "../../escape"
        with self.assertRaisesRegex(ValueError, "invalid order ID"):
            self.draft()

    def test_lock_and_failed_data_leave_no_success_artifacts(self):
        lock = self.queue / "TEST-001.lock"
        lock.mkdir()
        with self.assertRaisesRegex(ValueError, "already being processed"):
            self.draft()
        lock.rmdir()
        self.fixture.snapshot["decision_time_utc_ms"] -= 900_001
        with self.assertRaises(ValueError):
            self.draft()
        self.assertEqual(list(self.queue.iterdir()), [])

    def test_reader_paginates_with_agent_and_listing_scope(self):
        reader = object.__new__(TermixReader)
        with patch.object(reader, "get", side_effect=[
                {"items": [{"id": "one"}], "totalPages": 2},
                {"items": [{"id": "two"}], "totalPages": 2}]) as get:
            self.assertEqual(len(reader.orders()), 2)
            paths = [call.args[0] for call in get.call_args_list]
            self.assertTrue(all("providerAgentId=" in p and "listingId=" + LISTING_ID in p for p in paths))
            self.assertIn("page=2", paths[1])

    def test_malformed_list_and_missing_chain_identity_block(self):
        reader = object.__new__(TermixReader)
        with patch.object(reader, "get", return_value={"items": [], "totalPages": "2"}):
            with self.assertRaisesRegex(ValueError, "schema"):
                reader.orders()
        self.reader.order.pop("chainOrderId")
        with self.assertRaisesRegex(ValueError, "on-chain order identity"):
            self.draft()


if __name__ == "__main__":
    unittest.main()
