#!/usr/bin/python
# -*- coding: utf-8 -*-

import paramiko
import parameters


class ServerLogin(object):

    def __init__(self, ip, passwd):
        self.ip = ip
        self.passwd = passwd

    def sshlogin(self, username, cmds, port=22):
        # try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, port, username, self.passwd, timeout=5)
            # global qping
            # qping = Queue.Queue()
            for cmd in cmds:
                out = []
                error = []
                stdin, stdout, stderr = ssh.exec_command(cmd)
                stdin.write("yes")
                for everyout in stdout.readlines():
                    out.append(everyout)
                for everyerror in stderr.readlines():
                    error.append(everyerror)
                # print "out: "
                # print out
                # print "error*****"
                # print error
                if len(out) > 2:
                    if out[1].startswith('Client'):
                        parameters.get_value('q').put((out, self.ip))
                    elif out[1].startswith('Connected to'):
                        parameters.get_value('qport').put((cmd.split()[-1], '可达', self.ip))
                    elif out[0].startswith('PING'):
                        parameters.get_value('qping').put((out, self.ip))
                    else:
                        if len(error) > 0:
                            print error
                        print "something is wrong with "+cmd+" in "+self.ip
                else:
                    if len(out) == 1 or len(out) == 2:
                        if error[0].startswith('telnet: Unable to'):
                            parameters.get_value('qport').put((cmd.split()[-1], '不可达', self.ip))
            ssh.close()

        #
        # except Exception,err:
        #     print "%s\tError\n" % self.ip
        #     print err
