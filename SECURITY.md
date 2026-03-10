# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| Latest | ✅ |

## Reporting a Vulnerability

We take the security of this threat feed and its supporting tooling seriously.

To help us respond appropriately, please use the correct reporting channel depending on the type of issue.

### Use GitHub Issues for

Please open a public GitHub Issue for:

- false positives
- feed quality problems
- documentation mistakes
- non-sensitive bugs
- integration problems
- general questions about usage

### Report privately for security vulnerabilities

Please **do not open a public issue** for security-sensitive problems.

Instead, report them privately by email to:

**yuexuan521@gmail.com**

Examples of issues that should be reported privately:

- sensitive data exposure
- vulnerabilities in repository code or automation
- dependency-related security issues
- exploitable flaws in the SDK or CLI
- issues that could help an attacker bypass protections or abuse the project

### What to include in a private report

Please include as much of the following as possible:

- affected component
- clear reproduction steps
- impact assessment
- relevant logs or screenshots
- any suggested remediation, if available

Please remove or redact sensitive information before sending logs or screenshots.

### Response process

We will acknowledge receipt of your report within **48 hours** and will investigate it as quickly as possible.

When appropriate, we may coordinate with the reporter on validation, remediation, and disclosure timing.

## Scope

This policy applies to:

- repository code
- automation workflows
- published tooling such as the SDK and CLI
- documentation or integration artifacts where a security issue may create real risk

It does **not** apply to normal false-positive disputes or general feed quality discussions, which should go through GitHub Issues.

## Disclaimer

This project publishes a defensive threat feed and related tooling.  
Use in production should always be validated in your own environment, with appropriate monitoring, rollback planning, and allowlist controls.
