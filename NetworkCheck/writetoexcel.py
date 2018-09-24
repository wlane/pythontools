#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlsxwriter

class WriteToExcel(object):

    def __init__(self, ip):
        #Thread.__init__(self)
        self.ip = ip

    def writein(self):
        try:
            localhost = [u'本地主机', '10.0.16.55']
            title = [u'时间间隔(s)\主机', '192.168.0.193', '192.168.0.239']
            interval = ['0-5', '5-10', u'平均值']

            workbook = xlsxwriter.Workbook('test.xlsx')
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
