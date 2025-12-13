# utils/zap_client.py
from zapv2 import ZAPv2
import requests
import time
from rich.console import Console

console = Console()

class ZapClient:
    def __init__(self, host="127.0.0.1", port=8080, api_key=""):
        self.base = f"http://{host}:{port}"
        self.api_key = api_key
        self.zap = ZAPv2(apikey=api_key, proxies={'http': self.base, 'https': self.base})
        console.print(f"[green]Initialized ZAP client -> {self.base}[/green]")

    def spider(self, target, context_name=None):
        console.print(f"[cyan]Starting spider for {target}[/cyan]")
        res = self.zap.spider.scan(target, contextname=context_name)
        scan_id = res
        return scan_id

    def spider_status(self, scan_id):
        return int(self.zap.spider.status(scan_id))

    def wait_for_spider(self, scan_id, timeout=300, interval=2):
        console.print("[cyan]Monitoring spider progress...[/cyan]")
        start = time.time()
        while True:
            status = self.spider_status(scan_id)
            console.print(f"Spider status: {status}%")
            if status >= 100 or (time.time() - start) > timeout:
                break
            time.sleep(interval)
        console.print("[cyan]Spider completed or timed out[/cyan]")

    def active_scan(self, target, context_name=None, recurse=True, scan_policy_name=None):
        console.print(f"[magenta]Starting active scan for {target}[/magenta]")
        res = self.zap.ascan.scan(target, contextid=None, recurse=recurse, scanpolicyname=scan_policy_name)
        scan_id = res
        return scan_id

    def active_scan_status(self, scan_id):
        return int(self.zap.ascan.status(scan_id))

    def wait_for_active_scan(self, scan_id, timeout=900, interval=5):
        console.print("[magenta]Monitoring active scan progress...[/magenta]")
        start = time.time()
        while True:
            status = self.active_scan_status(scan_id)
            console.print(f"Active scan status: {status}%")
            if status >= 100 or (time.time() - start) > timeout:
                break
            time.sleep(interval)
        console.print("[magenta]Active scan completed or timed out[/magenta]")

    def alerts(self, baseurl=None, risklevel=None):
        # risklevel: "Low", "Medium", "High"
        return self.zap.core.alerts(baseurl=baseurl, riskid=None)

    def full_report_html(self):
        return self.zap.core.htmlreport()

    def full_report_xml(self):
        return self.zap.core.xmlreport()

    def full_report_json(self):
        return self.zap.core.jsonreport()

    def urls(self):
        return self.zap.core.urls
