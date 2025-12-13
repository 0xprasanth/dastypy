# utils/helpers.py
import yaml
import os

def load_config(path="config.yaml"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def ensure_reports_dir(reports_dir):
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir, exist_ok=True)
    return reports_dir
