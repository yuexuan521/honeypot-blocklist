[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [Français](README_FR.md) | [Español](README_ES.md)

# HFish Honeypot Threat Feed

[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yuexuan521/honeypot-blocklist)
[![Source](https://img.shields.io/badge/Source-HFish-blue.svg)](https://hfish.net/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)
[![Data Quality Check](https://github.com/yuexuan521/honeypot-blocklist/actions/workflows/data_quality.yml/badge.svg)](https://github.com/yuexuan521/honeypot-blocklist/actions/workflows/data_quality.yml)

High-fidelity malicious IP feed generated from **HFish honeypot telemetry**, built for **Firewall / WAF / SIEM / IPSet / EDL** workflows.

This project continuously collects attacker IPs observed by publicly exposed HFish honeypots, applies automated filtering and whitelisting, and publishes a clean blocklist that can be consumed by security controls and automation pipelines.

> **Warning**
> This feed is generated automatically. Although filtering and whitelisting are applied, you should validate enforcement strategy before using it in production.

---

## Why this project exists

Internet-facing honeypots observe a large volume of brute-force attempts, exploit scans, and opportunistic intrusion traffic. This repository turns those observations into a reusable **defensive threat feed** so operators can:

- block recent attacker IPs at the edge
- enrich SIEM detections with known hostile sources
- automate deny rules in Linux firewalls and web infrastructure
- build their own HFish-based threat feed workflows

---

## What you get

- **24-hour rolling malicious IP feed**
- **Automatic refresh every 2–4 hours**
- **Plain-text subscription URL**
- **Python SDK and CLI**
- **Docker support**
- **Reference integrations** for Nginx, Linux firewall, Cloudflare, and Palo Alto
- **MIT-licensed open-source tooling**

---

## Threat feed URL

Use this URL directly in supported security products and scripts:

| Format | URL                                                          | Recommended use                                 |
| ------ | ------------------------------------------------------------ | ----------------------------------------------- |
| TXT    | `https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt` | Firewall EDL, Linux IPSet, WAF, SIEM enrichment |

---

## Feed profile

| Item               | Value                                                        |
| ------------------ | ------------------------------------------------------------ |
| Source             | HFish Honeypot (V3+)                                         |
| Observation scope  | Public Internet                                              |
| Included activity  | SSH/RDP brute-force, web exploitation/scanning, unauthorized service probing |
| Time window        | Last 24 hours                                                |
| Update cadence     | Every 2–4 hours                                              |
| Filtering          | Automatic cleanup and basic whitelisting                     |
| Typical exclusions | Known legitimate infrastructure such as GoogleBot, BingBot, GitHub services, and Cloudflare where applicable |

---

## Why trust this feed

This repository is designed to be simple, inspectable, and automation-friendly:

- **Open data format**: one IP per line, easy to audit and consume
- **Open tooling**: generation, client, and CLI logic live in the repository
- **Documented risk boundary**: false positives are possible and explicitly acknowledged
- **Operational focus**: built for direct use in real security controls, not just as a demo dataset

That said, no automated threat feed is perfect. Shared hosting, NAT gateways, compromised endpoints, and dynamic IP reassignment can all create noise. Review enforcement strategy before applying blocks globally.

---

## Quick start

### Linux IPSet + iptables

```bash
# 1) Download the latest feed
wget -O /tmp/blacklist.txt https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt

# 2) Create an IP set
ipset create honeypot_blacklist hash:ip hashsize 4096

# 3) Import IPs
while read ip; do
  ipset add honeypot_blacklist "$ip"
done < /tmp/blacklist.txt

# 4) Drop matching traffic
iptables -I INPUT -m set --match-set honeypot_blacklist src -j DROP

```

------

## Developer usage

### Python SDK

```python
from tools.client import ThreatFeedClient

feed = ThreatFeedClient()
feed.fetch_data()

if feed.is_malicious("1.2.3.4"):
    print("Block this IP")
else:
    print("IP not currently listed")
````

### CLI

```bash
# Download the latest feed
python3 tools/cli.py --update

# Check a single IP
python3 tools/cli.py --check 1.2.3.4

# Export as JSON
python3 tools/cli.py --export json

# Export as TXT
python3 tools/cli.py --export txt
```

### Docker

```bash
docker build -t hfish-feed .
docker run --rm hfish-feed --check 1.1.1.1
```

------

## Integrations

The `integrations/` directory contains platform-specific examples:

| Platform       | Type          | Purpose                                         |
| -------------- | ------------- | ----------------------------------------------- |
| Nginx          | Script        | Generate deny rules for web servers             |
| Linux Firewall | Script        | Use `ipset` + `iptables` for efficient blocking |
| Cloudflare     | Worker        | Edge-side blocking logic                        |
| Palo Alto      | Documentation | External Dynamic List (EDL) integration         |

------

## Build your own feed from HFish

If you run your own HFish deployment, you can reuse this project to generate a private or organization-specific blocklist.

Relevant tooling:

- `tools/generate_feed.py`
- `tools/update_feed.sh`

Reference article:

- **Practical Guide: Building an Automated Threat Intelligence Source Based on HFish + Python + GitHub Pages**

------

## Repository layout

```text
.
├── .github/workflows/       # data quality / automation
├── integrations/            # platform-specific integration examples
├── tools/                   # generator, client SDK, CLI, update scripts
├── tests/                   # tests
├── ip_list.txt              # published threat feed
└── README*.md               # multilingual documentation
```

------

## Project maturity

This repository is maintained as a practical security utility rather than a research-only proof of concept.

Current project signals:

- public repository
- open license
- documented feed semantics
- CLI and SDK access patterns
- integration examples
- automated data quality workflow badge

For production adoption, users should still evaluate:

- enforcement scope
- false-positive handling
- refresh cadence expectations
- rollback strategy
- local allowlist requirements

------

## Reporting false positives

False positives are possible.

If you believe an IP was listed incorrectly, please open an Issue and include:

- the affected IP
- why it should be removed
- relevant supporting evidence
- approximate timestamp if known

This helps improve feed quality over time.

------

## Security

This repository publishes a blocklist and supporting tooling. It is **not** a prevention guarantee, and it should not be treated as a complete threat intelligence solution.

Recommended usage:

- apply as one signal among multiple controls
- combine with local allowlists
- test in monitor mode before hard enforcement
- review impact on shared or dynamic IP ranges

For vulnerability reports related to repository code or automation, please use GitHub Issues unless you prefer a private disclosure path.

------

## Contributing

Contributions are welcome.

Good contribution areas include:

- feed quality improvements
- false-positive reduction
- parser and client improvements
- new integrations
- documentation and translation fixes
- tests and CI hardening

Please open an Issue first for larger changes so design and scope can be discussed before implementation.

------

## Roadmap

Planned or desirable future improvements:

- richer metadata feed formats
- stricter false-positive suppression
- additional firewall / SIEM integrations
- better testing coverage
- feed statistics and transparency reporting

------

## Disclaimer

1. **Accuracy**
   Data is collected and processed automatically. We aim to reduce noise, but compromised hosts, shared infrastructure, or dynamic IPs may still appear.
2. **Use at your own risk**
   You are responsible for evaluating the suitability of this feed before using it in production.
3. **No liability**
   The maintainer is not responsible for service interruption, loss of connectivity, or data loss caused by enforcement decisions based on this feed.

------

## License

Released under the **MIT License**.

------

Powered by [HFish](https://hfish.net/) and Python automation.
