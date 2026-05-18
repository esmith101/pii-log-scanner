# pii-log-scanner

A Claude Code plugin for security engineers at fintech and healthcare companies. Scans application log statements for PII and sensitive financial data — card numbers, SSNs, account numbers — before code reaches production.

**Persona:** A security engineer who needs to catch PII exposure in logs at the PR stage, not six months later when an auditor runs a query against your SIEM.

**What it does:**
- Scans Python service files for log statements that expose PII
- Maps every finding to the relevant regulation (PCI DSS, SOC2 CC6.7, GLBA)
- Proposes the correct fix per data type (mask card numbers to last-4, remove CVV entirely, mask SSNs)
- Stops for human approval before touching any code
- Writes a findings report formatted for your compliance team
- Reminds you to scan before every `git push`

---

## Install and try it in under 5 minutes

### 1. Clone the repo

```bash
git clone https://github.com/your-username/pii-log-scanner.git
cd pii-log-scanner
```

### 2. Start Claude Code with the plugin loaded

Navigate to the `sample/` directory (three payment service files with real PII violations), then start Claude Code pointing at the plugin root:

```bash
cd sample
claude --plugin-dir ..
```

### 3. Run the scan

```
/scan-pii
```

Claude Code will scan `payment_service.py`, `user_service.py`, and `transaction_service.py`, surface every finding by severity, show proposed fixes, and wait for your approval before changing anything.

### 4. Approve the fixes and generate the report

```
approve all fixes and write the report
```

A `pii_scan_report.md` will appear in the current directory, formatted for auditors.

### 5. See the push hook in action

From within the Claude Code session, ask Claude to run:

```
run: git push
```

The pre-push hook fires before the command executes and reminds you to scan first.

---

## Scan your own codebase

Point the skill at any directory:

```
/scan-pii ../path/to/your/services
```

Or scan a single file:

```
/scan-pii payment_service.py
```

---

## What's in the plugin

```
pii-log-scanner/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── skills/
│   └── scan-pii/
│       └── SKILL.md         # Agent instructions — invoke with /scan-pii
├── hooks/
│   └── hooks.json           # PreToolUse hook on git push
├── scripts/
│   └── check-push.sh        # Hook script — warning fires in milliseconds, never blocks
└── sample/                  # Three Python services with realistic PII violations
    ├── payment_service.py   # Card numbers and CVV in logs (PCI DSS)
    ├── user_service.py      # Full SSN in logs (SOC2 CC6.7)
    └── transaction_service.py  # Account and routing numbers in logs (GLBA)
```

---

## Why this catches what SAST tools miss

Static analysis tools like Semgrep pattern-match on variable names. They catch `logger.log(card_number)` if you wrote a rule for it. They miss:

```python
logger.error(f"transaction failed: {payment_context}")
```

...where `payment_context` happens to hold card data. This scanner reads the value being passed into each log call and understands what it is — it doesn't rely on the variable being named `ssn` or `card_number`.

---

## What I'd do with more time

- Add support for JavaScript/TypeScript log statements (Winston, Pino, console.log)
- Add a CI mode (`claude --print "/scan-pii ." --no-color > pii_scan.md`) with a non-zero exit code on Critical findings, so the scan gates PRs automatically
- Add a baseline file so teams can suppress known false positives without editing the plugin
