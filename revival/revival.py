#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Created on 2016年8月8日
    @author: yumiao

    command:
        initEnv: revival.py -i
        Record:  revival.py -w -p file[file_path]
        Revival: revival.py -r -p file[file_path] -c 5[retry]
'''

import os
import os.path
import sys
import getopt


def exit():
    sys.exit()


def excute_command(command, log=False):
    # print command
    if not log:
        os.system(command + " 1>/dev/null")
    else:
        os.system(command)


def startRevival(command_path, retry):
    excute_command('adb push ' + command_path + ' ' + "/sdcard/command")
    excute_command('adb shell revival read -c ' + retry, True)
    clearTempFile()


def startRecord(command_path):
    excute_command('adb shell revival write', True)
    excute_command('adb pull ' + "/sdcard/command" + ' ' + command_path)
    clearTempFile()


def clearTempFile():
    excute_command('adb shell rm ' + "/sdcard/command")


def adjustFilePath(command_path):
    return os.path.abspath(command_path)


def init_environment():
    excute_command(
        'adb root && adb remount && adb push revival ' + "/system/bin/")
    excute_command('adb shell chmod 755 /system/bin/revival')
    excute_command('adb shell chown root:shell /system/bin/revival')


def parse_params():
    opts, args = getopt.getopt(sys.argv[1:], "iwrp:c:m:")
    init = False
    record = False
    revival = False
    param_path = None
    retry = None
    msg = None
    for op, value in opts:
        if op == "-i":
            init = True
        if op == "-w":
            record = True
        if op == "-r":
            revival = True
        if op == "-p":
            param_path = value.strip()
        if op == "-c":
            retry = value.strip()
        if op == "-m":
            msg = value.strip()
    return init, record, revival, param_path, retry, msg


def check_params(record, revival, param_path, retry):
    ret = True
    if record and revival:
        print "only support one command at once."
        ret = False
    elif record and param_path is None:
        print "please input the file path to save the recorded command."
        ret = False
    elif revival and param_path is None:
        print "Please input the command file path you want to revival."
        ret = False
    elif revival and not retry.isdigit():
        print "Invalid retry number, Please input a integer."
        ret = False
    return ret


def main():
    if len(sys.argv) < 2:
        init = raw_input(
            "Welcome!, do you want to init environment?\n[Yes/No]:")
        if init == 'Yes':
            init_environment()
        command = raw_input(
            "Which command do you want to excute?\n[record/revival]:")
        if 'record' == command:
            file_path = raw_input(
                "Please input the file path to save the recorded command.\n")
            startRecord(adjustFilePath(file_path))
        elif 'revival' == command:
            file_path = raw_input(
                "Please input the command file path you want to revival.\n")
            retry = raw_input(
                "How many times do you want to loop?\nnumber[integer]:")
            if not retry.isdigit():
                print "Invalid number, Please input a integer"
                exit()
            startRevival(adjustFilePath(file_path), retry)
        else:
            print "Sorry, Unknown Command.."
            exit()
    else:
        init, record, revival, param_path, retry, msg = parse_params()
        if msg is not None:
            excute_command("adb shell revival " + msg, True)
            exit()
        if init:
            init_environment()
        if retry is None:
            retry = '1'
        if not check_params(record, revival, param_path, retry):
            exit()
        if record:
            startRecord(adjustFilePath(param_path))
        elif revival:
            startRevival(adjustFilePath(param_path), retry)
        else:
            print "Sorry, Unknown Command.."
            exit()


if __name__ == '__main__':
    main()
