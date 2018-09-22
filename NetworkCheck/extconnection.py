#!/usr/bin/python
# -*- coding:utf8 -*-

import pexpect
import datetime
import threading

host = ["www.baidu.com","114.114.114.114"]
#host = []

class PingStatus(object):

    def __init__(self, ip):
        #Thread.__init__(self)
        self.ip = ip

    def pingprocess(self):
        curtime = datetime.datetime.now()
        ping = pexpect.spawn("ping -c1 %s" % (self.ip))
        check = ping.expect([pexpect.TIMEOUT, "1 packets transmitted, 1 received, 0% packet loss"], 3)
        if check == 0:
            print("[%s] %s 超时" % (curtime, self.ip))
        elif check == 1:
            print ("[%s] %s 可达" % (curtime, self.ip))
        else:
            print("[%s] 主机%s 不可达" % (curtime, self.ip))


# 多线程同时执行
if __name__ == '__main__':
    for i in host:
        t = PingStatus(i)
        a = threading.Thread(target=t.pingprocess)
        a.start()
        a.join()
