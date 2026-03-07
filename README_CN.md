[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [Français](README_FR.md) | [Español](README_ES.md)

# HFish 蜜罐威胁情报订阅源

[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yuexuan521/honeypot-blocklist)
[![Source](https://img.shields.io/badge/Source-HFish-blue.svg)](https://hfish.net/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)
[![Data Quality Check](https://github.com/yuexuan521/honeypot-blocklist/actions/workflows/data_quality.yml/badge.svg)](https://github.com/yuexuan521/honeypot-blocklist/actions/workflows/data_quality.yml)

基于 **HFish 蜜罐遥测数据** 自动生成的高可信恶意 IP 订阅源，适用于 **防火墙 / WAF / SIEM / IPSet / EDL** 等安全防护场景。

本项目持续收集部署在公网环境中的 HFish 蜜罐所观测到的攻击源 IP，对数据进行自动过滤和白名单处理，并以简洁、可自动化接入的形式发布，方便安全设备和防御系统直接消费。

> **警告**
> 本订阅源为自动生成。虽然已经进行了过滤和白名单处理，但在生产环境中启用封禁前，仍建议结合自身业务环境进行评估与验证。

---

## 项目背景

面向公网的蜜罐通常会持续收到大量暴力破解、漏洞扫描、弱口令尝试和自动化攻击流量。  
本仓库的目标，是将这些真实攻击观测数据转化为一个可复用的 **防御型威胁情报订阅源**，帮助使用者：

- 在网络边界快速封禁近期恶意来源 IP
- 为 SIEM / SOAR 提供威胁情报补充信号
- 自动生成 Linux 防火墙、Web 服务、边缘代理等环境中的拦截规则
- 基于 HFish 自行搭建和维护私有威胁情报流

---

## 项目特性

- **24 小时滚动恶意 IP 订阅**
- **每 2–4 小时自动更新**
- **纯文本订阅地址，易于集成**
- **内置 Python SDK 与 CLI**
- **支持 Docker 使用**
- **提供 Nginx、Linux Firewall、Cloudflare、Palo Alto 集成示例**
- **MIT 开源许可，便于复用和二次开发**

---

## 订阅地址

你可以直接将以下地址接入安全设备、脚本或自动化流程：

| 格式 | 地址 | 适用场景 |
|---|---|---|
| TXT | `https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt` | 防火墙 EDL、Linux IPSet、WAF、SIEM 情报增强 |

---

## 订阅源说明

| 项目 | 内容 |
|---|---|
| 数据来源 | HFish Honeypot (V3+) |
| 观测范围 | 公网环境 |
| 包含行为 | SSH/RDP 暴力破解、Web 扫描/漏洞利用、未授权服务探测 |
| 时间窗口 | 最近 24 小时 |
| 更新频率 | 每 2–4 小时 |
| 数据处理 | 自动清洗与基础白名单过滤 |
| 常见排除对象 | GoogleBot、BingBot、GitHub 服务、Cloudflare 等已知合法基础设施（在适用情况下） |

---

## 为什么值得信任

这个项目的设计目标是：**简单、透明、可审计、适合自动化接入**。

- **开放的数据格式**：每行一个 IP，便于审查、解析与集成
- **开放的工具链**：生成逻辑、客户端、CLI 都在仓库中公开
- **明确的风险边界**：公开说明误报可能性，而不是夸大准确率
- **面向实战场景**：重点是可接入实际防护系统，而不是只做演示用途

当然，任何自动化威胁情报源都无法做到绝对准确。  
共享出口、NAT 网络、被入侵主机、动态 IP 重新分配等情况，都可能带来噪声或误报。因此在生产环境中，建议先进行观察和验证，再决定是否启用强制封禁。

---

## 适用场景

本订阅源适合以下用途：

- 在网络边界快速拦截已知恶意来源 IP
- 作为企业防火墙 **EDL（External Dynamic List）** 的输入源
- 作为 **SIEM / SOAR** 的威胁情报增强数据
- 自动生成 **Linux IPSet / iptables** 拦截规则
- 为 **Nginx** 生成拒绝访问配置
- 在 **Cloudflare Workers** 等边缘平台实现轻量级封禁逻辑

---

## 快速开始

### Linux IPSet + iptables

```bash
# 1) 下载最新订阅源
wget -O /tmp/blacklist.txt https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt

# 2) 创建 IPSet
ipset create honeypot_blacklist hash:ip hashsize 4096

# 3) 导入 IP
while read ip; do
  ipset add honeypot_blacklist "$ip"
done < /tmp/blacklist.txt

# 4) 丢弃匹配流量
iptables -I INPUT -m set --match-set honeypot_blacklist src -j DROP
```

------

## 开发者使用方式

### Python SDK

```python
from tools.client import ThreatFeedClient

feed = ThreatFeedClient()
feed.fetch_data()

if feed.is_malicious("1.2.3.4"):
    print("建议封禁该 IP")
else:
    print("该 IP 当前未命中订阅源")
```

### CLI

```bash
# 更新本地数据
python3 tools/cli.py --update

# 检查某个 IP 是否在订阅源中
python3 tools/cli.py --check 1.2.3.4

# 导出为 JSON
python3 tools/cli.py --export json

# 导出为 TXT
python3 tools/cli.py --export txt
```

### Docker

```bash
docker build -t hfish-feed .
docker run --rm hfish-feed --check 1.1.1.1
```

------

## 集成示例

`integrations/` 目录中提供了常见平台的接入示例：

| 平台           | 类型   | 用途                               |
| -------------- | ------ | ---------------------------------- |
| Nginx          | 脚本   | 生成 Web 服务拒绝规则              |
| Linux Firewall | 脚本   | 使用 `ipset` + `iptables` 高效封禁 |
| Cloudflare     | Worker | 在边缘侧执行封禁逻辑               |
| Palo Alto      | 文档   | 对接 External Dynamic List（EDL）  |

------

## 使用你自己的 HFish 构建私有订阅源

如果你已经部署了自己的 HFish 蜜罐环境，也可以复用本项目中的工具链，生成属于你自己组织或环境的私有威胁情报订阅源。

相关工具包括：

- `tools/generate_feed.py`
- `tools/update_feed.sh`

参考文章：

- **基于 HFish + Python + GitHub Pages 搭建自动化威胁情报源实践指南**

------

## 仓库结构

```text
.
├── .github/workflows/       # 数据质量检查与自动化流程
├── integrations/            # 各平台集成示例
├── tools/                   # 生成工具、客户端 SDK、CLI、更新脚本
├── tests/                   # 测试代码
├── ip_list.txt              # 发布的威胁情报订阅源
└── README*.md               # 多语言文档
```

------

## 项目成熟度说明

这是一个面向实际防御场景维护的安全工具项目，而不是单纯的演示仓库。

当前已具备的项目成熟度信号包括：

- 公开可访问的仓库
- 明确的开源许可证
- 清晰的订阅语义说明
- CLI 与 SDK 使用方式
- 集成示例
- 自动化数据质量检查流程

如果要在生产环境中正式采用，仍建议结合自身情况重点评估：

- 封禁范围是否合适
- 误报处理机制是否完善
- 更新频率是否满足要求
- 是否具备回滚方案
- 是否需要本地白名单

------

## 误报申诉

误报无法完全避免。

如果你认为某个 IP 被错误加入了订阅源，欢迎提交 Issue，并尽量提供以下信息：

- 相关 IP 地址
- 申诉理由
- 支撑证据
- 如已知，请提供大致时间点

这些信息有助于持续改进订阅源质量。

------

## 安全说明

本仓库发布的是一个威胁情报订阅源及其辅助工具，**并不构成完整防护能力，也不应被视为唯一封禁依据**。

推荐使用方式：

- 将其作为多种检测与防护信号之一
- 结合本地白名单机制使用
- 先在观察模式或低风险范围内验证
- 对共享出口、动态 IP 段保持谨慎

如果你发现的是仓库代码、自动化流程或集成脚本中的安全问题，建议优先通过 GitHub Issue 报告；若涉及敏感问题，也可选择私下联系维护者。

------

## 贡献指南

欢迎贡献代码、文档和改进建议。

适合贡献的方向包括：

- 提高订阅源质量
- 降低误报率
- 改进解析器、客户端和 CLI
- 增加新的平台集成
- 修正文档与翻译
- 增加测试覆盖和 CI 能力

对于较大的功能变更，建议先提交 Issue 讨论方案与范围，再发起 PR。

------

## 未来计划

后续可持续增强的方向包括：

- 提供更丰富的元数据格式
- 更严格的误报抑制机制
- 增加更多防火墙 / SIEM 集成
- 提升测试覆盖率
- 增加统计信息与透明度说明

------

## 免责声明

1. **准确性说明**
   数据由自动化流程采集和处理。我们会尽量减少噪声，但共享基础设施、动态 IP、被入侵主机等情况仍可能导致误报。
2. **使用风险自负**
   在生产环境中启用封禁前，请自行评估该订阅源是否适合你的业务场景。
3. **免责说明**
   因使用本订阅源而导致的服务中断、连接受阻、业务影响或数据损失，维护者不承担责任。

------

## 许可证

本项目基于 **MIT License** 开源。

------

由 [HFish](https://hfish.net/) 与 Python 自动化驱动。