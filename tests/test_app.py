import unittest

from app import (
    assess_vendor,
    determine_inherent_risk,
    load_controls,
    load_vendor,
)


class VendorAssessmentTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vendor = load_vendor()
        cls.controls = load_controls()
        cls.findings = assess_vendor(cls.vendor, cls.controls)

    def test_high_inherent_risk(self):
        self.assertEqual(
            determine_inherent_risk(self.vendor),
            "High",
        )

    def test_four_control_gaps_identified(self):
        self.assertEqual(len(self.findings), 4)

    def test_penetration_test_is_planned_not_implemented(self):
        penetration_test = next(
            finding
            for finding in self.findings
            if finding["control"]["control_id"] == "VM-01"
        )

        self.assertEqual(penetration_test["status"], "Planned")
        self.assertTrue(penetration_test["human_review"])

    def test_edr_gap_requires_human_review(self):
        edr_finding = next(
            finding
            for finding in self.findings
            if finding["control"]["control_id"] == "EP-01"
        )

        self.assertTrue(edr_finding["human_review"])

    def test_log_retention_gap_is_identified(self):
        log_finding = next(
            finding
            for finding in self.findings
            if finding["control"]["control_id"] == "LOG-01"
        )

        self.assertEqual(
            log_finding["status"],
            "Partially implemented",
        )

    def test_findings_reference_defined_controls(self):
        valid_control_ids = set(self.controls)

        for finding in self.findings:
            self.assertIn(
                finding["control"]["control_id"],
                valid_control_ids,
            )


if __name__ == "__main__":
    unittest.main()