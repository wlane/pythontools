#!/usr/bin/python
# -*- coding:utf8 -*-

import pexpect
from pexpect import popen_spawn
import datetime
import threading

host = ["114.114.114.114"]
#host = []

class PingStatus(object):

    def __init__(self, ip):
        #Thread.__init__(self)
        self.ip = ip

    def pingprocess(self):
        curtime = datetime.datetime.now()
        print "1"
        # ping = pexpect.spawn("ping -c1 %s" % (self.ip))   # linux
        ping = pexpect.popen_spawn.PopenSpawn('cmd')    # windows
        ping.sendline('ping %s' % (self.ip))   # windows
        ping.sendline('exit')    # windows
        ping.expect(pexpect.EOF)  # windows
        out = ping.before.decode('gbk')   # windows
        per = out[:out.find('%')][-2:]   # windows
        per = [ch for ch in per if ch.isdigit()]   # windows
        per = int(''.join(per))   # windows
        if per >= 100:   # windows
            print('[%s] %s  网络不通！' % (curtime, self.ip))   # windows
        elif 80 >= per >= 30:   # windows
            print('[%s] %s 网络不稳定！' % (curtime, self.ip))   # windows
        else:   # windows
            print('[%s] %s 网络正常！' % (curtime, self.ip))   # windows
        # check = ping.expect([pexpect.TIMEOUT, "1 packets transmitted, 1 received, 0% packet loss"], 3)  #linux

        # if check == 0:  #linux
        #     print("[%s] %s 超时" % (curtime, self.ip))  #linux
        # elif check == 1:  #linux
        #     print ("[%s] %s 可达" % (curtime, self.ip))  #linux
        # else:  #linux
        #     print("[%s] 主机%s 不可达" % (curtime, self.ip))  #linux


# 多线程同时执行
if __name__ == '__main__':
    for i in host:
        t = PingStatus(i)
        a = threading.Thread(target=t.pingprocess)
        a.start()
        a.join()
