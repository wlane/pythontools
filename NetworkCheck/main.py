#!/usr/bin/python
# -*- coding:utf-8 -*-


def baseparameters():
    while 1:
        host = raw_input(u'请确认所有linux主机的用户名和密码一致，是否继续（y/n）: ')
        if host == 'y':
            username = raw_input(u'请输入用户名：')
            password = raw_input(u'请输入密码：')
            host = raw_input(u'请输入本机的ip地址：')
            hosts = raw_input(u'请输入远程登陆的ip地址，以空格分开：')
            localhosts[host] = password
            for h in hosts.split():
                remotehosts[h] = password
        else:
            print u"你需要先设置用户名和密码，确保他们在所有linux主机上一致"
            exit(5)
        ifcontinous = raw_input(u'请确认以上输入是否正确（y/n）: ')
        if ifcontinous == 'y':
            break
        else:
            continue


if __name__ == '__main__':
    remotehosts = {}
    localhosts = {}
    username = ''
    password = ''
    baseparameters()


    print username
    print password
    print localhosts
    print remotehosts
