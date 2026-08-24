# Sample Third-Party Risk Assessment

## Executive Summary

NorthStar Analytics provides a Cloud-based customer analytics platform. The preliminary inherent-risk rating is **High**.

The assessment identified **4 control gaps**. Final vendor approval and risk acceptance require human review.

## Vendor Overview

- Vendor: NorthStar Analytics
- Service: Cloud-based customer analytics platform
- Deployment model: SaaS
- Business criticality: High
- Inherent risk: High

## Findings

### 1. Lack of Independent Penetration Testing

- Control: VM-01
- Domain: Vulnerability Management
- Severity: High
- Status: Planned

#### Condition

The vendor has not completed an independent penetration test. The vendor plans to complete one within 120 days of contract execution.

#### Risk Statement

Because the vendor has not completed an independent penetration test, exploitable weaknesses may remain unidentified, potentially resulting in unauthorized access, data exposure, or service disruption.

#### Recommendation

Complete an independent penetration test and provide the executive summary, scope, testing dates, material findings, and remediation evidence.

#### Human Review

Required

### 2. Endpoint Detection and Response Not Deployed

- Control: EP-01
- Domain: Endpoint Security
- Severity: High
- Status: Planned

#### Condition

EDR is not currently deployed. The vendor plans implementation within 30 days of contract execution.

#### Risk Statement

Because EDR is not deployed, malicious endpoint activity may not be detected or contained promptly, potentially resulting in system compromise or data loss.

#### Recommendation

Deploy EDR across applicable endpoints and provide configuration evidence and an endpoint coverage report.

#### Human Review

Required

### 3. Insufficient Security Log Retention

- Control: LOG-01
- Domain: Logging and Monitoring
- Severity: Medium
- Status: Partially implemented

#### Condition

Security logs are retained for 30 days instead of the required 180 days.

#### Risk Statement

Because security logs are not retained for the required period, the vendor may be unable to investigate incidents or reconstruct malicious activity.

#### Recommendation

Increase log retention to at least 180 days and provide the logging policy or platform configuration as evidence.

#### Human Review

Review during normal assessment approval

### 4. Partial Subprocessor Risk Management

- Control: TPRM-02
- Domain: Fourth-Party Risk
- Severity: Medium
- Status: Partially implemented

#### Condition

The vendor reported that its subprocessor-management process is only partially implemented.

#### Risk Statement

Because subprocessors are not fully assessed, security weaknesses at a fourth party could expose organizational data or disrupt the service.

#### Recommendation

Maintain a subprocessor inventory, perform documented security reviews, and provide notification of material subprocessor changes.

#### Human Review

Review during normal assessment approval

## Preliminary Residual Risk

**High** until the high-risk findings are remediated and validated.

## Limitations

- This assessment uses fictional data.
- Findings require validation by a qualified security professional.
- Planned remediation is not treated as an implemented control.
- This output does not constitute final vendor approval.