#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql as mysql
import json
from flask import Flask, request, render_template

app = Flask(__name__)
db = mysql.connect(host="47.52.106.208",user="xiaowan", password="xiaowan", db="falcon", charset="utf8")
db.autocommit(True)


# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 fetchone() 方法获取单条数据.

@app.route("/", methods=["GET", "POST"])
def hello():
    sql = ""
    if request.method == "POST":
        data = request.json
        print("data:%s" % (data['Host']))
        print("data:%s" % (data['MemFree']))
        print("data:%s" % (data['MemUsage']))
        print("data:%s" % (data['MemTotal']))
        print("data:%s" % (data['LoadAvg']))
        print("data:%s" % (data['Time']))
        print("type data['LoadAvg']:%s" % (type(data['LoadAvg'])))
        print("type data['Time']:%s" % (type(data['Time'])))
        try:
            sql = "INSERT INTO `stat` (`host`,`mem_free`,`mem_usage`,`mem_total`,`load_avg`,`time`) VALUES('%s', '%d', '%d', '%d', '%s', '%s')" % (
            data['Host'], data['MemFree'], data['MemUsage'], data['MemTotal'], data['LoadAvg'], data['Time'])
            ret = cursor.execute(sql)
        except mysql.IntegrityError:
            pass
        return "OK"
    else:
        return render_template("mon.html")


@app.route("/data", methods=["GET"])
def getdata():
    cursor.execute("SELECT `time`,`mem_usage` FROM `stat`")
    ones = [[i[0].strftime("%Y-%m-%d %H:%M:%S"), i[1]] for i in cursor.fetchall()]
    onesToJson = json.dumps(ones)
    print("json.dumps(ones):%s" %(type(json.dumps(ones))))
    return "%s(%s);" % (request.args.get('callback'), onesToJson)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
    # app.run(host="127.0.0.1", port=8888, debug=True)