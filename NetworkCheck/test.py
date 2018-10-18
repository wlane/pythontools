#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import time
#
#
# def haha1(max_num):
#     for i in range(max_num):
#         time.sleep(1)
#         print i
#
# def haha2(max_num):
#     for i in range(10, max_num):
#         time.sleep(1)
#         print i
#
#
# if __name__ == '__main__':
#     for x in range(3):
#         t = threading.Thread(target=haha1, args=(10,))
#         s = threading.Thread(target=haha2, args=(20,))
#         #也可以干脆不写这一行
#         # t.setDaemon(True)
#         t.start()
#         t.join()
#         s.start()
#         # s.join()
#     print "test"

#每隔5秒打印时间
def clock(wait_time,n):
    for i in range(n):
        print("The time is %s"%time.ctime())
        print i
        time.sleep(1)

T=[]
for i in range(3):
    t=threading.Thread(target=clock,args=(5,2))
    #t.setDaemon(True)
    t.start()
    t.join()
#     T.append(t)
#
# #等待所有进程结束
# for t in T:
#     t.join()

print("all threads over")
