# 使用 Python 3.8 作为基础镜像
FROM docker-0.unsee.tech/python:3.8.12-slim

# 设置工作目录
WORKDIR /workspace

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app \
    FLASK_ENV=production \
    FLASK_DEBUG=0 \
    ADMIN_USERNAME=admin \
    ADMIN_EMAIL=admin@example.com \
    ADMIN_USERNAME=admin123 \
    MYSQL_HOST=127.0.0.1 \
    MYSQL_PORT=3306 \
    MYSQL_USERNAME=root \
    MYSQL_PASSWORD=123456

# # 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . .

# 安装 Python 依赖（直接从 pyproject.toml）
RUN pip install -e .

# # 健康检查
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD curl -f http://localhost:5000/health || exit 1

# 启动命令
CMD ["/bin/bash", "docker/run.sh"] 
