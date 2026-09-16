from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
POLICY = Path(os.getenv("AI_SECURITY_POLICY", ROOT / "policies" / "approved_tools.yaml"))
LOG = Path(os.getenv("AI_SECURITY_AUDIT_LOG", ROOT / "audit.jsonl"))

PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "phone": re.compile(r"(?<!\d)(?:\+?1[-. ]?)?\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}(?!\d)"),
    "password": re.compile(r"\b(?:password|passwd|pwd)\s*[:=]\s*\S+", re.I),
    "api_key": re.compile(r"\b(?:api[_ -]?key|access[_ -]?token|token|secret)\s*[:=]\s*[A-Za-z0-9_\-]{8,}", re.I),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def load_tools() -> dict[str, dict[str, Any]]:
    data = yaml.safe_load(POLICY.read_text(encoding="utf-8")) or {}
    return data.get("tools", {})


def scan(text: str) -> list[str]:
    """Return finding categories only; never return the sensitive values."""
    return sorted(name for name, pattern in PATTERNS.items() if pattern.search(text or ""))


def _write_audit(event: dict[str, Any]) -> None:
    """Write metadata only. Submitted prompt text is deliberately excluded."""
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, separators=(",", ":")) + "\n")


def evaluate(tool: str, text: str, data_class: str = "public", *, write_audit: bool = True) -> dict[str, Any]:
    tools = load_tools()
    cfg = tools.get(tool)
    findings = scan(text)

    if not cfg or not cfg.get("approved", False):
        decision, reason = "BLOCK", "Tool is not approved"
    elif findings:
        decision, reason = "BLOCK", "Sensitive information detected: " + ", ".join(findings)
    elif data_class in cfg.get("human_review_for", []):
        decision, reason = "REVIEW", "Human approval required before AI use"
    elif data_class not in cfg.get("allowed_data", []):
        decision, reason = "BLOCK", f"{data_class} data is not allowed for this tool"
    else:
        decision, reason = "ALLOW", "Checks passed"

    event = {
        "time": datetime.now(timezone.utc).isoformat(),
        "tool": tool,
        "data_class": data_class,
        "decision": decision,
        "reason": reason,
        "findings": findings,
    }
    if write_audit:
        _write_audit(event)
    return event


def main() -> None:
    parser = argparse.ArgumentParser(description="AI security guardrail reference demo")
    parser.add_argument("--tool", required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--data-class", default="public", choices=["public", "internal", "customer", "confidential"])
    args = parser.parse_args()
    print(json.dumps(evaluate(args.tool, args.text, args.data_class), indent=2))


if __name__ == "__main__":
    main()
