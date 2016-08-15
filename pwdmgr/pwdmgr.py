#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
import crypto
import os
import os.path
import getopt
import getpass

'''
    Created on 2016年8月13日
    @author: yumiao

    command:
        addSiteUserPwd: pwdmgr.py -w -p[path][option]
        getSiteUserPwd: pwdmgr.py -r -p[path][option]
    default config path:
        /home/yumiao/script_py/pwdmgr/userpwd_config
'''


def loadConfigFile(configpath):
    json_str = ''
    with open(configpath, 'r') as f:
        for line in f.readlines():
            if line.strip().startswith('#'):
                continue
            json_str = json_str + line
    return json_str


def writeConfigFile(configpath, content):
    with open(configpath, 'w') as f:
        f.write(content)


def addSiteUserPwd(site, user, pwd, configpath):
    json_obj = dict()
    try:
        json_obj = json.loads(loadConfigFile(configpath))
    except Exception:
        pass
    json_obj[site] = dict(username=user, password=pwd)
    writeConfigFile(configpath, json.dumps(json_obj))


def getSiteUserPwd(site, configpath):
    json_obj = json.loads(loadConfigFile(configpath))[site]
    return json_obj['username'], json_obj['password']


def parse_params():
    param_path = ''
    opts, args = getopt.getopt(sys.argv[1:], "rwp:")
    for op, value in opts:
        if op == "-r":
            pass
        if op == "-w":
            pass
        if op == "-p":
            param_path = os.path.abspath(value.strip())
            print param_path


def main():
    configpath = '/home/yumiao/script_py/pwdmgr/userpwd_config'
    read = False
    write = False
    opts, args = getopt.getopt(sys.argv[1:], "rwp:")
    for op, value in opts:
        if op == "-r":
            read = True
        if op == "-w":
            write = True
        if op == "-p":
            configpath = os.path.abspath(value.strip())

    if read:
        queryUserPwd(configpath)
    elif write:
        addRecordMain(configpath)


def addRecordMain(configpath):
    crypto_key = getpass.getpass("Please input the 16bit crypto key:[str]")
    add_site = raw_input("Please input the site to add:[str]")
    add_user = raw_input("Please input the username to add:[str]")
    add_pwd = raw_input("Please input the pwd to add:[str]")
    addSiteUserPwd(add_site, crypto.encrypt(add_user, crypto_key),
                   crypto.encrypt(add_pwd, crypto_key), configpath)


def queryUserPwd(configpath):
    crypto_key = getpass.getpass("Please input the 16bit crypto key:[str]")
    query_site = raw_input("Please input the site to query:[str]")
    username, password = getSiteUserPwd(query_site, configpath)
    print 'Username:%s Password:%s' % (crypto.decrypt(username, crypto_key),
                                       crypto.decrypt(password, crypto_key))

if __name__ == '__main__':
    main()
