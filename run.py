#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JobCenter Application Entry Point
"""

import os

from app import create_app

app = create_app()


def main():
    """Main function to run the application."""
    # 从环境变量获取配置，默认为 development
    config_name = os.getenv("FLASK_CONFIG", "development")
    app_instance = create_app(config_name)

    # 从环境变量获取端口，默认为 5000
    port = int(os.getenv("PORT", 5000))

    # 从环境变量获取是否开启调试模式，默认为 False
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    print(f"Starting JobCenter on port {port} with config: {config_name}")
    print(f"Debug mode: {debug}")

    app_instance.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
