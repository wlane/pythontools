#!/usr/bin/python
# -*- coding: utf-8 -*-

import paramiko
import threading
import Queue


class ServerLogin(object):

    def __init__(self, ip, passwd):
        self.ip = ip
        self.passwd = passwd

    def sshlogin(self, username, cmd):
        try:

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, 22, username, self.passwd, timeout=5)
            out = []
            error = []
            for m in cmd:
                stdin, stdout, stderr = ssh.exec_command(m)
                stdin.write("yes")
                for everyout in stdout.readlines():
                    out.append(everyout)
                for everyerror in stderr.readlines():
                    error.append(everyerror)
                print "out: "
                print out
                print "error*****"
                print error

            print "%s\tis\tdone\n" % self.ip
            ssh.close()
            if len(out) > 2:
                if out[1].startswith('Client'):
                    q.put((out, self.ip))
                else:
                    print "wrong---------"

        except:
            print "%s\tError\n" % self.ip


remotehosts = {'192.168.0.193': 'aykj83752661'}
localhosts = {'10.0.16.55':'njay0508'}

if __name__ == '__main__':
    remote_cmd = [
        'if [ `dpkg -l|grep iperf|wc -l` = 0 ];then echo aykj83752661 |sudo -S apt-get install iperf -y --force-yes;fi',
        'iperf -s -D 1>&2']          # 根据返回信息判断，当存在返回信息时，会一直判断处于运行状态，不退出
    local_cmd = ['ls']
    username = 'anyuan'
    threads = []
    result = []
    q = Queue.Queue()
    for host, pd in remotehosts.items():
        for localhost, localpd in localhosts.items():
            # print "Begining to login "+host+" ......"
            # print host, pd
            local_cmd = ['iperf -c '+host+' -t 9 -i 3']
            remote_run = ServerLogin(host, pd)
            local_run = ServerLogin(localhost, localpd)
            a = threading.Thread(target=remote_run.sshlogin, args=(username, remote_cmd))
            b = threading.Thread(target=local_run.sshlogin, args=('xueyunfei', local_cmd))
            a.start()
            a.join()
            b.start()
            b.join()
            while not q.empty():
                result.append(q.get())
            for item in result:
                if item[1] == localhost:
                    stritem = ' '
                    i = 6
                    while i < len(item[0])-1:
                        print "i="+str(i)
                        print "%s 's return value is : %s" % (stritem.join(item[0][i].split()[2:5]), stritem.join(item[0][i].split()[-2:]))
                        i += 1

            # remote_telnet_cmd = ['(echo quit;sleep 1) | telnet 192.168.0.180 3333']
    # for localhost, localpd in localhosts.items():
    #     remote_run = ServerLogin(localhost, localpd)
    #     a = threading.Thread(target=remote_run.sshlogin, args=('xueyunfei', remote_telnet_cmd))
    #     a.start()
    #     a.join()

