<div align="center">
  <a href="README.md">🇺🇸 English</a> | 
  <a href="README_CN.md">🇨🇳 简体中文</a> | 
  <a href="README_TW.md">🇭🇰 繁體中文</a> | 
  <a href="README_JP.md">🇯🇵 日本語</a> |
  <a href="README_FR.md">🇫🇷 Français</a> |
  <a href="README_ES.md">🇪🇸 Español</a>
</div>
<br/>



# 🛡️ HFish Honeypot Threat Feed

[![Update Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yuexuan521/honeypot-blocklist)
[![Data Source](https://img.shields.io/badge/Source-HFish-blue.svg)](https://hfish.net/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)
[![Data Quality Check](https://github.com/yuexuan521/honeypot-blocklist/actions/workflows/data_quality.yml/badge.svg)](https://github.com/yuexuan521/honeypot-blocklist/actions/workflows/data_quality.yml)

> **⚠️ Warning**: This threat feed is automatically generated. While whitelisting mechanisms are in place, please evaluate the risks before deploying it in a production environment.

## 📖 Introduction

This project provides an open-source **Threat Intelligence Feed** derived from a high-interaction honeypot system (HFish) deployed in a real-world internet environment.

It captures malicious behaviors such as SSH/RDP brute-force attacks, web vulnerability scanning, and unauthorized database access in real-time. The data is processed through automated scripts and whitelisting filters to generate a **High Fidelity** list of malicious IPs.

## 🔗 Subscription URLs

You can use the following links directly in your Firewall, WAF, or SIEM systems:

| Format  | URL (Direct Link)                                            | Description                                                  |
| :------ | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **TXT** | [ip_list.txt](https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt) | Plain text, one IP per line. Suitable for Firewall EDL, Linux IPSet. |

## 📊 Metadata

*   **Source**: HFish Honeypot (V3+), Public Internet.
*   **Attack Types**: SSH/RDP Brute-force, Web Exploits, Database Scanners.
*   **Time Window**: Last **24 Hours** only.
*   **Update Frequency**: Every **2~4 Hours**.
*   **Whitelisting**: Automatically excludes GoogleBot, BingBot, GitHub Services, and Cloudflare.

## 🛠️ Usage Example (Linux IPSet)

```bash
# 1. Download the list
wget -O /tmp/blacklist.txt https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt

# 2. Create IPSet
ipset create honeypot_blacklist hash:ip hashsize 4096

# 3. Import IPs
while read ip; do ipset add honeypot_blacklist $ip; done < /tmp/blacklist.txt

# 4. Block in Iptables
iptables -I INPUT -m set --match-set honeypot_blacklist src -j DROP
```
## 🛠️ Developer Tools & SDK (开发者工具)

We provide a Python SDK and CLI tool to help developers integrate this feed easily.

### 1. Python SDK Usage
You can use our `ThreatFeedClient` in your own Python projects:

```python
from tools.client import ThreatFeedClient

feed = ThreatFeedClient()
feed.fetch_data()

# Check an IP
if feed.is_malicious("192.168.1.5"):
    print("Block this IP!")
```

### 2. CLI Tool Usage (Command Line)

Administrators can use the CLI to check IPs or export data:

```
# Check specific IP
python3 tools/cli.py --check 1.2.3.4
# Output: ✅ SAFE: IP 1.2.3.4 is not currently listed.

# Export as JSON
python3 tools/cli.py --export json
```

### 3. Docker Usage

Run the tool without installing Python dependencies:

```
docker build -t hfish-feed .
docker run --rm hfish-feed --check 1.1.1.1
```

## 🔌 Integrations (集成方案)

We provide ready-to-use configurations for popular infrastructure:

| Platform                                           | Type   | Description                                          |
| :------------------------------------------------- | :----- | :--------------------------------------------------- |
| **[Nginx](integrations/nginx/)**                   | Script | Auto-generate `deny.conf` for web servers.           |
| **[Linux Firewall](integrations/linux-iptables/)** | Script | High-performance blocking with `ipset` + `iptables`. |
| **[Cloudflare](integrations/cloudflare/)**         | Worker | Serverless edge blocking script.                     |
| **[Palo Alto](integrations/paloalto/)**            | Docs   | Enterprise firewall EDL configuration guide.         |

## 🧰 For HFish Users: Generate Your Own Feed

If you are running your own HFish honeypot, you can use our open-source tool to generate threat feeds from your own data.

### Usage
1. Clone this repository.
2. Run the generator tool:
   - tools\generate_feed.py
   - tools\update_feed.sh

> Refer to this article:[Practical Guide: Building an Automated Threat Intelligence Source Based on HFish + Python + GitHub Pages](https://www.freebuf.com/articles/others-articles/467125.html)

## ⚖️ Disclaimer

1. **Accuracy**: The data is automatically captured. While we strive to minimize false positives, it may contain compromised hosts or dynamic IPs.
2. **At Your Own Risk**: The use of this data is voluntary.
3. **Liability**: The maintainer is not responsible for any **business interruption, network unavailability, or data loss** caused by blocking IPs from this list.

------



*Auto-generated by [HFish](https://hfish.net) & Python Automation Script.*	
