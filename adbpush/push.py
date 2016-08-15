#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import os.path
import json
import fnmatch
import sys
import getopt


class Adb(object):
    """docstring for ClassName"""

    def __init__(self):
        super(Adb, self).__init__()

    def pushfiles(self, path, targets):
        for target in targets:
            for filename in iterfindfiles(path, target):
                self.pushfile(filename)

    def pushfile(self, filename):
        from_name = filename[len(os.path.abspath('.')) + 1:]
        to_name = filename[len(os.path.abspath('..')):]
        command = 'adb push ' + from_name + ' ' + to_name
        print command
        os.system(command)


def iterfindfiles(path, fnexp):
    for root, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, fnexp):
            yield os.path.join(root, filename)


def loadconfig(configpath):
    json_str = ''
    with open(configpath, 'r') as f:
        for line in f.readlines():
            if line.strip().startswith('#'):
                continue
            json_str = json_str + line
    return json_str


def getAllTargets(json_str):
    for dic in json.loads(json_str)['files']:
        yield dic['name']


def parse_params():
    param_path = ''
    target_all = False
    opts, args = getopt.getopt(sys.argv[1:], "ap:")
    for op, value in opts:
        if op == "-a":
            target_all = True
        if op == "-p":
            param_path = os.path.abspath(value.strip())
    return target_all, param_path


def main():
    target_all, param_path = parse_params()
    if target_all:
        target_files = getAllTargets(loadconfig(
            '/home/yumiao/script_py/push_config'))
    else:
        target_files = ['services.jar']

    os.system("adb remount")
    adb_ins = Adb()
    adb_ins.pushfiles(param_path, target_files)
    os.system("adb reboot")

if __name__ == '__main__':
    main()
