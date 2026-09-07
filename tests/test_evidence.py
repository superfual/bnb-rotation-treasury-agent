import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EvidenceTests(unittest.TestCase):
    def test_public_summaries_share_snapshot_identity(self):
        live = json.loads((ROOT / "evidence/live_summary.json").read_text())
        replay = json.loads((ROOT / "evidence/replay_summary.json").read_text())
        self.assertEqual(live["mode"], "READ_ONLY")
        self.assertEqual(live["raw_snapshot_sha256"], replay["snapshot_sha256"])

    def test_failed_split_gate_blocks_live_claim(self):
        replay = json.loads((ROOT / "evidence/replay_summary.json").read_text())
        gate = replay["experiment_viability"]
        self.assertEqual(gate["status"], "FAILED_NOT_LIVE_READY")
        self.assertTrue(gate["blockers"])


if __name__ == "__main__":
    unittest.main()
