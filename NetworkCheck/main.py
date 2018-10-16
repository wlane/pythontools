#!/usr/bin/python
# -*- coding:utf-8 -*-


from login import ServerLogin
from writetoexcel import WriteToExcel
import parameters
import threading
import Queue
import time


def baseparameters():       # 一些基础参数的获取
    while 1:
        host = raw_input('请确认所有linux主机的用户名,密码和ssh登陆端口一致，是否继续（y/n）: ')
        if host == 'y' or host == 'Y':
            global username, password, loginport, localhosts, remotehosts, telnetip, telnetports
            username = raw_input('请输入用户名：')
            password = raw_input('请输入密码：')
            loginport = raw_input('请输入登陆端口：')
            localhosts = {}
            remotehosts = {}
            host = raw_input('请输入本机的ip地址：')
            hosts = raw_input('请输入远程登陆的ip地址，以空格分开：')
            localhosts[host] = password
            for h in hosts.split():
                remotehosts[h] = password
            telnetip = raw_input('请输入端口检测的ip：')
            telnetports = raw_input('请输入需要检测的端口，以空格区分：')
        else:
            print "你需要先设置用户名和密码，确保他们在所有linux主机上一致"
            exit(5)
        ifcontinous = raw_input('请确认以上输入是否正确（y/n）: ')
        if ifcontinous == 'y' or host == 'Y':
            break
        else:
            continue


def pingstatus(username, localhosts, remotehosts, pingport=22):      # ping检测
    print "开始进行ping值检测...请稍候"
    pinghost = ["114.114.114.114", "www.baidu.com"]  # ping状态获取
    remote_ping_cmd = []
    pingresult = []
    pingstatus = {}
    aggstatus = []
    num = 0
    for i in pinghost:      # 拼接完整的命令
        midping = 'ping -c1 ' + str(i)
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
    for item in pingresult:
        packetloss = item[0][4].split()[5]
        minrtt = item[0][5].split('/')[3].split('=')[1]
        avgrtt = item[0][5].split('/')[4]
        maxrtt = item[0][5].split('/')[5]
        everystatus = [packetloss, minrtt, avgrtt, maxrtt]
        if num % 2 == 0:        # 只需要ping两个地址
            aggstatus = []
        aggstatus.append(everystatus)
        pingstatus[item[1]] = aggstatus
        num += 1
    return pingstatus
    # "pingstatus": "{'192.168.0.193':[['100%', 'null', 'null', 'null'], ['0%', '7.8 ms', '88.5 ms', '9.0 ms']],
    #               '192.168.0.180':[['100%', 'null', 'null', 'null'], ['0%', '7.8 ms', '88.5 ms', '9.0 ms']]}"


def telnetstatus(username, telnetip, telnetports, telnetport=22):      # 端口检测
    print "开始检测对外开放的端口...请稍候"
    telnetlocalhosts = {'192.168.0.163': 'aykj83752661'}   # 远程登陆执行telnet命令的服务器
    remote_telnet_cmd = []
    portresult = []
    portconnect = {}
    for p in telnetports.split():       # 拼接完成的命令
        midp = '(echo quit;sleep 1) | telnet ' + telnetip + ' ' + str(p)
        remote_telnet_cmd.append(midp)
    for localhost, localpd in telnetlocalhosts.items():     # 登陆相应服务器执行
        remote_telnet_run = ServerLogin(localhost, localpd)
        b = threading.Thread(target=remote_telnet_run.sshlogin, args=(username, remote_telnet_cmd, telnetport))
        b.start()
        b.join()
    while not parameters.get_value('qport').empty():    # 处理上述执行结果队列中的数据
        portresult.append(parameters.get_value('qport').get())
    for item in portresult:
        portconnect[item[0]] = item[1].decode('utf-8')
    return portconnect
    # "portconnect": "{'8000': u'\u4e0d\u53ef\u8fbe','7001': u'\u53ef\u8fbe'}"


def getband(username, localhosts, remotehosts, bandport=22):     # 带宽检测
    print "开始检测服务器之间的带宽...请稍候"
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
    for host, pd in remotehosts.items():    # 登陆相应服务器执行，先执行iperf服务端,再执行客户端操作
        for localhost, localpd in localhosts.items():
            local_cmd = [
                'if [ `dpkg -l|grep iperf|wc -l` = 0 ];then echo aykj83752661 |sudo -S apt-get install iperf -y --force-yes;fi',
                'iperf -c ' + host + ' -t 6 -i 3']
            remote_run = ServerLogin(host, pd)
            local_run = ServerLogin(localhost, localpd)
            c = threading.Thread(target=remote_run.sshlogin, args=(username, remote_cmd, bandport))
            d = threading.Thread(target=local_run.sshlogin, args=(username, local_cmd, bandport))
            c.start()
            c.join()
            d.start()
            d.join()
    while not parameters.get_value('q').empty():    # 处理上述操作后队列的数据
        result.append(parameters.get_value('q').get())
    for item in result:
        if item[1] in localhosts:
            stritem = ' '
            i = 6
            j = 0
            interval = locals()
            otherhost.append(item[0][1].split()[3].rstrip(','))     # 远程主机列表
            while i < len(item[0]):     # 遍历（从第7个值开始计算）
                if 'a' + str(j) not in interval:     # 在没有定义本地变量a0,a1...的情况下初始化变量
                    interval['a' + str(j)] = []
                    interval['a' + str(j)].append(stritem.join(item[0][i].split()[2:5]))  # 写入时间间隔，例如0.0-5.0 sec
                i += 1
                j += 1
            i = 6
            j = 0
            while i < len(item[0]):     # 遍历（从第7个值开始计算）
                interval['a' + str(j)].append(stritem.join(item[0][i].split()[-2:]))   # 写入带宽值
                i += 1
                j += 1
                m = j
    while k < m:
        bandvalue.append(locals()['a' + str(k)])    # 拼接结果值
        k += 1
    return bandvalue, otherhost
    # "bandvalue": "[['0.0-5.0 sec', '94.2 Mbits/sec', '90.6 Mbits/sec'],
    #               ['5.0-10.0 sec', '92.2 Mbits/sec', '93.0 Mbits/sec'],
    #               ['0.0-10.0 sec', '93.2 Mbits/sec', '94.3 Mbits/sec']]"
    # "otherhost": "['192.168.0.193', '192.168.0.233']",


if __name__ == '__main__':      # 主函数
    dt = {}
    baseparameters()    # 获取初始化参数
    parameters._init()      # 初始化全局变量
    parameters.set_value('q', Queue.Queue())
    parameters.set_value('qping', Queue.Queue())
    parameters.set_value('qport', Queue.Queue())
    pingvalue = pingstatus(username, localhosts, remotehosts, int(loginport))
    band, hostip = getband(username, localhosts, remotehosts, int(loginport))
    portvalue = telnetstatus(username, telnetip, telnetports, int(loginport))
    dt["bandvalue"] = str(band)     # 拼接各个结果值
    dt["otherhost"] = str(hostip)
    dt["portconnect"] = str(portvalue)
    dt["pingstatus"] = str(pingvalue)
    print dt
    for localhostip in localhosts.keys():   # 写入excel文档
        e = WriteToExcel(time.strftime("%Y-%m-%d-%H-%M", time.localtime()) + "-网络测试.xlsx")
        e.writeinband(localhostip, **dt)

