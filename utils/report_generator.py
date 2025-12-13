# utils/report_generator.py
import os
import json
from datetime import datetime

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_text(content, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_markdown_summary(alerts, out_path):
    """
    alerts: list of alert dicts (from ZAP JSON)
    """
    ensure_dir(os.path.dirname(out_path) or ".")
    by_severity = {}
    for a in alerts:
        severity = a.get("risk", "Info")
        by_severity.setdefault(severity, []).append(a)

    md = []
    md.append(f"# DAST Scan Summary - {datetime.utcnow().isoformat()}Z\n")
    for severity in sorted(by_severity.keys(), reverse=True):
        md.append(f"## {severity} ({len(by_severity[severity])})\n")
        for a in by_severity[severity]:
            md.append(f"- **{a.get('alert')}** — `{a.get('risk')}` — {a.get('url')}\n")
            md.append(f"  - CWE: {a.get('cweid')}  Confidence: {a.get('confidence')}\n")
            if a.get("evidence"):
                md.append(f"  - Evidence: `{a.get('evidence')}`\n")
            md.append("\n")

    save_text("\n".join(md), out_path)

def generate_html_report(html_content, out_path):
    ensure_dir(os.path.dirname(out_path) or ".")
    save_text(html_content, out_path)
