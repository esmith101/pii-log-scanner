# PII Log Scanner

This repo contains a Claude Code skill for security engineers at fintech and healthcare companies. It scans Python service files for log statements that expose PII or sensitive financial data before code reaches production.

## Available commands

- `/scan-pii` — scan files or a directory for PII in log statements. Pass a path as an argument, or run without arguments to scan the current directory.

## Sample files

The `sample/` directory contains three Python payment services with realistic PII logging violations for demonstration and testing.
