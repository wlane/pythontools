#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import paramiko
import parameters


class ServerLogin(object):      # 登陆服务器并执行命令的类

    def __init__(self, ip, passwd):   # 初始化参数
        self.ip = ip
        self.passwd = passwd

    def sshlogin(self, username, cmds, port=22):   # 使用密码登陆执行相应操作
        try:
            ssh = paramiko.SSHClient()  # 创建ssh实例
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, port, username, self.passwd, timeout=5)   # 建立一个ssh的连接
            for cmd in cmds:
                out = []
                error = []
                stdin, stdout, stderr = ssh.exec_command(cmd)   # 执行cmd命令
                stdin.write("yes")  # 执行命令过程中可能需要输入yes
                for everyout in stdout.readlines():     # 执行命令后的输出
                    out.append(everyout)
                for everyerror in stderr.readlines():   # 错误输出
                    error.append(everyerror)
                # print "out: " + str(out) + " in " + self.ip
                # print "error: " + str(error) + " in " + self.ip
                if len(out) > 2:    # 当输出内容长度大于2时，即有效输出
                    if out[1].startswith('Client'):     # 根据输出判断操作是带宽检测,将内容存入q队列
                        parameters.get_value('q').put((out, self.ip))
                    elif out[1].startswith('Connected to'):     # 根据输出判断操作是端口检测,将内容存入qport队列
                        parameters.get_value('qport').put((cmd.split()[-1], '可达', self.ip))
                    elif out[0].startswith('PING'):     # 根据输出判断操作是ping检测,将内容存入qping队列
                        parameters.get_value('qping').put((out, self.ip))
                    else:
                        if len(error) > 0:      # 错误输出不为空时,输出错误内容
                            print error,
                            print " something is wrong with " + cmd + " in " + self.ip
                else:
                    if len(out) == 1 or len(out) == 2:      # 当输出内容小于2时,此时一般命令执行有问题
                        if error[0].startswith('telnet: Unable to'):        # 同时存在标准输出和错误输出
                            parameters.get_value('qport').put((cmd.split()[-1], '不可达', self.ip))
                    else:       # 当输出内容为0时
                        if len(error) > 0:      # 存在错误输出
                            print error,
                            print " something is wrong with " + cmd + " in " + self.ip
            ssh.close()
        except Exception, err:       # 出错时的处理
            print "%s\tError:\n" % self.ip
            print err

    def keylogin(self, username, keyfile, cmds, port=22):       # 使用key文件登录
        try:
            pkeyfile = os.path.expanduser(keyfile)
            key = paramiko.RSAKey.from_private_key_file(pkeyfile)
            ssh = paramiko.SSHClient()  # 创建ssh实例
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.ip, port=port, username=username, pkey=key, timeout=5)
            for cmd in cmds:
                out = []
                error = []
                stdin, stdout, stderr = ssh.exec_command(cmd)   # 执行cmd命令
                stdin.write("yes")  # 执行命令过程中可能需要输入yes
                for everyout in stdout.readlines():     # 执行命令后的输出
                    out.append(everyout)
                for everyerror in stderr.readlines():   # 错误输出
                    error.append(everyerror)
                # print "out: " + str(out) + " in " + self.ip
                # print "error: " + str(error) + " in " + self.ip
                if len(out) > 2:    # 当输出内容长度大于2时，即有效输出
                    if out[1].startswith('Client'):     # 根据输出判断操作是带宽检测,将内容存入q队列
                        parameters.get_value('q').put((out, self.ip))
                    elif out[1].startswith('Connected to'):     # 根据输出判断操作是端口检测,将内容存入qport队列
                        parameters.get_value('qport').put((cmd.split()[-1], '可达', self.ip))
                    elif out[0].startswith('PING'):     # 根据输出判断操作是ping检测,将内容存入qping队列
                        parameters.get_value('qping').put((out, self.ip))
                    else:
                        if len(error) > 0:      # 错误输出不为空时,输出错误内容
                            print error,
                            print " something is wrong with " + cmd + " in " + self.ip
                else:
                    if len(out) == 1 or len(out) == 2:      # 当输出内容小于2时,此时一般命令执行有问题
                        if error[0].startswith('telnet: Unable to'):        # 同时存在标准输出和错误输出
                            parameters.get_value('qport').put((cmd.split()[-1], '不可达', self.ip))
                    else:       # 当输出内容为0时
                        if len(error) > 0:      # 存在错误输出
                            print error,
                            print " something is wrong with " + cmd + " in " + self.ip
            ssh.close()
        except Exception, err:
            print "%s\tError:\n" % self.ip
            print err
