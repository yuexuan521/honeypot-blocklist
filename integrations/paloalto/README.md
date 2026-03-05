# Palo Alto Networks (PAN-OS) Integration

This threat feed is compatible with Palo Alto Networks **External Dynamic List (EDL)**.

## Configuration Steps

1. **Log in** to your PAN-OS Web Interface.
2. Navigate to **Objects** > **External Dynamic Lists**.
3. Click **Add** and configure:
   * **Name**: `HFish-Blocklist`
   * **Type**: `IP List`
   * **Source**: `https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt`
   * **Repeat**: `Hourly`
4. Commit changes.
5. Use this object (`HFish-Blocklist`) in your **Security Policies** with action **Deny**.