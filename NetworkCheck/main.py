#!/usr/bin/python
# -*- coding:utf-8 -*-

hosts = {}
while 1:
    host = raw_input(u'请输入远程主机的ip和密码(例如): ')
    hosts[host[0]] = hosts[host[1]]

print hosts