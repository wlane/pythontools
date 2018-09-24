#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlsxwriter
import time


class WriteToExcel(object):

    def __init__(self,workbookname ):
        self.workbookname = workbookname

    def writein(self ,**hostip):
        try:
            for host in hostip.keys():
                if host == 'localhost':
                    localhost = [u'本地主机', host]
                else:
                    title = [u'时间间隔(s)\主机']
                    title.append(hostip[host])
            interval = ['0-5', '5-10', u'平均值']

            workbook = xlsxwriter.Workbook(self.workbookname)
            worksheet = workbook.add_worksheet('result')
            # worksheet.set_column('A:A', 20)
            # bold = workbook.add_format({'bold': True})
            format_title = workbook.add_format()
            format_title.set_border(1)
            format_title.set_bg_color('#cccccc')
            format_title.set_align('center')
            format_title.set_bold()

            worksheet.write_row('A1',localhost,format_title)
            worksheet.write_row('A2', title, format_title)
            worksheet.write_column('A3', interval, format_title)

            workbook.close()
        except:
            print "%s\tError\n" % self.ip


if __name__ == '__main__':
    a = WriteToExcel(time.strftime("%Y-%m-%d-%H-%M", time.localtime())+".xlsx")

    a.writein(localhost="10.0.16.55")
