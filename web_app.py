import json

import streamlit as st

from ai_layer import MockAssessmentProvider, build_assessment_prompt
from app import (
    assess_vendor,
    determine_inherent_risk,
    load_controls,
    render_report,
)


st.set_page_config(
    page_title="AI Vendor Risk Assessment",
    page_icon="🛡️",
    layout="wide",
)


def build_vendor_profile(
    vendor_name,
    service,
    business_owner,
    deployment_model,
    business_criticality,
    personal_information,
    payment_card_data,
    health_information,
    confidential_business_data,
    sso_supported,
    mfa_supported,
    api_access,
    privileged_access,
    soc_2_type_2,
    iso_27001,
    penetration_testing,
    edr_deployed,
    log_retention_days,
    encryption_at_rest,
    encryption_in_transit,
    incident_response_plan,
    business_continuity_plan,
    subprocessor_management,
):
    return {
        "vendor_name": vendor_name,
        "service": service,
        "business_owner": business_owner,
        "deployment_model": deployment_model,
        "business_criticality": business_criticality,
        "hosting_provider": "User-provided test scenario",
        "data_access": {
            "personal_information": personal_information,
            "payment_card_data": payment_card_data,
            "health_information": health_information,
            "confidential_business_data": confidential_business_data,
        },
        "integration": {
            "sso_supported": sso_supported,
            "mfa_supported": mfa_supported,
            "api_access": api_access,
            "privileged_access": privileged_access,
        },
        "security_responses": {
            "soc_2_type_2": soc_2_type_2,
            "iso_27001": iso_27001,
            "penetration_testing": penetration_testing,
            "edr_deployed": edr_deployed,
            "log_retention_days": log_retention_days,
            "encryption_at_rest": encryption_at_rest,
            "encryption_in_transit": encryption_in_transit,
            "incident_response_plan": incident_response_plan,
            "business_continuity_plan": business_continuity_plan,
            "subprocessor_management": subprocessor_management,
        },
        "vendor_commitments": {
            "penetration_test": (
                "Within an approved remediation period"
                if not penetration_testing
                else "Completed"
            ),
            "edr_implementation": (
                "Within an approved remediation period"
                if not edr_deployed
                else "Completed"
            ),
            "log_retention": (
                "Increase to 180 days"
                if log_retention_days < 180
                else "Requirement met"
            ),
        },
    }


st.title("AI Vendor Risk Assessment")
st.caption(
    "A human-governed portfolio demonstration for evaluating "
    "third-party cybersecurity risks."
)

st.warning(
    "Use fictional or synthetic information only. Do not submit actual "
    "vendor data, SOC reports, personal information, credentials, or "
    "confidential employer documentation."
)

with st.sidebar:
    st.header("About this demonstration")
    st.write(
        "The application evaluates test information against a defined "
        "third-party security control library."
    )
    st.write(
        "Results are preliminary and require validation by a qualified "
        "security professional."
    )
    st.info(
        "The application cannot approve a vendor or accept security risk."
    )

with st.form("vendor_assessment_form"):
    st.subheader("1. Vendor and service information")

    column_one, column_two = st.columns(2)

    with column_one:
        vendor_name = st.text_input(
            "Fictional vendor name",
            value="NorthStar Analytics",
        )
        service = st.text_area(
            "Service description",
            value="Cloud-based customer analytics platform",
        )
        business_owner = st.text_input(
            "Business owner",
            value="Marketing",
        )

    with column_two:
        deployment_model = st.selectbox(
            "Deployment model",
            ["SaaS", "PaaS", "IaaS", "On-premises", "Professional service"],
        )
        business_criticality = st.selectbox(
            "Business criticality",
            ["Low", "Moderate", "High"],
            index=2,
        )

    st.subheader("2. Information in scope")

    data_one, data_two = st.columns(2)

    with data_one:
        personal_information = st.checkbox(
            "Personal information",
            value=True,
        )
        payment_card_data = st.checkbox("Payment-card information")
        health_information = st.checkbox("Health information")

    with data_two:
        confidential_business_data = st.checkbox(
            "Confidential business information",
            value=True,
        )

    st.subheader("3. Access and integration")

    integration_one, integration_two = st.columns(2)

    with integration_one:
        sso_supported = st.checkbox("SSO supported", value=True)
        mfa_supported = st.checkbox("MFA supported", value=True)

    with integration_two:
        api_access = st.checkbox("API access", value=True)
        privileged_access = st.checkbox("Privileged access")

    st.subheader("4. Security control information")

    control_one, control_two = st.columns(2)

    with control_one:
        soc_2_type_2 = st.checkbox("Current SOC 2 Type II report", value=True)
        iso_27001 = st.checkbox("Current ISO 27001 certification")
        penetration_testing = st.checkbox(
            "Independent penetration testing completed"
        )
        edr_deployed = st.checkbox("EDR deployed")

    with control_two:
        encryption_at_rest = st.checkbox(
            "Encryption at rest",
            value=True,
        )
        encryption_in_transit = st.checkbox(
            "Encryption in transit",
            value=True,
        )
        incident_response_plan = st.checkbox(
            "Incident-response plan",
            value=True,
        )
        business_continuity_plan = st.checkbox(
            "Business-continuity plan",
            value=True,
        )

    log_retention_days = st.slider(
        "Security-log retention in days",
        min_value=0,
        max_value=365,
        value=30,
        step=30,
    )

    subprocessor_management = st.selectbox(
        "Subprocessor-risk management status",
        ["Not implemented", "Partial", "Implemented"],
        index=1,
    )
    include_ai_review = st.checkbox(
        "Include simulated provider-neutral AI review",
        value=True,
        help=(
            "Demonstrates the external model boundary without making "
            "network requests or using an actual AI service."
        ),
    )
    consent = st.checkbox(
        "I confirm that this scenario contains only fictional or "
        "synthetic information."
    )

    submitted = st.form_submit_button(
        "Run assessment",
        type="primary",
        use_container_width=True,
    )


