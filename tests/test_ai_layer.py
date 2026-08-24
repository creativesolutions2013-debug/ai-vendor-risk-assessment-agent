import unittest

from ai_layer import (
    MockAssessmentProvider,
    build_assessment_prompt,
)
from app import (
    assess_vendor,
    determine_inherent_risk,
    load_controls,
    load_vendor,
)


class AIAssessmentLayerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vendor = load_vendor()
        cls.controls = load_controls()
        cls.inherent_risk = determine_inherent_risk(cls.vendor)
        cls.findings = assess_vendor(
            cls.vendor,
            cls.controls,
        )

        cls.prompt = build_assessment_prompt(
            cls.vendor,
            cls.controls,
            cls.findings,
            cls.inherent_risk,
        )

    def test_prompt_contains_required_sections(self):
        required_sections = [
            "SYSTEM INSTRUCTIONS",
            "ASSESSMENT INSTRUCTIONS",
            "VENDOR PROFILE",
            "CONTROL LIBRARY",
            "RULES-BASED BASELINE",
            "FINAL SAFETY REQUIREMENTS",
        ]

        for section in required_sections:
            self.assertIn(section, self.prompt)

    def test_prompt_contains_human_review_requirement(self):
        self.assertIn(
            "Do not accept risk",
            self.prompt,
        )

    def test_prompt_contains_vendor_and_control_data(self):
        self.assertIn("NorthStar Analytics", self.prompt)
        self.assertIn("VM-01", self.prompt)
        self.assertIn("EP-01", self.prompt)

    def test_mock_provider_rejects_incomplete_prompt(self):
        provider = MockAssessmentProvider()

        with self.assertRaises(ValueError):
            provider.generate("Incomplete assessment prompt")

    def test_mock_output_is_clearly_labeled(self):
        provider = MockAssessmentProvider()
        response = provider.generate(self.prompt)

        self.assertIn("Simulation notice", response)
        self.assertIn(
            "No external AI service was used",
            response,
        )

    def test_mock_output_requires_human_review(self):
        provider = MockAssessmentProvider()
        response = provider.generate(self.prompt)

        self.assertIn("Human Review Requirements", response)
        self.assertIn(
            "final vendor-approval and risk-acceptance decisions",
            response,
        )


if __name__ == "__main__":
    unittest.main()