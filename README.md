# **ZAP DAST Automation Framework**

### **Automated Dynamic Application Security Testing using Python + OWASP ZAP**

This project is a production-ready **DAST automation framework** built with **Python** and **OWASP ZAP**, designed to help developers and security engineers automatically scan web applications for OWASP Top 10 vulnerabilities.

It supports spidering, active scanning, alert extraction, severity-based filtering, and multiple reporting formats, and can be integrated directly into CI/CD pipelines.

---

## 🚀 **Features**

* 🔍 Automated **Spider + Active Scan**
* 🛡️ Detects OWASP Top 10 issues (XSS, SQLi, SSRF, CSRF, IDOR, etc.)
* 📝 Exports results to **HTML, JSON, Markdown**
* 🎛️ Configurable scan settings via `config.yaml`
* 🧪 Optional CI/CD integration (GitHub Actions)
* 📊 Severity-based vulnerability classification
* 🐳 Supports ZAP Docker image
* ⚡ Parallel scans for multiple URLs

---

## 🧰 **Tech Stack**

* **Python 3.10+**
* **OWASP ZAP (Daemon Mode)**
* **python-owasp-zap-v2.4 SDK**
* **Rich (for terminal styling)**
* **YAML (for configuration)**

---

## 📦 **Installation**

### 1️⃣ Clone the repo

```bash
git clone https://github.com/0xprasanth/dastypy
cd zap-dast-automation
```

### 2️⃣ Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Start OWASP ZAP (no UI)

```bash
zap.sh -daemon -port 8080 -config api.disablekey=true
```

(or using Docker)

```bash
docker run -u zap -p 8080:8080 -i ghcr.io/zaproxy/zaproxy:stable zap.sh -daemon -port 8080 -config api.disablekey=true
```

---

## ⚙️ **Configuration**

Edit `config.yaml`:

```yaml
target: "https://example.com"
exclude:
  - "https://example.com/logout"
reports:
  - html
  - json
  - md
timeout: 300
```

---

## ▶️ **Usage**

### Run a full DAST scan:

```bash
python run_scan.py --target https://example.com
```

### Output Reports:

* `/reports/scan-results.html`
* `/reports/scan-results.json`
* `/reports/scan-results.md`

---

## 📊 **Sample Report Output**

```
High Severity (3)
 - SQL Injection in /login
 - XSS in /search

Medium Severity (2)
 - Missing Security Headers
 - Insecure Cookie Flags
```


## 🏗️ **Project Structure**

```
zap-dast-automation/
│── config.yaml
│── run_scan.py
│── utils/
│   ├── zap_client.py
│   ├── report_generator.py
│   └── helpers.py
│── reports/
│── README.md
│── requirements.txt
```

---

## 📘 **Roadmap**

* Add authenticated scanning
* Add context importing
* Add Slack/Email alerting
* Add dashboard UI
* Add parallel scanning engine
* Add CI/CD Integration for github Actions

---

## 🛡️ **License**

MIT License — free to use, modify, and share.
