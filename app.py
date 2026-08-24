import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).parent
VENDOR_FILE = BASE_DIR / "sample-data" / "fictional-vendor.json"
CONTROL_FILE = BASE_DIR / "controls" / "control-library.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "sample-assessment.md"


def load_vendor():
    with VENDOR_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def load_controls():
    with CONTROL_FILE.open(encoding="utf-8") as file:
        return {
            row["control_id"]: row
            for row in csv.DictReader(file)
        }


def determine_inherent_risk(vendor):
    data = vendor["data_access"]
    criticality = vendor["business_criticality"]

    if criticality == "High" and (
        data["personal_information"]
        or data["confidential_business_data"]
    ):
        return "High"

    if any(data.values()):
        return "Moderate"

    return "Low"


def create_finding(title, control, status, condition, risk, recommendation):
    return {
        "title": title,
        "control": control,
        "severity": control["severity"],
        "status": status,
        "condition": condition,
        "risk": risk,
        "recommendation": recommendation,
        "human_review": control["severity"] == "High",
    }


def assess_vendor(vendor, controls):
    responses = vendor["security_responses"]
    commitments = vendor["vendor_commitments"]
    findings = []

    if not responses["penetration_testing"]:
        findings.append(
            create_finding(
                "Lack of Independent Penetration Testing",
                controls["VM-01"],
                "Planned",
                (
                    "The vendor has not completed an independent "
                    "penetration test. The vendor plans to complete one "
                    f"{commitments['penetration_test'].lower()}."
                ),
                (
                    "Because the vendor has not completed an independent "
                    "penetration test, exploitable weaknesses may remain "
                    "unidentified, potentially resulting in unauthorized "
                    "access, data exposure, or service disruption."
                ),
                (
                    "Complete an independent penetration test and provide "
                    "the executive summary, scope, testing dates, material "
                    "findings, and remediation evidence."
                ),
            )
        )

    if not responses["edr_deployed"]:
        findings.append(
            create_finding(
                "Endpoint Detection and Response Not Deployed",
                controls["EP-01"],
                "Planned",
                (
                    "EDR is not currently deployed. The vendor plans "
                    f"implementation {commitments['edr_implementation'].lower()}."
                ),
                (
                    "Because EDR is not deployed, malicious endpoint "
                    "activity may not be detected or contained promptly, "
                    "potentially resulting in system compromise or data loss."
                ),
                (
                    "Deploy EDR across applicable endpoints and provide "
                    "configuration evidence and an endpoint coverage report."
                ),
            )
        )

    if responses["log_retention_days"] < 180:
        findings.append(
            create_finding(
                "Insufficient Security Log Retention",
                controls["LOG-01"],
                "Partially implemented",
                (
                    f"Security logs are retained for "
                    f"{responses['log_retention_days']} days instead of "
                    "the required 180 days."
                ),
                (
                    "Because security logs are not retained for the required "
                    "period, the vendor may be unable to investigate incidents "
                    "or reconstruct malicious activity."
                ),
                (
                    "Increase log retention to at least 180 days and provide "
                    "the logging policy or platform configuration as evidence."
                ),
            )
        )

    if responses["subprocessor_management"] != "Implemented":
        findings.append(
            create_finding(
                "Partial Subprocessor Risk Management",
                controls["TPRM-02"],
                "Partially implemented",
                (
                    "The vendor reported that its subprocessor-management "
                    "process is only partially implemented."
                ),
                (
                    "Because subprocessors are not fully assessed, security "
                    "weaknesses at a fourth party could expose organizational "
                    "data or disrupt the service."
                ),
                (
                    "Maintain a subprocessor inventory, perform documented "
                    "security reviews, and provide notification of material "
                    "subprocessor changes."
                ),
            )
        )

    return findings


def render_report(vendor, inherent_risk, findings):
    lines = [
        "# Sample Third-Party Risk Assessment",
        "",
        "## Executive Summary",
        "",
        (
            f"{vendor['vendor_name']} provides a {vendor['service']}. "
            f"The preliminary inherent-risk rating is **{inherent_risk}**."
        ),
        "",
        (
            f"The assessment identified **{len(findings)} control gaps**. "
            "Final vendor approval and risk acceptance require human review."
        ),
        "",
        "## Vendor Overview",
        "",
        f"- Vendor: {vendor['vendor_name']}",
        f"- Service: {vendor['service']}",
        f"- Deployment model: {vendor['deployment_model']}",
        f"- Business criticality: {vendor['business_criticality']}",
        f"- Inherent risk: {inherent_risk}",
        "",
        "## Findings",
        "",
    ]

    for number, finding in enumerate(findings, start=1):
        lines.extend(
            [
                f"### {number}. {finding['title']}",
                "",
                f"- Control: {finding['control']['control_id']}",
                f"- Domain: {finding['control']['domain']}",
                f"- Severity: {finding['severity']}",
                f"- Status: {finding['status']}",
                "",
                "#### Condition",
                "",
                finding["condition"],
                "",
                "#### Risk Statement",
                "",
                finding["risk"],
                "",
                "#### Recommendation",
                "",
                finding["recommendation"],
                "",
                "#### Human Review",
                "",
                (
                    "Required"
                    if finding["human_review"]
                    else "Review during normal assessment approval"
                ),
                "",
            ]
        )

    lines.extend(
        [
            "## Preliminary Residual Risk",
            "",
            "**High** until the high-risk findings are remediated and validated.",
            "",
            "## Limitations",
            "",
            "- This assessment uses fictional data.",
            "- Findings require validation by a qualified security professional.",
            "- Planned remediation is not treated as an implemented control.",
            "- This output does not constitute final vendor approval.",
        ]
    )

    return "\n".join(lines)


def main():
    vendor = load_vendor()
    controls = load_controls()
    inherent_risk = determine_inherent_risk(vendor)
    findings = assess_vendor(vendor, controls)
    report = render_report(vendor, inherent_risk, findings)

    OUTPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")

    print(f"Assessment completed: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
