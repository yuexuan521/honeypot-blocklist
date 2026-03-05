import requests
import json
import ipaddress
import urllib3
import time
import sys
from datetime import datetime, timedelta

# ================= 配置区 =================
HFISH_HOST = "https://IP:4433"                       #!!填写你的Hish网址!!
API_KEY = ""                                         #!!填写你的Hish API Key!!
OUTPUT_TXT = "/root/threat-feed/ip_list.txt"         #!!填写你保存文件的地址!!
TIME_WINDOW_HOURS = 24 

LOCAL_WHITELIST = [
    "127.0.0.1", "192.168.0.0/16", "10.0.0.0/8", "172.16.0.0/12",
    "8.8.8.8", "1.1.1.1", "60.204.200.232"
]
WHITELIST_URLS = {
    "bing": "https://www.bing.com/toolbox/bingbot.json",
    "github": "https://api.github.com/meta"
}
# =========================================

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WhitelistManager:
    def __init__(self):
        self.whitelist_cidrs = []
        for ip in LOCAL_WHITELIST:
            try:
                self.whitelist_cidrs.append(ipaddress.ip_network(ip, strict=False))
            except: pass

    def fetch_remote_whitelists(self):
        print("[-] Fetching remote whitelists...")
        for name, url in WHITELIST_URLS.items():
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    prefixes = []
                    if "prefixes" in data: prefixes = [p.get("ipv4Prefix") for p in data["prefixes"]]
                    elif "web" in data: prefixes = data.get("web", [])
                    for p in prefixes:
                        if p and "." in p:
                            self.whitelist_cidrs.append(ipaddress.ip_network(p))
            except: pass

    def is_whitelisted(self, ip_str):
        try:
            target = ipaddress.ip_address(ip_str)
            for network in self.whitelist_cidrs:
                if target in network: return True
        except: pass
        return False

def get_data():
    url = f"{HFISH_HOST}/api/v1/attack/ip?api_key={API_KEY}"
    end_time = int(time.time())
    start_time = 0 if TIME_WINDOW_HOURS == 0 else int(end_time - (TIME_WINDOW_HOURS * 3600))
    
    payload = {
        "start_time": start_time,
        "end_time": end_time,
        "intranet": 0,
        "threat_label": []
    }
    
    try:
        resp = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, verify=False, timeout=20)
        return resp.json()
    except Exception as e:
        print(f"[!] Request Error: {e}")
        return None

def main():
    wl = WhitelistManager()
    wl.fetch_remote_whitelists()
    
    result = get_data()
    if not result: return

    raw_ips = []
    
    if 'data' in result:
        data_content = result['data']
        print(f"[-] API Response Keys: {data_content.keys() if isinstance(data_content, dict) else 'List Type'}")
        
        if isinstance(data_content, list):

            raw_ips = data_content
        elif isinstance(data_content, dict):

            if 'attack_ip' in data_content:
                raw_ips = data_content['attack_ip']
            elif 'list' in data_content:
                raw_ips = data_content['list']
            else:
                print("[!] Error: Unknown dict structure in 'data'")
                print(data_content) # 打印出来看看
    else:
        print(f"[!] Error: No 'data' field. keys: {result.keys()}")

    print(f"[-] Raw IPs found: {len(raw_ips)}")


    clean_ips = set()
    for item in raw_ips:
        ip = None

        if isinstance(item, str):
            ip = item

        elif isinstance(item, dict):
            ip = item.get('source_ip') or item.get('ip') or item.get('attack_ip')
            

        if ip and "." in ip and "attack_ip" not in ip:
            if not wl.is_whitelisted(ip):
                clean_ips.add(ip)

    print(f"[-] Final Unique IPs: {len(clean_ips)}")


    with open(OUTPUT_TXT, 'w') as f:
        f.write(f"# HFish Threat Feed\n")
        f.write(f"# Updated: {datetime.now()}\n")
        for ip in clean_ips:
            f.write(f"{ip}\n")
    print(f"[-] Saved to {OUTPUT_TXT}")

if __name__ == "__main__":
    main()