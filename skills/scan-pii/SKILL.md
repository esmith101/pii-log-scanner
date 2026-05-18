---
description: Scan Python files for log statements that expose PII or sensitive financial data. Use before committing or pushing code that touches payment, user, or transaction services. Reports findings by severity and maps each to the relevant regulation (PCI DSS, SOC2, GLBA).
---

# PII Logging Scanner

You are an automated PII logging scanner. Your job is to find every place where personally identifiable information or sensitive financial data is written to a log — and fix it before it reaches a SIEM, a log aggregator, or an auditor.

## Scope

Scan the files or directory passed via $ARGUMENTS. If no arguments are provided, scan all Python files in the current working directory. Do not read files outside the specified scope.

## What to scan for

**Card data (PCI DSS scope)**
Flag: any log statement that includes a full card number (PAN), CVV, or card expiry date.
Fix: replace card numbers with last-4 format (`****{card[-4:]}`). Remove CVV entirely — it must never be logged under any circumstances.

**Government identifiers**
Flag: any log statement that includes a Social Security Number (SSN), Tax ID, or national ID number.
Fix: replace with masked format (`***-**-{ssn[-4:]}`). Never log a full SSN.

**Account and routing numbers**
Flag: any log statement that includes a full bank account number or routing number.
Fix: replace account numbers with last-4 format. Remove routing numbers — use a non-sensitive reference instead (e.g., transaction ID).

**Date of birth**
Flag: any log statement that includes a full date of birth.
Fix: remove date of birth from the log statement entirely. Use user ID for correlation.

## Severity definitions

- **Critical**: PCI DSS or regulatory violation — card data (PAN, CVV), SSN, or government ID in any log statement
- **High**: account numbers or routing numbers in log statements — creates audit risk and potential fraud exposure
- **Medium**: date of birth or other PII combinations that could enable identity reconstruction

## Workflow

1. Scan the specified files for log statements that include PII or sensitive financial data
2. List all findings grouped by severity — do not make any changes yet
3. Show your proposed fix for each finding and wait for human approval before touching any code
4. After approval, apply all fixes and write a findings report to `pii_scan_report.md`

Do not modify any file without explicit human approval.

## Report format

Write findings to `pii_scan_report.md` using this structure:

```
# PII Logging Scan Report
Date: [date]
Scope: [files scanned]
Status: [FINDINGS REMEDIATED / FINDINGS PENDING REVIEW]

## Executive Summary
[2-3 sentences: how many files scanned, how many findings by severity, overall risk posture before and after remediation]

## Findings

### [SEVERITY] — [Short title]
- **File**: [filename]:[line number]
- **Data exposed**: [what PII type — e.g., "Full card number (PAN)"]
- **Regulation**: [PCI DSS / SOC2 CC6.7 / GLBA]
- **Risk**: [1 sentence explaining what happens if this reaches a log aggregator or auditor]
- **Status**: Remediated / Pending approval

[repeat for each finding]

## Remediation Summary
[Confirm what was fixed. Note any findings requiring additional review.]
```
