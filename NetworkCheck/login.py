# !/usr/bin/python
# -*- coding: utf-8 -*-

import paramiko
import threading


class SystemInitial(object):
    def __init__(self, ip, passwd):
        self.ip = ip
        self.passwd = passwd

    def ssh_login(self, username, cmd):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, 22, username, self.passwd, timeout=5)
            for m in cmd:
                stdin, stdout, stderr = ssh.exec_command(m)
                stdin.write("yes")
                for out in stdout.readlines():
                    print "out message: "+out,
                for err in stderr.readlines():
                    print "error message: "+err,
            print "%s\tis\tdone\n" % self.ip
            ssh.close()
        except:
            print "%s\tError\n" % self.ip

remotehosts = {'192.168.0.193': 'aykj83752661','192.168.0.239':'aykj83752661'}
localhosts = {'10.0.16.55':'njay0508'}

if __name__ == '__main__':
    remote_cmd = ['echo aykj83752661 | sudo -S apt-get install iperf -y --force-yes','iperf -s -D 1>&2']
    #remote_cmd = ['ip a |grep 192']
    local_cmd = ['ls']
    username = 'anyuan'
    threads = []
    for host, pd in remotehosts.items():
        for localhost, localpd in localhosts.items():
            print "Begining to login "+host+" ......"
            print host, pd
            local_cmd = ['iperf -c '+host+' -t 10 -i 5']
            remote_run = SystemInitial(host, pd)
            local_run = SystemInitial(localhost, localpd)
            a = threading.Thread(target=remote_run.ssh_login, args=(username, remote_cmd))
            b = threading.Thread(target=local_run.ssh_login,args=('xueyunfei', local_cmd))  #
            a.start()
            a.join()
            b.start()
