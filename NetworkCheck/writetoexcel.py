#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlsxwriter
import time
import ast
import sys

class WriteToExcel(object):

    def __init__(self,workbookname ):
        self.workbookname = workbookname

    def writeinband(self, localhostip, **data):
            #reload(sys)
        #sys.setdefaultencoding('utf-8')
        # try:
            titleband = [u'时间间隔\主机']
            titlenet = [u'测试地址', u'丢包率', u'rtt最大时长', u'rtt最小时长', u'rtt平均时间']
            titleport = [u'测试端口', u'是否对外开放']
            bandlocal = [u'本地主机',localhostip]
            testaddress = ['www.baidu.com', '114.114.114.114']
            netlocalhost = [u'测试主机', '192.168.0.193']    # 填写对外开放的云服务器地址
            testport = []
            portconn = []

            for host in ast.literal_eval(data["otherhost"]):
                if host == 'localhost':
                    bandlocal = [u'本地主机', 'localhost']
                else:
                    titleband.append(host)

            workbook = xlsxwriter.Workbook(self.workbookname)
            bandworksheet = workbook.add_worksheet(u'带宽')
            networksheet = workbook.add_worksheet(u'外网连接状态')
            portworksheet = workbook.add_worksheet(u'端口开放情况')

            format_title = workbook.add_format()
            format_title.set_border(1)
            format_title.set_bg_color('#cccccc')
            format_title.set_align('center')
            format_title.set_bold()

            bandworksheet.write_row('A1', bandlocal, format_title)
            bandworksheet.write_row('A2', titleband, format_title)
            line = 3
            t = ast.literal_eval(data["bandvalue"])
            print "t= "
            print t
            for v_t in t:
                bandworksheet.write_row('A'+str(line), v_t, format_title)
                line = line+1
                print line

            networksheet.write_row('A1', netlocalhost, format_title)
            networksheet.write_row('A2', titlenet, format_title)
            networksheet.write_column('A3', testaddress, format_title)
            line = 3
            t = ast.literal_eval(data["192.168.0.193"])
            for v_t in t:
                networksheet.write_row('B'+str(line), v_t, format_title)
                line += 1
                print line

            for p in ast.literal_eval(data["portconnect"]).keys():
                print "p========"
                print p, ast.literal_eval(data["portconnect"])[p]
                print ast.literal_eval(data["portconnect"])[p].decode('utf-8')
                testport.append(p)
                portconn.append(ast.literal_eval(data["portconnect"])[p].decode('utf-8'))

            portworksheet.write_row('A1', titleport, format_title)
            portworksheet.write_column('A2', testport, format_title)
            portworksheet.write_column('B2', portconn, format_title)
            workbook.close()
        # except:
        #     print "%s\tError\n" % self.workbookname


if __name__ == '__main__':
    val = u'可达'
    v1 = val.encode('utf-8')
    print v1
    a = WriteToExcel(time.strftime("%Y-%m-%d-%H-%M", time.localtime())+"-网络测试.xlsx")
    localip = '10.0.16.55'
    dt = {
        "bandvalue": "[['0.0-5.0 sec', '94.2 Mbits/sec', '5.6 Mbits/sec'], ['5.0-10.0 sec', '92.2 Mbits/sec'], ['0.0-10.0 sec', '93.2 Mbits/sec']]",
        "otherhost": "['192.168.0.193', '192.168.0.233']",
        "portconnect": "{'8000': '可达','7001': '不可达'}",
        "192.168.0.193": "[['100%', 'null', 'null', 'null'], ['0%', '7.8 ms', '88.5 ms', '9.0 ms']]"
    }
    a.writeinband(localip, **dt)
