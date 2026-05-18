# Build Your Own Claude Code Plugin
## A practical guide for engineers at fintech and healthcare companies

You've seen the PII scanner. Here's how to build one for a different workflow at your org — in an afternoon.

---

### The mental model

A plugin is three things:

1. **A skill** — the agent's instructions. This is where all the judgment lives: what to look for, how to classify it, what to do about it, what format to produce. Think of it as the senior engineer you'd normally have to pull into every PR review, encoded once.

2. **A hook** — makes the skill ambient. Instead of engineers remembering to run a scan, the hook fires automatically at the right moment (before a push, after a file write, on session start). Optional, but it's what separates a useful tool from one that gets forgotten.

3. **Sample files** — concrete examples of the problem you're solving. These let anyone on your team try the plugin in under five minutes without needing access to production code.

That's it. You don't need an MCP server unless you're calling an external API. You don't need a hook unless there's a natural trigger moment. Start with just the skill.

---

### Pick the right workflow

Good plugin candidates share three traits:
- A senior engineer is currently the bottleneck (code review, triage, audit prep)
- The judgment can be written down — if you can explain it in a doc, you can encode it in a skill
- The output has a consistent format (a report, a diff, a ranked list)

**Examples that work at your org:**
- Dependency CVE triage: scan `package.json` or `requirements.txt` against your approved/blocked list, rank findings by exploitability, draft the Jira ticket
- Secrets detection: scan staged files for hardcoded API keys, connection strings, and tokens before commit
- Terraform module reviewer: check new modules against your org's naming conventions, tagging requirements, and required outputs before they're shared across teams
- Incident postmortem generator: given a set of log files and a deployment history, draft the RCA in your org's standard format

---

### The four files to copy and modify

Clone the PII scanner repo and replace these four things:

**1. `skills/your-skill-name/SKILL.md`**
This is where you spend your time. Define:
- What you're scanning for (be specific — "hardcoded secrets" is too vague; list the patterns)
- Severity levels and what they mean at your company
- The exact fix or action for each finding type
- The output format (who reads this — an engineer, a compliance team, an on-call SRE?)

**2. `sample/`**
Add 2-3 real-looking files that contain the problem you're solving. Sanitize them — no actual credentials or customer data. The sample is how you demo the plugin and onboard your team.

**3. `.claude-plugin/plugin.json`**
Change `name`, `description`, and `keywords`. Everything else can stay the same.

**4. `hooks/hooks.json` and `scripts/check-push.sh`** *(only if you want a hook)*
Edit the grep pattern in the shell script to match the trigger that makes sense for your workflow. `git push` is right for a pre-push scanner. `git commit` works for secrets detection. You could also remove the hook entirely and just use the skill on demand.

---

### Test it before you share it

```bash
cd sample
claude --plugin-dir ..
```

Type your skill name to invoke it. Verify it finds what you expect, proposes the right fixes, and stops for approval before touching anything. Iterate on `SKILL.md` until the output is exactly what you'd want a junior engineer to hand you.

When it's ready, share the repo with your team. The install is the same two commands.

---

### One thing to get right

The quality of the skill is entirely in the specificity of `SKILL.md`. Generic instructions produce generic output. The more precisely you define what a violation looks like, what the correct fix is, and what the output format should be, the less you'll need to steer the agent during a real scan. Treat it like writing a runbook — the goal is that any engineer on your team could read it and know exactly what the agent is going to do.
