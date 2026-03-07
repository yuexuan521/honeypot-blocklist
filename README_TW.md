[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [Français](README_FR.md) | [Español](README_ES.md)

# HFish 蜜罐威脅情報訂閱源

[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yuexuan521/honeypot-blocklist)
[![Source](https://img.shields.io/badge/Source-HFish-blue.svg)](https://hfish.net/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)
[![Data Quality Check](https://github.com/yuexuan521/honeypot-blocklist/actions/workflows/data_quality.yml/badge.svg)](https://github.com/yuexuan521/honeypot-blocklist/actions/workflows/data_quality.yml)

基於 **HFish 蜜罐遙測資料** 自動生成的高可信惡意 IP 訂閱源，適用於 **防火牆 / WAF / SIEM / IPSet / EDL** 等安全防護場景。

本專案持續收集部署於公開網際網路環境中的 HFish 蜜罐所觀測到的攻擊來源 IP，對資料進行自動過濾與白名單處理，並以簡潔、易於自動化接入的形式發布，方便安全設備與防禦系統直接使用。

> **警告**
> 本訂閱源為自動生成。雖然已進行過濾與白名單處理，但在正式套用到生產環境前，仍建議結合自身業務環境進行評估與驗證。

---

## 專案背景

面向公開網際網路的蜜罐通常會持續接收到大量暴力破解、漏洞掃描、弱密碼嘗試與自動化攻擊流量。  
本倉庫的目標，是將這些真實攻擊觀測資料轉化為一個可重複使用的 **防禦型威脅情報訂閱源**，協助使用者：

- 在網路邊界快速封鎖近期惡意來源 IP
- 為 SIEM / SOAR 提供威脅情報補充訊號
- 自動生成 Linux 防火牆、Web 服務與邊緣代理等環境中的攔截規則
- 基於 HFish 自行建置與維護私有威脅情報流

---

## 專案特性

- **24 小時滾動惡意 IP 訂閱**
- **每 2–4 小時自動更新**
- **純文字訂閱位址，易於整合**
- **內建 Python SDK 與 CLI**
- **支援 Docker 使用**
- **提供 Nginx、Linux Firewall、Cloudflare、Palo Alto 整合範例**
- **MIT 開源授權，便於重用與二次開發**

---

## 訂閱位址

你可以直接將以下位址接入安全設備、腳本或自動化流程：

| 格式 | 位址 | 適用場景 |
|---|---|---|
| TXT | `https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt` | 防火牆 EDL、Linux IPSet、WAF、SIEM 情報增強 |

---

## 訂閱源說明

| 項目 | 內容 |
|---|---|
| 資料來源 | HFish Honeypot (V3+) |
| 觀測範圍 | 公開網際網路環境 |
| 包含行為 | SSH/RDP 暴力破解、Web 掃描/漏洞利用、未授權服務探測 |
| 時間視窗 | 最近 24 小時 |
| 更新頻率 | 每 2–4 小時 |
| 資料處理 | 自動清洗與基礎白名單過濾 |
| 常見排除對象 | GoogleBot、BingBot、GitHub 服務、Cloudflare 等已知合法基礎設施（在適用情況下） |

---

## 為什麼值得信任

本專案的設計目標是：**簡單、透明、可審計、適合自動化接入**。

- **開放的資料格式**：每行一個 IP，方便審查、解析與整合
- **開放的工具鏈**：生成邏輯、客戶端與 CLI 均在倉庫中公開
- **明確的風險邊界**：公開說明誤報可能性，而非誇大準確率
- **面向實戰場景**：重點在於可直接接入實際防護系統，而不只是示範用途

當然，任何自動化威脅情報源都無法做到絕對準確。  
共享出口、NAT 網路、已遭入侵主機、動態 IP 重新分配等情況，都可能帶來雜訊或誤報。因此在生產環境中，建議先觀察與驗證，再決定是否啟用強制封鎖。

---

## 適用場景

本訂閱源適合以下用途：

- 在網路邊界快速攔截已知惡意來源 IP
- 作為企業防火牆 **EDL（External Dynamic List）** 的輸入來源
- 作為 **SIEM / SOAR** 的威脅情報增強資料
- 自動生成 **Linux IPSet / iptables** 攔截規則
- 為 **Nginx** 生成拒絕存取設定
- 在 **Cloudflare Workers** 等邊緣平台實作輕量級封鎖邏輯

---

## 快速開始

### Linux IPSet + iptables

```bash
# 1) 下載最新訂閱源
wget -O /tmp/blacklist.txt https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt

# 2) 建立 IPSet
ipset create honeypot_blacklist hash:ip hashsize 4096

# 3) 匯入 IP
while read ip; do
  ipset add honeypot_blacklist "$ip"
done < /tmp/blacklist.txt

# 4) 丟棄符合的流量
iptables -I INPUT -m set --match-set honeypot_blacklist src -j DROP
```

------

## 開發者使用方式

### Python SDK

```python
from tools.client import ThreatFeedClient

feed = ThreatFeedClient()
feed.fetch_data()

if feed.is_malicious("1.2.3.4"):
    print("建議封鎖該 IP")
else:
    print("該 IP 目前未命中訂閱源")
```

### CLI

```bash
# 更新本地資料
python3 tools/cli.py --update

# 檢查某個 IP 是否在訂閱源中
python3 tools/cli.py --check 1.2.3.4

# 匯出為 JSON
python3 tools/cli.py --export json

# 匯出為 TXT
python3 tools/cli.py --export txt
```

### Docker

```bash
docker build -t hfish-feed .
docker run --rm hfish-feed --check 1.1.1.1
```

------

## 整合範例

`integrations/` 目錄中提供了常見平台的接入範例：

| 平台           | 類型   | 用途                               |
| -------------- | ------ | ---------------------------------- |
| Nginx          | 腳本   | 生成 Web 服務拒絕規則              |
| Linux Firewall | 腳本   | 使用 `ipset` + `iptables` 高效封鎖 |
| Cloudflare     | Worker | 在邊緣側執行封鎖邏輯               |
| Palo Alto      | 文件   | 對接 External Dynamic List（EDL）  |

------

## 使用你自己的 HFish 建立私有訂閱源

如果你已部署自己的 HFish 蜜罐環境，也可以重用本專案中的工具鏈，生成屬於你自己組織或環境的私有威脅情報訂閱源。

相關工具包括：

- `tools/generate_feed.py`
- `tools/update_feed.sh`

參考文章：

- **基於 HFish + Python + GitHub Pages 搭建自動化威脅情報源實踐指南**

------

## 倉庫結構

```text
.
├── .github/workflows/       # 資料品質檢查與自動化流程
├── integrations/            # 各平台整合範例
├── tools/                   # 生成工具、客戶端 SDK、CLI、更新腳本
├── tests/                   # 測試程式
├── ip_list.txt              # 發布的威脅情報訂閱源
└── README*.md               # 多語言文件
```

------

## 專案成熟度說明

這是一個面向實際防禦場景維護的安全工具專案，而非單純的展示型倉庫。

目前已具備的成熟度訊號包括：

- 公開可存取的倉庫
- 明確的開源授權
- 清楚的訂閱語義說明
- CLI 與 SDK 使用方式
- 整合範例
- 自動化資料品質檢查流程

若要在生產環境中正式採用，仍建議結合自身情況重點評估：

- 封鎖範圍是否合適
- 誤報處理機制是否完善
- 更新頻率是否符合需求
- 是否具備回滾方案
- 是否需要本地白名單

------

## 誤報申訴

誤報無法完全避免。

如果你認為某個 IP 被錯誤加入訂閱源，歡迎提交 Issue，並盡量提供以下資訊：

- 相關 IP 位址
- 申訴理由
- 支撐證據
- 如已知，請提供大致時間點

這些資訊有助於持續改善訂閱源品質。

------

## 安全說明

本倉庫發布的是一個威脅情報訂閱源及其輔助工具，**並不構成完整防護能力，也不應被視為唯一封鎖依據**。

建議使用方式：

- 將其作為多種信號之一
- 結合本地白名單機制使用
- 先在觀察模式或低風險範圍內驗證
- 對共享出口與動態 IP 網段保持審慎

如果你發現的是倉庫程式碼、自動化流程或整合腳本中的安全問題，建議優先透過 GitHub Issue 回報；若涉及敏感問題，也可選擇私下聯絡維護者。

------

## 貢獻指南

歡迎貢獻程式碼、文件與改進建議。

適合貢獻的方向包括：

- 提高訂閱源品質
- 降低誤報率
- 改進解析器、客戶端與 CLI
- 新增更多平台整合
- 修正文檔與翻譯
- 增加測試覆蓋與 CI 能力

對於較大的功能變更，建議先提交 Issue 討論方案與範圍，再發起 PR。

------

## 未來規劃

後續可持續增強的方向包括：

- 提供更豐富的中繼資料格式
- 更嚴格的誤報抑制機制
- 增加更多防火牆 / SIEM 整合
- 提升測試覆蓋率
- 增加統計資訊與透明度說明

------

## 免責聲明

1. **準確性說明**
   資料由自動化流程蒐集與處理。我們會盡量降低雜訊，但共享基礎設施、動態 IP、已遭入侵主機等情況仍可能導致誤報。
2. **使用風險自負**
   在生產環境中啟用封鎖前，請自行評估該訂閱源是否適合你的業務場景。
3. **免責說明**
   因使用本訂閱源而導致的服務中斷、連線受阻、業務影響或資料損失，維護者不承擔責任。

------

## 授權

本專案基於 **MIT License** 開源。

------

由 [HFish](https://hfish.net/) 與 Python 自動化驅動。
