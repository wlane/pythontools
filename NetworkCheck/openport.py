#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time
import threading


class OpenPort(object):

        def __init__(self, ip):
            self.ip = ip

        def createsocket(self, port):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((self.ip, int(port)))
                s.listen(10)
                print 'Waiting for telnet...'
                time.sleep(60)
                s.close()


if __name__ == '__main__':
    ports = "8888 9999"
    for port in ports.split():
        openports = OpenPort('127.0.0.1')
        a = threading.Thread(target=openports.createsocket, args=(port,))
        a.start()
