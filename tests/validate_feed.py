import ipaddress
import sys
import os

# 配置文件路径
FILE_PATH = 'ip_list.txt'

# 绝对禁止出现的 IP (白名单兜底)
CRITICAL_WHITELIST = [
    '127.0.0.1', '0.0.0.0', '8.8.8.8', '1.1.1.1'
]

def validate_file():
    print(f"🔍 Starting validation for {FILE_PATH}...")
    
    # 1. 检查文件是否存在
    if not os.path.exists(FILE_PATH):
        print("❌ Error: File not found!")
        sys.exit(1)

    # 2. 检查文件是否为空
    if os.path.getsize(FILE_PATH) == 0:
        print("❌ Error: File is empty!")
        sys.exit(1)

    with open(FILE_PATH, 'r') as f:
        lines = f.readlines()

    valid_count = 0
    error_count = 0

    print(f"📊 Analyzing {len(lines)} lines...")

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        
        # 跳过注释和空行
        if not line or line.startswith('#'):
            continue

        try:
            ip = ipaddress.ip_address(line)
            
            # 3. 检查是否是私有 IP (如 192.168.x.x)
            if ip.is_private:
                print(f"❌ Error at line {line_num}: {line} is a PRIVATE IP! (Risk of blocking local network)")
                error_count += 1
            
            # 4. 检查是否在关键白名单中
            if str(ip) in CRITICAL_WHITELIST:
                print(f"❌ Error at line {line_num}: {line} is in CRITICAL WHITELIST!")
                error_count += 1
            
            # 5. 检查是否是多播/保留地址
            if ip.is_multicast or ip.is_reserved:
                 print(f"❌ Error at line {line_num}: {line} is Reserved/Multicast.")
                 error_count += 1

            valid_count += 1

        except ValueError:
            print(f"❌ Error at line {line_num}: '{line}' is not a valid IP address.")
            error_count += 1

    if error_count > 0:
        print(f"\n🚨 Validation FAILED with {error_count} errors.")
        sys.exit(1) # 返回错误代码，GitHub Actions 会判定为失败
    else:
        print(f"\n✅ Validation PASSED. {valid_count} valid IPs ready for distribution.")
        sys.exit(0)

if __name__ == "__main__":
    validate_file()
