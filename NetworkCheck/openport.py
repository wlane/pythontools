#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time


class OpenPort(object):     # 打开需要检测的端口

        def __init__(self, ip):     # 初始化ip.一般为0.0.0.0
            self.ip = ip

        def socketserver(self, port):   # socket服务端,打开端口,接受信息
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((self.ip, int(port)))
                s.listen(10)
                # print 'Waiting for connection...'
                sock, addr = s.accept()
                # print 'Accept new connection from %s:%s...' % addr
                while True:
                    data = sock.recv(4)
                    time.sleep(1)
                    # print "port=%s data=%s" % (port, data)
                    if data == 'quit':      # 接受到quit信息则退出
                        break
                sock.close()
            except socket.error, msg:  # 出错处理
                print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]

        def socketclient(self, port):   # socket客户端，发送信息
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.ip, int(port)))
                print "closeport="+port
                s.send('over')
                s.close()
            except socket.error:
                print "socketclient error"
