#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time
import threading


class OpenPort(object):

        def __init__(self, ports):
            self.ports = ports

        def createsocket(self):
            for port in self.ports.split():
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(("127.0.0.1", int(port)))
                s.listen(2)
                print 'Waiting for telnet...'
                time.sleep(10)
                s.close()


if __name__ == '__main__':
    ports = "8888 9999"
    openports = OpenPort(ports)
    a = threading.Thread(target=openports.createsocket())
    a.start()
    a.join()