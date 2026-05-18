# pii-log-scanner

A Claude Code skill for security engineers at fintech and healthcare companies. Scans application log statements for PII and sensitive financial data — card numbers, SSNs, account numbers — before code reaches production.

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

### Option A: Marketplace install (when available)

```
/plugin marketplace add https://github.com/esmith101/pii-log-scanner
```

The plugin installs via the canonical `.claude-plugin/` manifest. Use this when the Claude Code marketplace install source type is supported in your version.

### Option B: Direct clone (works today)

```bash
git clone https://github.com/esmith101/pii-log-scanner.git
cd pii-log-scanner
```

### 2. Start Claude Code

```bash
claude
```

The `/scan-pii` command and pre-push hook load automatically from `.claude/`.

### 3. Run the scan against the sample files

Pass the directory you want to scan as the argument:

```
/scan-pii sample/
```

Claude Code will scan `payment_service.py`, `user_service.py`, and `transaction_service.py`, surface every finding by severity, show proposed fixes, and wait for your approval before changing anything.

### 4. Approve the fixes and generate the report

```
approve all fixes and write the report
```

A `pii_scan_report.md` will appear in the current directory, formatted for auditors.

### 5. See the pre-push hook in action

Ask Claude to run a git push:

```
run: git push
```

The hook fires before the command executes and reminds you to scan first.

---

## Scan your own codebase

Point the command at any directory or file:

```
/scan-pii ../path/to/your/services
```

```
/scan-pii payment_service.py
```

---

## What's in the repo

```
pii-log-scanner/
├── CLAUDE.md                        # Project context
├── .claude/
│   ├── commands/
│   │   └── scan-pii.md              # /scan-pii slash command (direct clone install)
│   └── settings.json                # Pre-push hook (direct clone install)
├── .claude-plugin/
│   ├── plugin.json                  # Canonical plugin manifest (marketplace install)
│   └── marketplace.json             # Marketplace registry entry
├── skills/
│   └── scan-pii/
│       └── SKILL.md                 # Skill definition (marketplace install)
├── hooks/
│   └── hooks.json                   # Hook definitions (marketplace install)
└── sample/                          # Three Python services with realistic PII violations
    ├── payment_service.py           # Card numbers and CVV in logs (PCI DSS)
    ├── user_service.py              # Full SSN in logs (SOC2 CC6.7)
    └── transaction_service.py       # Account and routing numbers in logs (GLBA)
```

Both install paths use identical skill and hook logic — the `.claude/` files are the working primitives today; the `.claude-plugin/` manifest is the canonical format for marketplace distribution.

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
- Add a baseline file so teams can suppress known false positives without editing the skill
- Validate hook behavior with the Claude Code team for marketplace plugin distribution
