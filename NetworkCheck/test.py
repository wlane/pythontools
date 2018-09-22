#!/usr/bin/python
# -*- coding:utf8 -*-

import csv

user_list = csv.reader(open("list_to_user.csv", "r"))    # 读取CSV文件到user_list字典类型变量中

for user in user_list:   # 遍历整个user_list
    sleep(2)
    self.logn_in('admin', 'admin')
    sleep(2)

    user_to_add = {'account': user[0],             # 读取一行csv，并分别赋值到user_to_add 中
                     'realname': user[1],
                     'gender': user[2],
                     'dept': user[3],
                     'role': user[4],
                      'password': user[5],
                      'email': user[0] + user[6]}
    self.add_user(user_to_add)