if submitted:
    if not consent:
        st.error(
            "Confirm that the information is fictional or synthetic "
            "before running the assessment."
        )
        st.stop()

    if not vendor_name.strip() or not service.strip():
        st.error("Enter a fictional vendor name and service description.")
        st.stop()

    vendor = build_vendor_profile(
        vendor_name,
        service,
        business_owner,
        deployment_model,
        business_criticality,
        personal_information,
        payment_card_data,
        health_information,
        confidential_business_data,
        sso_supported,
        mfa_supported,
        api_access,
        privileged_access,
        soc_2_type_2,
        iso_27001,
        penetration_testing,
        edr_deployed,
        log_retention_days,
        encryption_at_rest,
        encryption_in_transit,
        incident_response_plan,
        business_continuity_plan,
        subprocessor_management,
    )

    controls = load_controls()
    inherent_risk = determine_inherent_risk(vendor)
    findings = assess_vendor(vendor, controls)
    report = render_report(vendor, inherent_risk, findings)
    ai_review = None

    if include_ai_review:
        ai_prompt = build_assessment_prompt(
            vendor,
            controls,
            findings,
            inherent_risk,
        )
        ai_provider = MockAssessmentProvider()
        ai_review = ai_provider.generate(ai_prompt)
    st.divider()
    st.header("Assessment results")

    metric_one, metric_two, metric_three = st.columns(3)

    metric_one.metric("Inherent risk", inherent_risk)
    metric_two.metric("Control gaps", len(findings))
    metric_three.metric(
        "Human review",
        "Required" if findings else "Standard approval",
    )

    if inherent_risk == "High":
        st.error(
            "Preliminary high risk: material findings require human review."
        )
    elif inherent_risk == "Moderate":
        st.warning(
            "Preliminary moderate risk: validate controls and evidence."
        )
    else:
        st.success(
            "Preliminary low risk: complete normal assessment approval."
        )

    st.subheader("Identified findings")

    if not findings:
        st.success("No control gaps were identified by the current rules.")
    else:
        for number, finding in enumerate(findings, start=1):
            with st.expander(
                f"{number}. {finding['title']} — {finding['severity']}",
                expanded=number == 1,
            ):
                st.write(f"**Control:** {finding['control']['control_id']}")
                st.write(f"**Domain:** {finding['control']['domain']}")
                st.write(f"**Status:** {finding['status']}")
                st.write("**Condition**")
                st.write(finding["condition"])
                st.write("**Risk statement**")
                st.write(finding["risk"])
                st.write("**Recommendation**")
                st.write(finding["recommendation"])
                st.write(
                    "**Human review:** "
                    + (
                        "Required"
                        if finding["human_review"]
                        else "Standard assessment approval"
                    )
                )
    if ai_review:
        st.subheader("Simulated provider-neutral AI review")

        st.info(
            "Simulation notice: This review was generated by the mock "
            "provider. No external AI service or production model was used."
        )

        with st.expander(
            "View simulated AI-assisted review",
            expanded=False,
        ):
            st.markdown(ai_review)
    st.subheader("Download test results")

    download_one, download_two = st.columns(2)

    with download_one:
        st.download_button(
            "Download assessment report",
            data=report,
            file_name="vendor-risk-assessment.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with download_two:
        st.download_button(
            "Download test vendor profile",
            data=json.dumps(vendor, indent=2),
            file_name="test-vendor-profile.json",
            mime="application/json",
            use_container_width=True,
        )
    if ai_review:
        st.download_button(
            "Download simulated AI-assisted review",
            data=ai_review,
            file_name="simulated-ai-review.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with st.expander("View complete assessment report"):
        st.markdown(report)

    st.caption(
        "This output is a preliminary portfolio demonstration and does "
        "not constitute vendor approval, audit advice, or risk acceptance."
    )