# 使用轻量级 Python 镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制工具代码
COPY tools/ /app/tools/

# 安装依赖
RUN pip install --no-cache-dir -r tools/requirements.txt

# 设置环境变量
ENV PYTHONPATH=/app

# 默认入口：运行 CLI 工具的帮助界面
ENTRYPOINT ["python", "tools/cli.py"]
