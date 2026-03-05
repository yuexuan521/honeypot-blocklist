# Nginx Integration

This script automatically downloads the threat feed, converts it to Nginx `deny` syntax, and reloads the server.

## Usage
1. Edit `update_conf.sh` to set your Nginx config path.
2. Run the script via cron every 4 hours:
   ```bash
   0 */4 * * * /bin/bash /path/to/integrations/nginx/update_conf.sh
   ```
3. Include the config in your nginx.conf:
   ```Nginx
   http {
       include /etc/nginx/conf.d/blocklist.conf;
   }
   ```
