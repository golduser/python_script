#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
import crypto
import os
import os.path
import getopt
import random
import string
import getpass

'''
    Created on 2016年8月14日
    @author: yumiao

    command:
        addTrustUserPwd: pwdgenerator.py -w -t -p[path][option]
        getTrustUserPwd: pwdgenerator.py -r -t -p[path][option]
        getUnTrustUserPwd: pwdgenerator.py -r
    default config path:
        /home/yumiao/script_py/pwdmgr/trust_pwd
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


def getUserPwdList(configpath):
    json_obj = json.loads(loadConfigFile(configpath))
    return [users['item'] for users in json_obj['user_list']], \
        [pwds['item'] for pwds in json_obj['pwd_list']]


def addUserPwdInternal(user, pwd, crypto_key, configpath):
    json_obj = dict()
    try:
        json_obj = json.loads(loadConfigFile(configpath))
    except Exception:
        pass

    if not json_obj.has_key('user_list'):
        json_obj['user_list'] = []
    if not json_obj.has_key('pwd_list'):
        json_obj['pwd_list'] = []
    if not user == '':
        json_obj['user_list'].append(
            dict(item=crypto.encrypt(user, crypto_key)))
    if not pwd == '':
        json_obj['pwd_list'].append(dict(item=crypto.encrypt(pwd, crypto_key)))
    writeConfigFile(configpath, json.dumps(json_obj))


def addUserPwd(configpath):
    crypto_key = getpass.getpass("Please input the 16bit crypto key:[str]")
    add_user = raw_input(
        "Please input the username to add or press Enter to skip:[str]")
    add_pwd = raw_input(
        "Please input the pwd to add or press Enter to skip:[str]")
    addUserPwdInternal(add_user, add_pwd, crypto_key, configpath)


def getUserPwd(configpath):
    crypto_key = getpass.getpass("Please input the 16bit crypto key:[str]")
    user_list, pwd_list = getUserPwdList(configpath)
    user = user_list[random.randint(0, len(user_list) - 1)]
    pwd = pwd_list[random.randint(0, len(pwd_list) - 1)]
    print 'Username:%s Password:%s' % \
        (crypto.decrypt(user, crypto_key),
         crypto.decrypt(pwd, crypto_key))


def main():
    configpath = '/home/yumiao/script_py/pwdmgr/trust_pwd'
    read = False
    write = False
    trust = False
    opts, args = getopt.getopt(sys.argv[1:], "rwtp:")
    for op, value in opts:
        if op == "-r":
            read = True
        if op == "-w":
            write = True
        if op == "-t":
            trust = True
        if op == "-p":
            configpath = os.path.abspath(value.strip())

    if read:
        if trust:
            getUserPwd(configpath)
        else:
            getRandomUserPwd()
    elif write and trust:
        addUserPwd(configpath)


def getRandomUserPwd():
    # 33=! 126=~ 65=A 112=z
    print 'Username:%s Password:%s' % \
        (string.join(random.sample([chr(x) for x in xrange(65, 112)], 8), ''),
         string.join(random.sample([chr(x) for x in xrange(33, 126)], 8), ''))


if __name__ == '__main__':
    main()
