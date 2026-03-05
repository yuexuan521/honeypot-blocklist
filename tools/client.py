import requests
import logging

class ThreatFeedClient:
    """
    HFish Threat Feed SDK
    用于程序化获取和查询威胁情报数据的客户端
    """
    
    # 默认使用 GitHub Pages 加速地址
    DEFAULT_URL = "https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt"

    def __init__(self, url=None):
        self.url = url if url else self.DEFAULT_URL
        self.ips = set()
        self.logger = logging.getLogger("ThreatFeed")

    def fetch_data(self):
        """从远程源下载最新 IP 列表"""
        try:
            self.logger.info(f"Fetching data from {self.url}...")
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            
            # 清洗数据：去除空行和注释
            lines = response.text.splitlines()
            self.ips = {line.strip() for line in lines if line.strip() and not line.startswith('#')}
            
            self.logger.info(f"Successfully loaded {len(self.ips)} IPs.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to fetch data: {e}")
            return False

    def is_malicious(self, ip_address):
        """检查指定 IP 是否在黑名单中"""
        if not self.ips:
            # 如果缓存为空，尝试自动下载
            self.fetch_data()
        
        return ip_address in self.ips

    def get_all_ips(self):
        """获取所有恶意 IP 列表"""
        if not self.ips:
            self.fetch_data()
        return list(self.ips)

    def export_to_json(self):
        """导出为 JSON 格式"""
        return {
            "source": "HFish Honeypot Feed",
            "count": len(self.ips),
            "ips": list(self.ips)
        }
