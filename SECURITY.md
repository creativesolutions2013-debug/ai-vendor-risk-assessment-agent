# Security Policy

## Purpose

This repository is a portfolio demonstration of a third-party risk
assessment workflow. It is not approved for processing production,
confidential, regulated, or proprietary information.

## Permitted Data

Use only:

- Fictional vendor information
- Synthetic security evidence
- Publicly available control information
- Test data created specifically for this project

## Prohibited Data

Do not upload or process:

- Actual vendor assessments
- SOC 1 or SOC 2 reports
- Customer or employee information
- Personal, payment-card, or health information
- Employer or client documentation
- Confidential policies or control evidence
- Passwords, API keys, access tokens, or credentials

## Secrets Management

Credentials must never be stored directly in source code, prompts, sample
data, commit history, or configuration files committed to the repository.

Any future AI-provider credential must be supplied through an approved
environment variable or secret-management mechanism.

## AI Security Considerations

AI-generated assessment content must be treated as a draft. Users must:

- Validate findings against source evidence
- Review control mappings
- Confirm risk ratings
- Check for unsupported assumptions
- Prevent sensitive data from entering prompts
- Require human approval for material risk decisions

## Vulnerability Reporting

Do not report suspected security vulnerabilities through a public GitHub
issue.

Contact the repository owner privately through the contact information
provided on the GitHub profile.

## Disclaimer

This project does not provide legal, audit, compliance, or risk-acceptance
advice. Final decisions must be made by an authorized and qualified person.