import logging
import os

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

basedir = os.path.abspath(os.path.dirname(__file__))

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

FLASK_ENV = os.getenv("FLASK_ENV", "development")


# MySQL配置
MYSQL_INFO = {
    "host": os.environ.get("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.environ.get("MYSQL_PORT", 3306)),
    "dbname": os.environ.get("MYSQL_DBNAME", "jobs"),
    "username": os.environ.get("MYSQL_USERNAME"),
    "password": os.environ.get("MYSQL_PASSWORD"),
}

MYSQL_URL = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (
    MYSQL_INFO["username"],
    MYSQL_INFO["password"],
    MYSQL_INFO["host"],
    MYSQL_INFO["port"],
    MYSQL_INFO["dbname"],
)


# apscheduler 配置
class TaskConfig:

    JOBS = []
    SCHEDULER_JOBSTORES = {"default": SQLAlchemyJobStore(url=MYSQL_URL)}
    SCHEDULER_EXECUTORS = {"default": {"type": "threadpool", "max_workers": 10}}
    SCHEDULER_JOB_DEFAULTS = {
        "coalesce": False,
        "max_instances": 5,
        "misfire_grace_time": 15,  # 任务错过执行时间的宽限时间（秒）
    }
    SCHEDULER_API_ENABLED = False

    # 任务日志
    log = logging.getLogger("apscheduler.executors.default")
    log.setLevel(logging.DEBUG)  # DEBUG
    fmt = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
    h = logging.StreamHandler()
    h = logging.FileHandler("/tmp/task_scheduler.log")

    h.setFormatter(fmt)
    log.addHandler(h)


class Config:
    """基本配置"""

    SQLALCHEMY_ECHO = False  # 用于显式地禁用或启用查询记录
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY = os.environ.get("SECRET_KEY") or "A0Zr98j/3yXR~XHH!jmN]LWX/,?RT"
    # SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    BABEL_DEFAULT_LOCALE = "zh"
    # 公司邮箱域名后缀，限制只能公司域名才能注册
    COMPANY_MAIL_SUFFIX = "sctux.com"
    # 用户注册功能开关: True:可注册；False: 关闭注册
    REGISTER = False

    # 邮件信息
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = ADMIN_USERNAME
    MAIL_PASSWORD = ADMIN_PASSWORD
    FLASKY_MAIL_SUBJECT_PREFIX = "[TaskServices]"
    FLASKY_MAIL_SENDER = ADMIN_EMAIL
    FLASKY_ADMIN = ADMIN_EMAIL

    # 加密解密所需的key
    PRPCRYPTO_KEY = "2d4g53sdfs6L6K"

    # 配置类可以定义 init_app() 类方法，其参数是程序实例。
    # 在这个方法中，可以执行对当前 环境的配置初始化。
    # 现在，基类 Config 中的 init_app() 方法为空。
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    FORMAT:
        'mysql+pymysql://' + db_user + ':' + db_pass + '@' + db_host + '/' + db_name
        + '?charset=utf8mb4'
    """

    SQLALCHEMY_DATABASE_URI = MYSQL_URL


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = MYSQL_URL


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
