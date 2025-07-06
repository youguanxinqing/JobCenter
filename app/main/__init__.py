# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: __init__.py
# @Date:   2019-03-07 18:27:51
# @Last Modified by:   guomaoqiu
# @Last Modified time: 2019-03-21 11:58:58

from flask import Blueprint

main = Blueprint("main", __name__)

from ..models import Permission
from . import errors, views


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
