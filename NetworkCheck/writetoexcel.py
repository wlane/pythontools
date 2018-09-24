#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlsxwriter

title = [u'业务流量', u'星期一', u'星期二', u'星期三', u'星期四', u'星期五', u'星期六', u'星期日', u'平均流量']
buname = [u'业务官网', u'新闻中心', u'购物频道', u'体育频道', u'亲子频道']

workbook = xlsxwriter.Workbook('test.xlsx')
worksheet = workbook.add_worksheet('result')
# worksheet.set_column('A:A', 20)
# bold = workbook.add_format({'bold': True})
format_title = workbook.add_format()
format_title.set_border(1)
format_title.set_bg_color('#cccccc')
format_title.set_align('center')
format_title.set_bold()

worksheet.write_row('A1', title, format_title)
worksheet.write_column('A2', buname, format_title)

workbook.close()
