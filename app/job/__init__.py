# 注册蓝本 必须用下列顺序 避免陷入循环依赖
from flask import Blueprint

job = Blueprint("job", __name__)

from app.job import core, views # pylint:disable=broad-except
