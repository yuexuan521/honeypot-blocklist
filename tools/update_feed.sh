#!/bin/bash

# ================= 配置路径 =================
PY_SCRIPT="/root/generate_feed.py"
GIT_REPO="/root/threat-feed"
LOG_FILE="/var/log/hfish_feed.log"
# ===========================================

echo "-----------------------------------------------------" >> $LOG_FILE
echo "[$(date)] Starting update process..." >> $LOG_FILE

# 1. 进入 Git 仓库目录 (这一步必须最先做)
cd $GIT_REPO || { echo "[Error] Cannot cd into $GIT_REPO" >> $LOG_FILE; exit 1; }

# 2. 【新增】先拉取远程更新 (防止 Push 冲突)
# 这一步会把你在 GitHub 网页上改的 README 同步到本地
echo "[-] Pulling remote changes..." >> $LOG_FILE
if git pull origin main >> $LOG_FILE 2>&1; then
    echo "[Info] Git pull successful." >> $LOG_FILE
else
    # 如果 pull 失败（极少见），通常是因为冲突，记录日志但不退出，尝试强制覆盖
    echo "[Warn] Git pull failed (Conflict?). Will try to push anyway." >> $LOG_FILE
fi

# 3. 执行 Python 提取 IP
# 注意：即使 git pull 失败了，我们也要生成新数据，因为数据才是核心
/usr/bin/python3 $PY_SCRIPT >> $LOG_FILE 2>&1

# 4. 检查文件是否生成
if [ ! -f "ip_list.txt" ]; then
    echo "[Error] ip_list.txt missing. Python script failed?" >> $LOG_FILE
    exit 1
fi

# 5. 配置 Git 身份
git config user.name ""                          //!!填写你的name和email!!
git config user.email ""

# 6. 提交并推送
git add .

if git commit -m "Auto update: $(date "+%Y-%m-%d %H:%M")" >> $LOG_FILE 2>&1; then
    echo "[Info] Changes committed." >> $LOG_FILE
    
    # 尝试推送
    if git push origin main >> $LOG_FILE 2>&1; then
         echo "[Success] Pushed to GitHub." >> $LOG_FILE
    else
         echo "[Error] Git Push failed. Retrying with --force..." >> $LOG_FILE
         # 如果普通推送失败，尝试强制推送 (慎用，但在这种只增不减的情报源场景下是可行的)
         # git push -f origin main >> $LOG_FILE 2>&1
    fi
else
    echo "[Info] No changes detected. Nothing to push." >> $LOG_FILE
fi