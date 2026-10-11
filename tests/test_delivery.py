import json
import unittest

import test_termix
from bnb_rotation.delivery import (approve_report, prepare_delivery, review_copy,
                                   sha256, validate_delivery_intent)


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.fixture = test_termix.TermixTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.temporary.cleanup)
        self.fixture.draft()
        self.reader = self.fixture.reader
        self.root = self.fixture.queue
        self.now = self.fixture.fixture.now
        self.job = self.root / "TEST-001"

    def review(self):
        return review_copy(self.reader, self.root, "TEST-001", self.now)

    def approve(self):
        review = self.review()
        return approve_report(self.reader, self.root, "TEST-001", review["report_sha256"],
                              "Fixture operator", "Fixture content review; not real approval", self.now)

    def plan(self):
        return prepare_delivery(self.reader, self.root, "TEST-001", self.now)

    def test_approval_required_and_does_not_infer_delivery(self):
        self.review()
        with self.assertRaises(FileNotFoundError):
            self.plan()
        self.assertFalse((self.job / "delivery-plan.json").exists())
        self.approve()
        result = self.plan()
        self.assertEqual(result["status"], "READY_FOR_OPERATOR_DELIVERY")
        self.assertFalse(result["delivery_submitted"])
        plan = json.loads((self.job / "delivery-plan.json").read_text())
        self.assertFalse(plan["uploaded"])
        self.assertFalse(plan["transaction_prepared"])
        self.assertFalse(plan["signed"])
        self.assertEqual(plan["steps"][0]["body"]["sizeBytes"], len((self.job / "review/report.md").read_bytes()))
        self.assertEqual(plan["steps"][-1]["required_indexed_status"], "DELIVERED")

    def test_review_copy_preserves_operator_edits_and_source(self):
        self.review()
        path = self.job / "review/report.md"
        path.write_text("Operator's revised report with scope and data limitations.")
        review = self.review()
        self.assertEqual(review["report_sha256"], sha256(path.read_bytes()))
        self.assertIn("revised report", path.read_text())
        self.assertIn("research draft", (self.job / "report.md").read_text())

    def test_hash_and_nonempty_review_identity_required(self):
        self.review()
        for checksum, reviewer, note in (("a" * 64, "Operator", "Reviewed"),
                                         ("invalid", "Operator", "Reviewed"),
                                         (self.review()["report_sha256"], "", "Reviewed")):
            with self.assertRaises(ValueError):
                approve_report(self.reader, self.root, "TEST-001", checksum, reviewer, note, self.now)
        self.assertFalse((self.job / "approval.json").exists())

    def test_post_approval_edit_invalidates_plan_and_reapproval_clears_old_plan(self):
        self.approve()
        self.plan()
        path = self.job / "review/report.md"
        path.write_text(path.read_text() + "\nOperator update\n")
        with self.assertRaisesRegex(ValueError, "approved report changed"):
            self.plan()
        self.assertFalse((self.job / "delivery-plan.json").exists())
        self.approve()
        self.assertFalse((self.job / "delivery-plan.json").exists())
        self.assertEqual(self.plan()["status"], "READY_FOR_OPERATOR_DELIVERY")

    def test_expired_or_cancelled_order_blocks_after_approval(self):
        self.approve()
        self.reader.order["deliveryDueAt"] = "1970-01-01T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "DELIVERY_EXPIRED"):
            self.plan()
        self.reader.order["status"] = "CANCELLED"
        with self.assertRaisesRegex(ValueError, "NOT_READY"):
            self.plan()

    def test_changed_terms_redo_or_membership_block_handoff(self):
        self.approve()
        self.reader.order["redoUsed"] = True
        with self.assertRaisesRegex(ValueError, "order changed"):
            self.plan()
        self.reader.order["redoUsed"] = False
        self.reader.member = False
        with self.assertRaisesRegex(ValueError, "authenticated provider"):
            self.plan()

    def test_original_or_manifest_tampering_invalidates_approval(self):
        self.approve()
        path = self.job / "report.md"
        original = path.read_bytes()
        path.write_text("tampered")
        with self.assertRaisesRegex(ValueError, "draft artifact changed"):
            self.plan()
        path.write_bytes(original)
        manifest_path = self.job / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["job_sha256"] = "altered"
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "does not bind"):
            self.plan()

    def test_report_symlink_blocked(self):
        self.review()
        path = self.job / "review/report.md"
        path.unlink()
        path.symlink_to(self.job / "report.md")
        with self.assertRaisesRegex(ValueError, "must be local"):
            self.approve()

    def test_intent_envelope_requires_expected_chain_contract_action_and_no_value(self):
        address = "0x" + "12" * 20
        plan = {"escrow_contract": address, "status": "READY_FOR_OPERATOR_DELIVERY", "chain_id": 56}
        intent = {"action": "submitDelivery", "chainId": 56, "contract": address,
                  "value": "0", "callData": "0x12345678"}
        self.assertEqual(validate_delivery_intent(plan, intent)["status"],
                         "REQUIRES_WALLET_SIMULATION_AND_SIGNATURE")
        for key, value in (("chainId", 8453), ("chainId", True), ("contract", "0x5678"),
                           ("action", "releaseEscrow"), ("value", "1"),
                           ("callData", "0x123"), ("callData", "0xinvalid")):
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                validate_delivery_intent(plan, dict(intent, **{key: value}))


if __name__ == "__main__":
    unittest.main()
