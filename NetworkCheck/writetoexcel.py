#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlsxwriter
import time


class WriteToExcel(object):

    def __init__(self,workbookname ):
        self.workbookname = workbookname

    def writein(self, localhostip, *intervaltime, **hostip):
        try:
            title = [u'时间间隔（s）\主机']
            duration = []
            localdec=[u'本地主机',localhostip]
            for t in intervaltime:
                print t
                duration.append(t)
            for host in hostip.keys():
                if host == 'localhost':
                    localhost = [u'本地主机', hostip[host]]
                else:
                    title.append(hostip[host])
            #interval = ['0-10', '10-20', u'平均值']

            workbook = xlsxwriter.Workbook(self.workbookname)
            worksheet = workbook.add_worksheet('result')
            format_title = workbook.add_format()
            format_title.set_border(1)
            format_title.set_bg_color('#cccccc')
            format_title.set_align('center')
            format_title.set_bold()

            worksheet.write_row('A1',localdec, format_title)
            worksheet.write_row('A2', title, format_title)
            worksheet.write_column('A3', duration, format_title)

            workbook.close()
        except:
            print "%s\tError\n" % self.workbookname


if __name__ == '__main__':
    a = WriteToExcel(time.strftime("%Y-%m-%d-%H-%M", time.localtime())+".xlsx")
    lll = '10.0.16.55'
    aaa = ['0-5', '5-10']
    bbb = {
        'host1': '192',
        'host2': '168'
    }
    a.writein(lll, *aaa, **bbb)
