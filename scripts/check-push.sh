#!/bin/bash
# PII pre-push reminder hook
# Fires before any bash command. If the command is a git push,
# reminds the engineer to run a PII scan first.
#
# Claude Code passes tool input as JSON via stdin:
# {"command": "git push origin main", ...}

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('command', ''))
except:
    print('')
" 2>/dev/null)

if echo "$COMMAND" | grep -qE "git push"; then
    echo "" >&2
    echo "⚠️  About to push — have you scanned for PII in log statements?" >&2
    echo "   Run: /scan-pii <path-to-service-dir> to check before this push." >&2
    echo "" >&2
fi

# Always exit 0 — this is a reminder, not a blocker
exit 0
