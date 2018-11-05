#!/usr/bin/python
# -*- coding:utf-8 -*-


from login import ServerLogin
from writetoexcel import WriteToExcel
from openport import OpenPort
import parameters
import threading
import Queue
import time
import sys
import shutil


def baseparameters():       # 一些基础参数的获取
    alertmessage = raw_input('如果需要测试端口是否开放,请在端口所在的内网服务器上执行该脚本.是否继续（y/n）：')
    if alertmessage == 'y' or alertmessage == 'Y':
        while 1:
            host = raw_input('请确认所有linux主机的用户名,密码和ssh登陆端口一致,是否继续（y/n）: ')
            if host == 'y' or host == 'Y':
                global bandcontinue, pingcontinue, telnetcontinue, username, password, loginport, localhosts, remotehosts, telnetlocalhosts, telnetip, telnetports
                bandcontinue = raw_input('是否需要检测服务器之间的带宽：（y/n）：')
                pingcontinue = raw_input('是否需要检测外网是否连通（y/n）：')
                telnetcontinue = raw_input('是否需要检测端口是否对外开放：（y/n）：')
                username = raw_input('请输入用户名（默认值请回车）：') or "anyuan"
                password = raw_input('请输入密码（默认值请回车）：') or "aykj83752661"
                loginport = raw_input('请输入登陆端口（默认值请回车）：') or int('22')
                localhosts = {}
                remotehosts = {}
                host = raw_input('请输入本机的ip地址：')
                hosts = raw_input('请输入其他服务器的ip地址，以空格分开：')
                localhosts[host] = password
                for h in hosts.split():
                    remotehosts[h] = password
                telnetlocalhosts = raw_input('请输入测试端口需要登陆的服务器ip,ssh端口,用户名和密码（顺序不能错,以空格区分）：')
                outport = raw_input('是否存在映射出去对外开放的端口（y/n）：')
                if outport == 'y' or outport == 'Y':
                    telnetip = raw_input('请输入对外开放的端口对应的映射的公网ip：')
                else:
                    telnetip = host
                telnetports = raw_input('请输入需要检测的端口,以空格区分：')
            else:
                print "你需要先设置用户名和密码,确保他们在所有linux主机上一致."
                sys.exit()
            ifcontinous = raw_input('请确认以上输入是否正确（y/n）: ')
            if ifcontinous == 'y' or host == 'Y':
                break
            else:
                continue
    else:
        sys.exit()
    # global bandcontinue, pingcontinue, telnetcontinue, username, password, loginport, localhosts, remotehosts, telnetlocalhosts, telnetip, telnetports
    # username = "anyuan"
    # password = "aykj83752661"
    # loginport = "22"
    # telnetlocalhosts = "221.226.186.58 5005 anyuan aykj83752661"
    # localhosts = {}
    # remotehosts = {}
    # bandcontinue = sys.argv[1]
    # pingcontinue = sys.argv[2]
    # telnetcontinue = sys.argv[3]
    # host = sys.argv[4]
    # localhosts[host] = "aykj83752661"
    # hosts = sys.argv[5]
    # for h in hosts.split():
    #     remotehosts[h] = "aykj83752661"
    # telnetip = sys.argv[6]
    # telnetports = sys.argv[7]


def pingstatus(username, localhosts, remotehosts, pingport=22):      # ping检测
    if pingcontinue == 'y' or pingcontinue == 'Y':
        print "开始外网是否连通...请稍候"
        pinghost = ["114.114.114.114", "www.baidu.com"]  # ping状态获取
        remote_ping_cmd = []
        pingresult = []
        pingstatus = {}
        aggstatus = []
        at = []
        num = 0
        for i in pinghost:      # 拼接完整的命令
            midping = 'ping -c4 ' + str(i)
            remote_ping_cmd.append(midping)
        allhosts = localhosts.copy()
        allhosts.update(remotehosts)
        for host, pd in allhosts.items():    # 登陆每台服务器执行操作
            remote_ping_run = ServerLogin(host, pd)
            a = threading.Thread(target=remote_ping_run.sshlogin, args=(username, remote_ping_cmd, pingport))
            a.start()
            # a.join()
            at.append(a)        # 将子线程放入列表,等子线程执行结束再执行主线程
        for t in at:
            t.join()
        while not parameters.get_value('qping').empty():        # 处理上面操作完成后队列中的数据
            pingresult.append(parameters.get_value('qping').get())
        # print pingresult
        for item in pingresult:
            packetloss = 'null'
            minrtt = 'null'
            avgrtt = 'null'
            maxrtt = 'null'
            for i in item[0]:
                if 'packet' in i:
                    packetloss = i.split()[5]     # 截取测试结果
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
        return pingstatus
        # "pingstatus": "{'192.168.0.193':[['100%', 'null', 'null', 'null'], ['0%', '7.8 ms', '88.5 ms', '9.0 ms']],
        #               '192.168.0.180':[['100%', 'null', 'null', 'null'], ['0%', '7.8 ms', '88.5 ms', '9.0 ms']]}"
    else:
        return


