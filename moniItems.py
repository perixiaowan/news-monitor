#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import time
import urllib
import json
import socket
import urllib.request
import urllib.parse


class mon:
    def __init__(self):
        self.data = {}

    def getTime(self):
        return str(int(time.time()) + 8 * 3600)

    def getHost(self):
        return socket.gethostname()

    def getLoadAvg(self):
        with open('/proc/loadavg') as load_open:
            a = load_open.read().split()[:3]
            return ','.join(a)

    def getMemTotal(self):
        with open('/proc/meminfo') as mem_open:
            a = int(mem_open.readline().split()[1])
            return a / 1024

    def getMemUsage(self, noBufferCache=True):
        if noBufferCache:
            with open('/proc/meminfo') as mem_open:
                T = int(mem_open.readline().split()[1])
                F = int(mem_open.readline().split()[1])
                B = int(mem_open.readline().split()[1])
                C = int(mem_open.readline().split()[1])
                return (T - F - B - C) / 1024
        else:
            with open('/proc/meminfo') as mem_open:
                a = int(mem_open.readline().split()[1]) - int(mem_open.readline().split()[1])
                return a / 1024

    def getMemFree(self, noBufferCache=True):
        if noBufferCache:
            with open('/proc/meminfo') as mem_open:
                T = int(mem_open.readline().split()[1])
                F = int(mem_open.readline().split()[1])
                B = int(mem_open.readline().split()[1])
                C = int(mem_open.readline().split()[1])
                return (F + B + C) / 1024
        else:
            with open('/proc/meminfo') as mem_open:
                mem_open.readline()
                a = int(mem_open.readline().split()[1])
                return a / 1024

    def runAllGet(self):
        # 自动获取mon类里的所有getXXX方法，用XXX作为key，getXXX()的返回值作为value，构造字典
        for fun in inspect.getmembers(self, predicate=inspect.ismethod):
            if fun[0][:3] == 'get':
                self.data[fun[0][3:]] = fun[1]()
        return self.data


if __name__ == "__main__":
    while True:
        m = mon()
        data = m.runAllGet()
        print("type(data):%s" %(type(data)))
        print(data)
        params = urllib.parse.urlencode(data).encode(encoding='UTF8')
        print("type(params):%s" % (type(params)))
        url = "http://47.52.106.208:8888"
        # data = urllib.parse.urlencode(value).encode(encoding='utf-8')
        # req = urllib.request("http://47.52.106.208:8888", json.dumps(data), {'Content-Type': 'application/json'})
        f = urllib.request.Request(url, params, {'Content-Type': 'application/json'})
        # f = urllib.request.urlopen(urlencode)
        # f = urllib.urlopen(req)
        response = f.read().decode('utf-8')
        print(response)
        f.close()
        time.sleep(60)