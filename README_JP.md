[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [Français](README_FR.md) | [Español](README_ES.md)

# HFish ハニーポット脅威インテリジェンス フィード

[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yuexuan521/honeypot-blocklist)
[![Source](https://img.shields.io/badge/Source-HFish-blue.svg)](https://hfish.net/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)
[![Data Quality Check](https://github.com/yuexuan521/honeypot-blocklist/actions/workflows/data_quality.yml/badge.svg)](https://github.com/yuexuan521/honeypot-blocklist/actions/workflows/data_quality.yml)

**HFish ハニーポットのテレメトリデータ**をもとに自動生成される、高信頼の悪性 IP フィードです。  
**ファイアウォール / WAF / SIEM / IPSet / EDL** などのセキュリティ運用に利用できます。

このプロジェクトは、インターネット上に公開された HFish ハニーポットが観測した攻撃元 IP を継続的に収集し、自動フィルタリングとホワイトリスト処理を行ったうえで、シンプルかつ自動化しやすい形式で公開します。セキュリティ機器や防御システムにそのまま組み込めることを目的としています。

> **警告**
> このフィードは自動生成です。フィルタリングとホワイトリスト処理を行っていますが、本番環境でブロックを有効化する前に、必ず自組織の環境で評価と検証を行ってください。

---

## このプロジェクトの目的

公開インターネット向けのハニーポットには、ブルートフォース攻撃、脆弱性スキャン、弱い認証情報の試行、自動化された攻撃トラフィックが継続的に到達します。  
本リポジトリの目的は、そうした実際の攻撃観測データを、再利用可能な **防御向け脅威インテリジェンス フィード** として提供することです。

これにより、利用者は以下を実現できます。

- 境界防御で最近の悪性 IP をすばやく遮断する
- SIEM / SOAR に追加の脅威シグナルを提供する
- Linux ファイアウォール、Web サービス、エッジ環境向けのブロックルールを自動生成する
- HFish をもとに独自のプライベート脅威インテリジェンス フィードを構築する

---

## 主な特長

- **24 時間ローリングの悪性 IP フィード**
- **2〜4 時間ごとの自動更新**
- **プレーンテキストの購読 URL**
- **Python SDK と CLI を同梱**
- **Docker に対応**
- **Nginx、Linux Firewall、Cloudflare、Palo Alto 向けの統合例を提供**
- **MIT ライセンスのオープンソース**

---

## フィード URL

以下の URL を、そのままセキュリティ機器・スクリプト・自動化ワークフローに組み込めます。

| 形式 | URL | 用途 |
|---|---|---|
| TXT | `https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt` | Firewall EDL、Linux IPSet、WAF、SIEM エンリッチメント |

---

## フィードの概要

| 項目 | 内容 |
|---|---|
| データソース | HFish Honeypot (V3+) |
| 観測範囲 | 公開インターネット |
| 含まれる挙動 | SSH/RDP ブルートフォース、Web スキャン / 脆弱性悪用、未認可サービス探索 |
| 対象期間 | 過去 24 時間 |
| 更新頻度 | 2〜4 時間ごと |
| データ処理 | 自動クレンジングと基本的なホワイトリスト処理 |
| 主な除外対象 | GoogleBot、BingBot、GitHub サービス、Cloudflare などの既知の正当インフラ（該当する場合） |

---

## なぜ信頼できるのか

このプロジェクトは、**シンプルで、透明性が高く、監査しやすく、自動化に組み込みやすいこと** を重視して設計されています。

- **オープンなデータ形式**：1 行 1 IP のため、確認・解析・統合が容易
- **オープンなツールチェーン**：生成ロジック、クライアント、CLI をリポジトリ内で公開
- **リスク境界を明示**：誤検知の可能性を隠さず明記
- **実運用志向**：デモ用ではなく、実際の防御環境への組み込みを前提に設計

ただし、どのような自動化脅威フィードも完全ではありません。  
共有出口 IP、NAT 環境、侵害済みホスト、動的 IP の再割り当てなどにより、ノイズや誤検知が発生する可能性があります。本番環境では、まず観察と検証を行ったうえで、強制ブロックの適用を判断してください。

---

## 想定ユースケース

このフィードは、以下のような用途に適しています。

- 境界防御で既知の悪性 IP をすばやく遮断する
- 企業向けファイアウォールの **EDL（External Dynamic List）** ソースとして利用する
- **SIEM / SOAR** の脅威インテリジェンス強化に利用する
- **Linux IPSet / iptables** のブロックルールを自動生成する
- **Nginx** の deny 設定を生成する
- **Cloudflare Workers** などのエッジ環境で軽量な遮断ロジックを実装する

---

## クイックスタート

### Linux IPSet + iptables

```bash
# 1) 最新フィードをダウンロード
wget -O /tmp/blacklist.txt https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt

# 2) IPSet を作成
ipset create honeypot_blacklist hash:ip hashsize 4096

# 3) IP を取り込む
while read ip; do
  ipset add honeypot_blacklist "$ip"
done < /tmp/blacklist.txt

# 4) 一致するトラフィックを破棄
iptables -I INPUT -m set --match-set honeypot_blacklist src -j DROP
```

------

## 開発者向け利用方法

### Python SDK

```python
from tools.client import ThreatFeedClient

feed = ThreatFeedClient()
feed.fetch_data()

if feed.is_malicious("1.2.3.4"):
    print("この IP はブロック対象です")
else:
    print("この IP は現在フィードに含まれていません")
```

### CLI

```bash
# ローカルデータを更新
python3 tools/cli.py --update

# IP がフィードに含まれているか確認
python3 tools/cli.py --check 1.2.3.4

# JSON 形式でエクスポート
python3 tools/cli.py --export json

# TXT 形式でエクスポート
python3 tools/cli.py --export txt
```

### Docker

```bash
docker build -t hfish-feed .
docker run --rm hfish-feed --check 1.1.1.1
```

------

## 統合例

`integrations/` ディレクトリには、主要なプラットフォーム向けの統合例が含まれています。

| プラットフォーム | 種別         | 用途                                        |
| ---------------- | ------------ | ------------------------------------------- |
| Nginx            | スクリプト   | Web サーバー向け deny ルール生成            |
| Linux Firewall   | スクリプト   | `ipset` + `iptables` による効率的なブロック |
| Cloudflare       | Worker       | エッジ側でのブロック処理                    |
| Palo Alto        | ドキュメント | External Dynamic List（EDL）連携            |

------

## 独自の HFish フィードを構築する

独自の HFish 環境を運用している場合、このリポジトリのツールチェーンを再利用して、自組織向けのプライベート脅威インテリジェンス フィードを構築できます。

関連ツール：

- `tools/generate_feed.py`
- `tools/update_feed.sh`

参考記事：

- **HFish + Python + GitHub Pages による自動脅威インテリジェンス フィード構築ガイド**

------

## リポジトリ構成

```text
.
├── .github/workflows/       # データ品質チェックと自動化
├── integrations/            # 各種プラットフォーム向け統合例
├── tools/                   # 生成ツール、クライアント SDK、CLI、更新スクリプト
├── tests/                   # テスト
├── ip_list.txt              # 公開フィード
└── README*.md               # 多言語ドキュメント
```

------

## プロジェクト成熟度について

このプロジェクトは、単なるデモではなく、実運用の防御シナリオを意識したセキュリティユーティリティとして管理されています。

現在の成熟度を示す要素：

- 公開リポジトリ
- 明確なオープンソースライセンス
- フィード仕様の文書化
- CLI / SDK の利用方法
- 統合例
- 自動データ品質チェックのワークフロー

本番利用にあたっては、以下をあらかじめ評価することを推奨します。

- 適用するブロック範囲
- 誤検知時の対応手順
- 更新頻度への期待値
- ロールバック方法
- ローカルホワイトリストの必要性

------

## 誤検知の報告

誤検知を完全になくすことはできません。

ある IP が誤ってフィードに含まれていると思われる場合は、Issue を作成し、できるだけ以下の情報を添えてください。

- 対象の IP アドレス
- 誤検知と考える理由
- 根拠となる情報
- わかる場合はおおよその時刻

これらの情報は、フィード品質の継続的な改善に役立ちます。

------

## セキュリティに関する注意

このリポジトリが提供するのは、脅威インテリジェンス フィードと補助ツールです。
**完全な防御を保証するものではなく、唯一のブロック根拠として利用すべきでもありません。**

推奨される利用方法：

- 複数の防御シグナルのひとつとして扱う
- ローカルホワイトリストと併用する
- まず監視モードまたは低リスク環境で検証する
- 共有出口や動的 IP 帯には慎重に適用する

リポジトリのコード、自動化、統合スクリプトに関するセキュリティ上の問題を発見した場合は、まず GitHub Issue で報告してください。機微な内容の場合は、非公開での連絡手段を用意しても構いません。

------

## コントリビューション

コード、ドキュメント、改善提案を歓迎します。

特に歓迎される貢献分野：

- フィード品質の向上
- 誤検知の削減
- パーサー、クライアント、CLI の改善
- 新しい統合例の追加
- ドキュメントや翻訳の修正
- テストと CI の強化

大きな変更については、先に Issue を作成して方針と範囲を議論してから PR を送ることを推奨します。

------

## 今後の予定

今後強化したい項目：

- よりリッチなメタデータ形式の提供
- より厳格な誤検知抑制
- 防火墙 / SIEM 向け統合の拡充
- テストカバレッジの向上
- 統計情報や透明性レポートの追加

------

## 免責事項

1. **正確性について**
   データは自動的に収集・処理されます。ノイズ低減に努めていますが、共有インフラ、動的 IP、侵害済みホストなどにより誤検知が発生する場合があります。
2. **自己責任で利用してください**
   本番環境でブロックを有効化する前に、このフィードが自組織の用途に適しているかを必ず評価してください。
3. **責任の制限**
   このフィードの利用に起因するサービス停止、接続障害、業務影響、データ損失について、メンテナは責任を負いません。

------

## ライセンス

このプロジェクトは **MIT License** のもとで公開されています。

------

[HFish](https://hfish.net/) と Python 自動化によって運用されています。