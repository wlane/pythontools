#!/usr/bin/python
# -*- coding:utf-8 -*-

import paramiko
import threading
import Queue


def baseparameters():
    while 1:
        host = raw_input(u'请确认所有linux主机的用户名和密码一致，是否继续（y/n）: ')
        if host == 'y':
            username = raw_input(u'请输入用户名：')
            password = raw_input(u'请输入密码：')
            host = raw_input(u'请输入本机的ip地址：')
            hosts = raw_input(u'请输入远程登陆的ip地址，以空格分开：')
            localhosts[host] = password
            for h in hosts.split():
                remotehosts[h] = password
        else:
            print u"你需要先设置用户名和密码，确保他们在所有linux主机上一致"
            exit(5)
        ifcontinous = raw_input(u'请确认以上输入是否正确（y/n）: ')
        if ifcontinous == 'y':
            break
        else:
            continue


def pingstatus():
    pinghost = ["114.114.114.114", "www.baidu.com"]  # ping状态获取
    qping = Queue.Queue()
    remote_ping_cmd = []
    pingresult = []
    everystatus = []
    pingstatus = {}
    num = 0
    username = 'anyuan'
    for i in pinghost:
        midping = 'ping -c1 ' + str(i)
        remote_ping_cmd.append(midping)
    for host, pd in remotehosts.items():
        remote_ping_run = ServerLogin(host, pd)
        a = threading.Thread(target=remote_ping_run.sshlogin, args=(username, remote_ping_cmd))
        a.start()
        a.join()
    while not qping.empty():
        pingresult.append(qping.get())
    print "------------------------------------"
    for item in pingresult:
        packetloss = item[0][4].split()[5]
        minrtt = item[0][5].split('/')[3].split('=')[1]
        avgrtt = item[0][5].split('/')[4]
        maxrtt = item[0][5].split('/')[5]
        everystatus = [packetloss, minrtt, avgrtt, maxrtt]
        if num % 2 == 0:
            aggstatus = []
        aggstatus.append(everystatus)
        pingstatus[item[1]] = aggstatus
        num += 1
    print pingstatus


def telnetstatus():
    port = [22, 3333]  # telnet状态获取
    remote_telnet_cmd = []
    portresult = []
    portconnect = {}
    qport = Queue.Queue()
    for p in port:
        midp = '(echo quit;sleep 1) | telnet 192.168.0.180 ' + str(p)
        # print midp
        remote_telnet_cmd.append(midp)
    # print remote_telnet_cmd
    for localhost, localpd in localhosts.items():
        remote_telnet_run = ServerLogin(localhost, localpd)
        a = threading.Thread(target=remote_telnet_run.sshlogin, args=(username, remote_telnet_cmd))
        a.start()
        a.join()
    while not qport.empty():
        portresult.append(qport.get())
    # print portresult
    for item in portresult:
        portconnect[item[0]] = item[1].decode('utf-8')
    print "----------------------------------------"
    print "portconnect"
    print portconnect  # unicode字符


def getband():
    remote_cmd = [  # band状态获取
        'if [ `dpkg -l|grep iperf|wc -l` = 0 ];then echo aykj83752661 |sudo -S apt-get install iperf -y --force-yes;fi',
        'iperf -s -D 1>&2']  # 根据返回信息判断，当存在返回信息时，会一直判断处于运行状态，不退出
    local_cmd = ['ls']
    threads = []
    result = []
    otherhost = []
    bandvalue = []
    k = 0
    m = 0
    q = Queue.Queue()
    for host, pd in remotehosts.items():
        for localhost, localpd in localhosts.items():
            # print "Begining to login "+host+" ......"
            # print host, pd
            local_cmd = [
                'if [ `dpkg -l|grep iperf|wc -l` = 0 ];then echo aykj83752661 |sudo -S apt-get install iperf -y --force-yes;fi',
                'iperf -c ' + host + ' -t 12 -i 3']
            remote_run = ServerLogin(host, pd)
            local_run = ServerLogin(localhost, localpd)
            a = threading.Thread(target=remote_run.sshlogin, args=(username, remote_cmd))
            b = threading.Thread(target=local_run.sshlogin, args=(username, local_cmd))
            a.start()
            a.join()
            b.start()
            b.join()
    while not q.empty():
        result.append(q.get())
    for item in result:
        if item[1] in localhosts:
            stritem = ' '
            i = 6
            j = 0
            interval = locals()
            otherhost.append(item[0][1].split()[3].rstrip(','))
            while i < len(item[0]):
                if 'a' + str(j) not in interval:
                    interval['a' + str(j)] = []
                    interval['a' + str(j)].append(stritem.join(item[0][i].split()[2:5]))
                # print interval['a'+str(j)]
                i += 1
                j += 1
            i = 6
            j = 0
            while i < len(item[0]):
                interval['a' + str(j)].append(stritem.join(item[0][i].split()[-2:]))
                i += 1
                j += 1
                m = j
    while k < m:
        bandvalue.append(locals()['a' + str(k)])
        k += 1
    print "----------------------------------------"
    print "band***"
    print bandvalue
    print otherhost


if __name__ == '__main__':
    remotehosts = {}
    localhosts = {}
    username = ''
    password = ''
    baseparameters()


    print username
    print password
    print localhosts
    print remotehosts