def telnetstatus(telnetlocalhosts, telnetip, telnetports):      # 端口检测
    if telnetcontinue == 'y' or telnetcontinue == 'Y':
        print "开始检测端口是否对外开放...请稍候"
        remote_telnet_cmd = []
        telnetkeyfile = "/home/anyuan/.ssh/id_rsa"
        portresult = []
        portconnect = {}
        jt = []
        kt = []
        i = 0
        for v in telnetlocalhosts.split():  # 获取远程登陆服务器的参数
            if i == 0:
                telnethost = v
                i += 1
            elif i == 1:
                telnetport = v
                i += 1
            elif i == 2:
                telnetuser = v
                i += 1
            elif i == 3:
                telnetpd = v
        for p in telnetports.split():       # 拼接完成的命令
            midp = '(echo quit;sleep 1) | telnet ' + telnetip + ' ' + str(p)
            remote_telnet_cmd.append(midp)
        for port in telnetports.split():        # 开启端口
            openports = OpenPort('0.0.0.0')
            b = threading.Thread(target=openports.socketserver, args=(port,))
            b.start()
        time.sleep(10)
        remote_telnet_run = ServerLogin(telnethost, telnetpd)   # 登陆相应服务器执行命令
        remote_telnet_run.keylogin(telnetuser, telnetkeyfile, remote_telnet_cmd, telnetport)
        while not parameters.get_value('qport').empty():    # 处理上述执行结果队列中的数据
            portresult.append(parameters.get_value('qport').get())
        for item in portresult:
            portconnect[item[0]] = item[1].decode('utf-8')
        return portconnect
        # "portconnect": "{'8000': u'\u4e0d\u53ef\u8fbe','7001': u'\u53ef\u8fbe'}"
    else:
        return


def getband(username, localhosts, remotehosts, bandport=22):     # 带宽检测
    if bandcontinue == 'y' or bandcontinue == 'Y':
        print "开始检测服务器之间的带宽...请稍候"
        threads = []
        result = []
        otherhost = []
        bandwidth = []
        k = 0
        m = 0
        tserver = []
        tclient = []
        for host, pd in remotehosts.items():    # 登陆相应服务器执行，先执行iperf服务端,再执行客户端操作
            remote_cmd = [  # band状态获取
                'if [ `dpkg -l|grep iperf|wc -l` = 0 ];then echo aykj83752661 |sudo -S apt-get install iperf -y --force-yes;fi',
                'iperf -s -D 1>&2']  # 根据返回信息判断，当存在返回信息时，会一直判断处于运行状态，不退出
            remote_run = ServerLogin(host, pd)
            c = threading.Thread(target=remote_run.sshlogin, args=(username, remote_cmd, bandport))
            c.start()
            tserver.append(c)
        for t in tserver:
            t.join()
        for host in remotehosts.keys():     # 执行iperf客户端命令
            for localhost, localpd in localhosts.items():
                local_cmd = [
                    'if [ `dpkg -l|grep iperf|wc -l` = 0 ];then echo aykj83752661 |sudo -S apt-get install iperf -y --force-yes;fi',
                    'iperf -c ' + host + ' -t 10 -i 10']       # 10秒的间隔.小于10的话需要调整下面写入时间间隔的方式
                local_run = ServerLogin(localhost, localpd)
                d = threading.Thread(target=local_run.sshlogin, args=(username, local_cmd, bandport))
                d.start()
                tclient.append(d)
        for t in tclient:
            t.join()
        for host, pd in remotehosts.items():    # 登陆相应服务器执行，先执行iperf服务端,再执行客户端操作
            remote_cmd = ["ps -ef|grep iperf | grep -v grep | awk '{print $2}' | xargs kill -9"]  # 杀掉服务端进程
            remote_run = ServerLogin(host, pd)
            e = threading.Thread(target=remote_run.sshlogin, args=(username, remote_cmd, bandport))
            e.start()
            tserver.append(e)
        for e in tserver:
            e.join()
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
                        interval['a' + str(j)].append(stritem.join(item[0][i].split()[2:4]))  # 写入时间间隔,例如0.0-10.0 sec
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
            bandwidth.append(locals()['a' + str(k)])    # 拼接结果值
            k += 1
        return bandwidth, otherhost
        # "bandwidth": "[['0.0-5.0 sec', '94.2 Mbits/sec', '90.6 Mbits/sec'],
        #               ['5.0-10.0 sec', '92.2 Mbits/sec', '93.0 Mbits/sec'],
        #               ['0.0-10.0 sec', '93.2 Mbits/sec', '94.3 Mbits/sec']]"
        # "otherhost": "['192.168.0.193', '192.168.0.233']",
    else:
        return


if __name__ == '__main__':      # 主函数
    dt = {}
    baseparameters()    # 获取初始化参数
    parameters._init()      # 初始化全局变量
    parameters.set_value('q', Queue.Queue())
    parameters.set_value('qping', Queue.Queue())
    parameters.set_value('qport', Queue.Queue())
    pingvalue = pingstatus(username, localhosts, remotehosts, int(loginport))
    bandwidthvalue = getband(username, localhosts, remotehosts, int(loginport))
    portvalue = telnetstatus(telnetlocalhosts, telnetip, telnetports)
    dt["bandvalue"] = str(bandwidthvalue[0])     # 拼接各个结果值
    dt["otherhost"] = str(bandwidthvalue[1])
    dt["portconnect"] = str(portvalue)
    dt["pingstatus"] = str(pingvalue)
    for localhostip in localhosts.keys():   # 写入excel文档
        filename = time.strftime("%Y-%m-%d-%H-%M", time.localtime()) + "-网络测试.xlsx"
        e = WriteToExcel(filename)
        e.writeinband(localhostip, **dt)
        shutil.move(filename, "/home/anyuan/Desktop/")
        print "检测结果路径: /home/anyuan/Desktop/" + filename
    print "检测完毕！"