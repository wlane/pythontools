#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlsxwriter
import ast


class WriteToExcel(object):     # 将相应内容写入到excel文档的类

    def __init__(self, workbookname):   # 初始化
        self.workbookname = workbookname

    def writeinband(self, localhostip, **data):     # 写入excel
        # reload(sys)
        # sys.setdefaultencoding('utf-8')
        try:
            titleband = [u'时间间隔\主机']
            titlenet = [u'测试地址', u'丢包率', u'rtt最大时长(ms)', u'rtt最小时长(ms)', u'rtt平均时间(ms)']
            titleport = [u'测试端口', u'是否对外开放']
            bandlocal = [u'本地主机', localhostip]
            testaddress = ['114.114.114.114', 'www.baidu.com']
            testport = []
            portconn = []

            for host in ast.literal_eval(data["otherhost"]):
                if host == 'localhost':
                    bandlocal = [u'本地主机', 'localhost']
                else:
                    titleband.append(host)      # 除本机外的其他主机

            workbook = xlsxwriter.Workbook(self.workbookname)       # 生成名为workbookname的excel文档
            bandworksheet = workbook.add_worksheet(u'带宽')   # 增加一个叫带宽的sheet
            networksheet = workbook.add_worksheet(u'外网连接状态')    # 增加一个叫外网连连接状态的sheet
            portworksheet = workbook.add_worksheet(u'端口开放情况')   # 增加一个叫端口开放情况的sheet

            format_title = workbook.add_format()    # excel文档的格式设置
            format_title.set_border(1)
            format_title.set_bg_color('#cccccc')
            format_title.set_align('center')
            format_title.set_bold()

            bandworksheet.write_row('A1', bandlocal, format_title)  # 添加带宽sheet的内容
            bandworksheet.write_row('A2', titleband, format_title)
            line = 3
            t = ast.literal_eval(data["bandvalue"])
            for v_t in t:
                bandworksheet.write_row('A'+str(line), v_t, format_title)
                line = line+1

            wline = 0       # 添加外网连接状态sheet的内容
            t = ast.literal_eval(data["pingstatus"])
            for v_t in t:
                netlocalhost = [u'测试主机', v_t ]
                pnum = 0
                while pnum < 2:
                    networksheet.write_row('A'+str(wline+1), netlocalhost, format_title)
                    networksheet.write_row('A'+str(wline+2), titlenet, format_title)
                    networksheet.write_column('A'+str(wline+3), testaddress, format_title)
                    networksheet.write_row('B'+str(wline+3+pnum), ast.literal_eval(data["pingstatus"])[v_t][pnum], format_title)
                    pnum += 1
                wline += 4

            for p in ast.literal_eval(data["portconnect"]).keys():      # 添加端口开放情况sheet的内容
                testport.append(p)
                portconn.append(ast.literal_eval(data["portconnect"])[p])
            portworksheet.write_row('A1', titleport, format_title)
            portworksheet.write_column('A2', testport, format_title)
            portworksheet.write_column('B2', portconn, format_title)
            workbook.close()
        except Exception, err:      # 出错处理
            print "%s\tError:\n" % self.workbookname
            print err
