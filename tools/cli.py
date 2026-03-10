import argparse
import sys
import json
from .client import ThreatFeedClient

def main():
    parser = argparse.ArgumentParser(description="HFish Threat Feed CLI Tool")
    
    # 定义命令参数
    parser.add_argument("--update", action="store_true", help="Download latest threat data")
    parser.add_argument("--check", type=str, help="Check if a specific IP is malicious")
    parser.add_argument("--export", type=str, choices=['json', 'txt'], help="Export data to format")
    
    args = parser.parse_args()
    
    # 初始化客户端
    client = ThreatFeedClient()
    
    # 如果没有参数，打印帮助
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # 执行逻辑
    if args.update or args.check or args.export:
        success = client.fetch_data()
        if not success:
            print("Error: Could not fetch data.")
            sys.exit(1)

    if args.check:
        ip = args.check
        if client.is_malicious(ip):
            print(f"❌ DANGER: IP {ip} is in the blocklist!")
            sys.exit(1) # 返回非0状态码，方便脚本集成
        else:
            print(f"✅ SAFE: IP {ip} is not currently listed.")
            sys.exit(0)

    if args.export == 'json':
        print(json.dumps(client.export_to_json(), indent=2))
    elif args.export == 'txt':
        for ip in client.get_all_ips():
            print(ip)

if __name__ == "__main__":
    main()
