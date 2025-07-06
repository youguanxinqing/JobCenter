.PHONY: help install install-dev format clean run run-flask init-project

help: ## 显示帮助信息
	@echo "可用的命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## 安装项目依赖
	pip install -e .

install-dev: ## 安装开发依赖
	pip install -e .[dev]

format: ## 格式化代码 (black + isort)
	black .
	isort .
	flake8 .

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

init-project: ## 初始化项目
	flask initdb
	flask admin
