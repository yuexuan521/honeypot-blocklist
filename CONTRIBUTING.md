# Contributing to HFish Threat Feed

First off, thank you for considering contributing to this project! It's people like you that make the open-source community such an amazing place to learn, inspire, and create.

## 🐛 Reporting False Positives (Reporting Innocent IPs)
If you find an IP address in `ip_list.txt` that belongs to a legitimate service (e.g., Google, Cloudflare, or your company VPN), please report it immediately!

1.  **Open an Issue**: Go to the Issues tab.
2.  **Title**: Use `[False Positive] IP 1.2.3.4`.
3.  **Description**: Please provide the IP address and the owner (ASN) if known.
4.  **Action**: We will review and add it to our `whitelist` immediately.

## 🛠️ Contributing Code (Tools & Integrations)
We welcome contributions to our Python SDK (`tools/`) and Integrations (`integrations/`).

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 💡 Suggesting New Features
If you want to suggest a new integration (e.g., support for a specific Firewall), please open an issue with the tag `enhancement`.