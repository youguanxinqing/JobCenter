import os

import click
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from app.auth import auth as auth_blueprint
from app.config import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    FLASK_ENV,
    MYSQL_INFO,
    TaskConfig,
    config,
)
from app.extensions import bootstrap, db, login_manager, mail, moment, scheduler
from app.job import job as job_blueprint
from app.main import main as main_blueprint
from app.models import Role, User


def create_app(config_name=None):
    config_name = config_name or FLASK_ENV

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "xxxxxxxxx"

    app.debug = False
    toolbar = DebugToolbarExtension()
    toolbar.init_app(app)

    # 配置引入
    app.config.from_object(config[config_name])
    app.config.from_object(TaskConfig())
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

    # 注册扩展
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    # 创建 database
    create_database(app)

    # 延迟启动apscheduler服务
    scheduler.start()

    # apscheduler api认证
    @scheduler.authenticate
    def authenticate(auth):
        return auth["username"] == "guest" and auth["password"] == "guest"

    return app


def create_database(app):
    """Create database if it doesn't exist."""
    import pymysql

    # 连接到MySQL服务器（不指定数据库）
    connection = pymysql.connect(
        host=MYSQL_INFO["host"],
        port=MYSQL_INFO["port"],
        user=MYSQL_INFO["username"],
        password=MYSQL_INFO["password"],
        charset="utf8",
    )

    with connection.cursor() as cursor:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS "
            f"`{MYSQL_INFO['dbname']}` CHARACTER SET utf8 COLLATE utf8_general_ci"
        )
    connection.close()


# 注册扩展
def register_extensions(app):
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    scheduler.init_app(app)
    db.init_app(app)


# 注册蓝图
def register_blueprints(app):
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(job_blueprint, url_prefix="/v1/cron/job")


# 注册命令
def register_commands(app):
    @app.cli.command()
    @click.option("--drop", is_flag=True, help="Create after drop.")
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm(
                "This operation will delete the database, do you want to continue?",
                abort=True,
            )
            db.drop_all()
            click.echo("Drop tables.")

        db.create_all()
        click.echo("Initialized database.")

    @app.cli.command()
    def init():
        """Initialize Albumy."""
        click.echo("Initializing the database...")
        db.create_all()

        # click.echo('Initializing the roles and permissions...')
        Role.insert_roles()
        click.echo("Done.")

    @app.cli.command()
    def admin():
        """Create default admin account using environment variables."""
        click.echo("Creating default admin account...")

        # 确保角色已创建
        Role.insert_roles()

        # 从配置中获取默认管理员邮箱
        admin_email = ADMIN_EMAIL
        admin_username = ADMIN_USERNAME
        admin_password = ADMIN_PASSWORD  # 默认密码，建议首次登录后修改

        # 检查用户是否已存在
        if User.query.filter_by(email=admin_email).first():
            click.echo(f"Admin user with email {admin_email} already exists.")
            return

        if User.query.filter_by(username=admin_username).first():
            click.echo(f"Admin user with username {admin_username} already exists.")
            return

        # 创建管理员用户
        admin_role = Role.query.filter_by(name="Administrator").first()
        if not admin_role:
            click.echo('Administrator role not found. Please run "flask init" first.')
            return

        user = User(
            username=admin_username, email=admin_email, role=admin_role, confirmed=True
        )
        user.password = admin_password

        db.session.add(user)
        db.session.commit()

        click.echo("Default admin account created successfully!")
        click.echo(f"Username: {admin_username}")
        click.echo(f"Email: {admin_email}")
        click.echo(f"Password: {admin_password}")
        click.echo("Please change the password after first login!")
        click.echo("Done.")
