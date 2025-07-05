# -*- coding: utf-8 -*-
# Author: guomaoqiu
# Date: 2020-2-28
# Desc: 钉钉通知


import os
import sys
import json
import datetime
import requests, time

# 依赖包: pip install flask gitpython
from flask import Flask, request, jsonify, abort


def dingding(dingding_send_info):
    # dingding_send_info = {
    #     "address": request.headers.get('X-Forwarded-For',request.remote_addr) ,
    #     "agent": str(request.user_agent),
    #     "title": u'😝点点滴滴😝'

    # }
    ##
    ## 告警测试
    print("*** 发送钉钉 *** ")
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=3fbfe5dff3c6e5002d908b96c20f654256a4ff916aec169fc2ea79e683335b14"

    ## 定义接受信息的人和信息内容
    user = "15928461018"
    ## 组装内容
    data = {
        "msgtype": "markdown",
        "markdown": {
            # "title":"MSG"
            "title": "" + dingding_send_info["title"],
            "text": ""
            + dingding_send_info["title"]
            + "\n\n"
            + "> AccessIP: "
            + dingding_send_info["address"]
            + "\n\n"
            + "> Time: "
            + time.strftime("%Y-%m-%d %H:%M:%S")
            + "\n\n"
            + "> Target: "
            + dingding_send_info["title"]
            + "\n\n"
            "> Browser: " + dingding_send_info["agent"] + "\n\n" +
            # "> ![screenshot](http://x.sctux.com/static/xxy/images/index.gif)\n\n" +
            "> [Add Blacklist?](http://x.sctux.com/blackip/"
            + dingding_send_info["address"]
            + ") \n"
            "> [CheckIP](http://x.sctux.com/checkip/"
            + dingding_send_info["address"]
            + ") \n",
        },
        "at": {"atMobiles": [user], "isAtAll": False},
    }

    ## 调用request.post发送json格式的参数
    headers = {"Content-Type": "application/json"}

    if (
        "Ubuntu" not in dingding_send_info["agent"]
        and "Firefox" not in dingding_send_info["agent"]
    ):
        result = requests.post(
            url=webhook, data=json.dumps(data), headers=headers, verify=False
        )
        print("--" * 30)
        print(result)
        print(result.json())
        print("--" * 30)

        if result.json()["errcode"] == 0:
            print("send ok")
        else:
            print("send failed!")
