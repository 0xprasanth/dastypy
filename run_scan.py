# run_scan.py
import argparse
import time
import json
from pathlib import Path
from utils.zap_client import ZapClient
from utils.report_generator import generate_markdown_summary, generate_html_report, save_json
from utils.helpers import load_config, ensure_reports_dir
from rich.console import Console

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Run DAST using OWASP ZAP via API")
    parser.add_argument("--config", "-c", default="config.yaml", help="Path to config.yaml")
    parser.add_argument("--target", "-t", help="Override target from config")
    args = parser.parse_args()

    cfg = load_config(args.config)
    zap_cfg = cfg.get("zap", {})
    scan_cfg = cfg.get("scan", {})
    output_cfg = cfg.get("output", {})
    reports_cfg = cfg.get("reports", {})
    reports_dir = ensure_reports_dir(output_cfg.get("reports_dir", "reports"))

    target = args.target or scan_cfg.get("target")
    if not target:
        console.print("[red]No target specified. Use --target or set scan.target in config.yaml[/red]")
        return

    zap = ZapClient(host=zap_cfg.get("host", "127.0.0.1"), port=zap_cfg.get("port", 8080), api_key=zap_cfg.get("api_key", ""))

    console.print(f"[bold]Target:[/bold] {target}")
    # Spider
    spider_id = zap.spider(target, context_name=scan_cfg.get("context"))
    zap.wait_for_spider(spider_id, timeout=scan_cfg.get("max_scan_time", 300))
    time.sleep(1)  # brief pause

    # Active scan
    scan_id = zap.active_scan(target, context_name=scan_cfg.get("context"))
    zap.wait_for_active_scan(scan_id, timeout=scan_cfg.get("max_scan_time", 900))

    # Get alerts as JSON
    console.print("[blue]Fetching alerts from ZAP[/blue]")
    raw_json = zap.full_report_json()
    # The python ZAP API returns a JSON string -- parse it
    try:
        alerts_obj = json.loads(raw_json)
    except Exception:
        # Fallback: try to query alerts endpoint
        alerts_obj = {"site": []}

    # Flatten alerts for summary (ZAP JSON structure might be nested per site)
    alerts_flat = []
    for site in alerts_obj.get("site", []):
        for alert in site.get("alerts", []):
            alerts_flat.append(alert)

    timestamp = int(time.time())
    base_name = f"scan-{timestamp}"
    # Save JSON
    json_path = Path(reports_dir) / f"{base_name}.json"
    save_json(alerts_obj, str(json_path))
    console.print(f"[green]Saved JSON report -> {json_path}[/green]")

    # Save HTML (full report)
    html_out = Path(reports_dir) / f"{base_name}.html"
    html_content = zap.full_report_html()
    generate_html_report(html_content, str(html_out))
    console.print(f"[green]Saved HTML report -> {html_out}[/green]")

    # Save Markdown summary
    md_out = Path(reports_dir) / f"{base_name}.md"
    generate_markdown_summary(alerts_flat, str(md_out))
    console.print(f"[green]Saved Markdown summary -> {md_out}[/green]")

    console.print("[bold green]DAST run complete[/bold green]")

if __name__ == "__main__":
    main()
