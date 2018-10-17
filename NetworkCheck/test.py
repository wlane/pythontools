#!/usr/bin/python
# -*- coding: utf-8 -*-

from login import ServerLogin
from writetoexcel import WriteToExcel
import parameters
import threading
import Queue
import time


def pingstatus(username, localhosts, remotehosts, pingport=22):      # ping检测
    print "开始进行ping值检测...请稍候"
    pinghost = ["114.114.114.115", "www.baidu.com"]  # ping状态获取
    remote_ping_cmd = []
    pingresult = []
    pingstatus = {}
    aggstatus = []
    num = 0
    for i in pinghost:      # 拼接完整的命令
        midping = 'ping -c3 ' + str(i)
        remote_ping_cmd.append(midping)
    allhosts = localhosts.copy()
    allhosts.update(remotehosts)
    for host, pd in allhosts.items():    # 登陆每台服务器执行操作
        remote_ping_run = ServerLogin(host, pd)
        a = threading.Thread(target=remote_ping_run.sshlogin, args=(username, remote_ping_cmd, pingport))
        a.start()
        a.join()
    while not parameters.get_value('qping').empty():        # 处理上面操作完成后队列中的数据
        pingresult.append(parameters.get_value('qping').get())
    # print pingresult
    for item in pingresult:
        minrtt = 'null'
        avgrtt = 'null'
        maxrtt = 'null'
        print item[0]
        print 'long: '+str(len(item[0]))
        for i in item[0]:
            if 'packet' in i:
                packetloss = i.split()[5]     # 截取测试结果,此处的数据63与ping命令后面选项c的值有关,c值加3
            if 'rtt' in i:
                minrtt = i.split('/')[3].split('=')[1]
                avgrtt = i.split('/')[4]
                maxrtt = i.split('/')[5]
        everystatus = [packetloss, minrtt, avgrtt, maxrtt]
        if num % 2 == 0:        # 只需要ping两个地址
            aggstatus = []
        aggstatus.append(everystatus)
        pingstatus[item[1]] = aggstatus
        num += 1
    print pingstatus
    return pingstatus
    # "pingstatus": "{'192.168.0.193':[['100%', 'null', 'null', 'null'], ['0%', '7.8 ms', '88.5 ms', '9.0 ms']],
    #               '192.168.0.180':[['100%', 'null', 'null', 'null'], ['0%', '7.8 ms', '88.5 ms', '9.0 ms']]}"


if __name__ == "__main__":
    parameters._init()  # 初始化全局变量
    parameters.set_value('qping', Queue.Queue())
    username = "anyuan"
    localhosts = {"192.168.0.163": "aykj83752661"}
    remotehosts = {"192.168.0.239": "aykj83752661", "192.168.0.235": "aykj83752661"}
    pingstatus(username, localhosts, remotehosts)