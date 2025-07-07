.PHONY: help install install-dev fmt clean run run-flask init-project docker-build docker-run

help: ## 显示帮助信息
	@echo "可用的命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## 安装项目依赖
	pip install -e .

install-dev: ## 安装开发依赖
	pip install -e .[dev]

fmt: ## 格式化代码 (black + isort)
	black .
	isort .
	ruff check --fix .

clean: ## 清理临时文件
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/

run: ## 运行应用
	flask run

dev: ## 开发模式运行引用
	flask run --host 127.0.0.1 --port 9091

init-project: ## 初始化项目
	flask initdb
	flask admin

docker-build: ## 构建docker镜像
	docker build -f ./docker/Dockerfile -t youguanxinqing/newjobcenter:latest .

docker-run: ## 运行docker镜像
	docker run --privileged=true -v /etc/localtime:/etc/localtime:ro --net host -itd newjobcenter
