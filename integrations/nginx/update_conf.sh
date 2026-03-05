#!/bin/bash

# 配置：远程列表 URL
LIST_URL="https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt"
# 配置：Nginx 配置文件输出路径 (根据实际情况修改)
OUTPUT_FILE="/etc/nginx/conf.d/blocklist.conf"
TEMP_FILE="/tmp/nginx_blocklist.tmp"

echo "Downloading threat feed..."
# 下载并转换格式：
# 1. grep -v '#' : 去掉注释
# 2. awk : 在每个 IP 前加 'deny '，后加 ';'
curl -s $LIST_URL | grep -v '#' | grep -v '^$' | awk '{print "deny " $1 ";"}' > $TEMP_FILE

# 检查文件是否有内容
if [ -s $TEMP_FILE ]; then
    echo "Updating Nginx configuration..."
    mv $TEMP_FILE $OUTPUT_FILE
    
    # 测试配置并重载
    nginx -t && systemctl reload nginx
    echo "Done! Malicious IPs are now blocked."
else
    echo "Error: Downloaded list is empty."
    rm $TEMP_FILE
fi
