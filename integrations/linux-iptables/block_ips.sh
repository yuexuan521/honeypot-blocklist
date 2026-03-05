#!/bin/bash

# 创建名为 'threat_feed' 的 IP 集合
ipset create threat_feed hash:ip hashsize 4096 -exist

# 下载并导入
curl -s "https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt" | \
grep -v "#" | grep -v "^$" | while read ip; do
  ipset add threat_feed $ip -exist
done

# 添加 iptables 规则 (如果没有的话)
iptables -C INPUT -m set --match-set threat_feed src -j DROP 2>/dev/null
if [ $? -ne 0 ]; then
  iptables -I INPUT -m set --match-set threat_feed src -j DROP
fi

echo "Firewall updated. Current blocked IPs: $(ipset list threat_feed | wc -l)"
