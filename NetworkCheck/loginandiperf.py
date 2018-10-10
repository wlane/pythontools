#!/usr/bin/python
# -*- coding: utf-8 -*-

import paramiko
import threading
import Queue


class ServerLogin(object):

    def __init__(self, ip, passwd):
        self.ip = ip
        self.passwd = passwd

    def sshlogin(self, username, cmds):
        try:

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, 22, username, self.passwd, timeout=5)
            for cmd in cmds:
                out = []
                error = []
                print "cmd----"
                print cmd
                print cmd.split()[-1]
                stdin, stdout, stderr = ssh.exec_command(cmd)
                stdin.write("yes")
                for everyout in stdout.readlines():
                    out.append(everyout)
                for everyerror in stderr.readlines():
                    error.append(everyerror)
                print "out: "
                print out
                print "error*****"
                print error
                if len(out) > 2:
                    if out[1].startswith('Client'):
                        q.put((out, self.ip))
                    elif out[1].startswith('Connected to'):
                        qport.put((cmd.split()[-1], u'可达', self.ip))
                    else:
                        print "something is wrong with exec_commad"
                else:
                    if error[0].startswith('telnet: Unable to'):
                        qport.put((cmd.split()[-1], u'不可达', self.ip))
            ssh.close()


        except:
            print "%s\tError\n" % self.ip


remotehosts = {'192.168.0.193': 'aykj83752661', '192.168.0.239': 'aykj83752661'}
localhosts = {'10.0.16.55':'njay0508'}

if __name__ == '__main__':
    # remote_cmd = [
    #     'if [ `dpkg -l|grep iperf|wc -l` = 0 ];then echo aykj83752661 |sudo -S apt-get install iperf -y --force-yes;fi',
    #     'iperf -s -D 1>&2']          # 根据返回信息判断，当存在返回信息时，会一直判断处于运行状态，不退出
    # local_cmd = ['ls']
    # username = 'anyuan'
    # threads = []
    # result = []
    # hostip = []
    # bandvalue = []
    # k = 0
    # m = 0
    # q = Queue.Queue()
    # for host, pd in remotehosts.items():
    #     for localhost, localpd in localhosts.items():
    #         # print "Begining to login "+host+" ......"
    #         # print host, pd
    #         local_cmd = ['iperf -c '+host+' -t 12 -i 3']
    #         remote_run = ServerLogin(host, pd)
    #         local_run = ServerLogin(localhost, localpd)
    #         a = threading.Thread(target=remote_run.sshlogin, args=(username, remote_cmd))
    #         b = threading.Thread(target=local_run.sshlogin, args=('xueyunfei', local_cmd))
    #         a.start()
    #         a.join()
    #         b.start()
    #         b.join()
    # while not q.empty():
    #     result.append(q.get())
    # for item in result:
    #     if item[1] in localhosts:
    #         stritem = ' '
    #         i = 6
    #         j = 0
    #         interval = locals()
    #         hostip.append(item[0][1].split()[3].rstrip(','))
    #         while i < len(item[0]):
    #             if 'a'+str(j) not in interval:
    #                 interval['a'+str(j)] = []
    #                 interval['a'+str(j)].append(stritem.join(item[0][i].split()[2:5]))
    #             # print interval['a'+str(j)]
    #             i += 1
    #             j += 1
    #         i = 6
    #         j = 0
    #         while i < len(item[0]):
    #             interval['a' + str(j)].append(stritem.join(item[0][i].split()[-2:]))
    #             i += 1
    #             j += 1
    #             m = j
    # while k < m:
    #     bandvalue.append(locals()['a' + str(k)])
    #     k += 1
    # print "----------------------------------------"
    # print bandvalue
    # print hostip
    port = [22, 3333]
    remote_telnet_cmd = []
    portresult = []
    qport = Queue.Queue()
    for p in port:
        midp = '(echo quit;sleep 1) | telnet 192.168.0.180 '+str(p)
        print midp
        remote_telnet_cmd.append(midp)
    print remote_telnet_cmd
    for localhost, localpd in localhosts.items():
        remote_run = ServerLogin(localhost, localpd)
        a = threading.Thread(target=remote_run.sshlogin, args=('xueyunfei', remote_telnet_cmd))
        a.start()
        a.join()
    while not qport.empty():
        portresult.append(qport.get())
    for item in portresult:
        for i in range(len(item)):
            print item[i],

