#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time


class OpenPort(object):

        def __init__(self, ip):
            self.ip = ip

        def socketserver(self, port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.ip, int(port)))
            s.listen(10)
            print 'Waiting for connection...'
            sock, addr = s.accept()
            print 'Accept new connection from %s:%s...' % addr
            while True:
                data = sock.recv(1024)
                time.sleep(1)
                if data == 'over':
                    break
            s.close()

        def socketclient(self, port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, int(port)))
            s.send('over')
            s.close()

# if __name__ == '__main__':
#     ports = "8888 9999"
#     for port in ports.split():
#         openports = OpenPort('0.0.0.0')
#         a = threading.Thread(target=openports.socketserver, args=(port,))
#         a.start()
#     time.sleep(30)
#     for port in ports.split():
#         openports = OpenPort('0.0.0.0')
#         a = threading.Thread(target=openports.socketclient, args=(port,))
#         a.start()
