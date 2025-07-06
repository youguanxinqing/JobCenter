# JobCenter Installation Guide

## 安装方式

### 方式一：使用 pip 安装（推荐）

```bash
# 从当前目录安装
pip install .

# 或者安装开发版本
pip install -e .
```

## 配置环境变量

创建或编辑 `.flaskenv` 文件：

```bash
FLASK_APP=app
FLASK_ENV=development
FLASK_DEBUG=0

# MySQL 配置
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DBNAME=jobs
MYSQL_USERNAME=root
MYSQL_PASSWORD=your_password
```

## 初始化数据库

```bash
# 创建数据库和表
flask init

# 创建管理员账号
flask admin
```

## 运行应用

### 方式一：使用 Flask 命令

```bash
flask run
```

### 方式二：使用 Python 脚本

```bash
python run.py
```

### 方式三：使用安装后的命令

```bash
# 如果使用 pip 安装
jobcenter-run
```

## 环境变量说明

- `FLASK_CONFIG`: 配置环境（development/testing/production）
- `PORT`: 运行端口（默认 5000）
- `FLASK_DEBUG`: 是否开启调试模式（True/False）
- `MYSQL_HOST`: MySQL 主机地址
- `MYSQL_PORT`: MySQL 端口
- `MYSQL_DBNAME`: 数据库名称
- `MYSQL_USERNAME`: MySQL 用户名
- `MYSQL_PASSWORD`: MySQL 密码

## 开发环境设置

```bash
# 安装开发依赖
pip install -e .[dev]

# 运行代码格式化
black .

# 运行代码检查
flake8 .

# 运行类型检查
mypy .
```

## 生产环境部署

1. 设置环境变量为 `production`
2. 确保数据库已正确配置
3. 使用 WSGI 服务器（如 Gunicorn）运行

```bash
export FLASK_CONFIG=production
gunicorn -w 4 -b 0.0.0.0:5000 run:app
``` 
