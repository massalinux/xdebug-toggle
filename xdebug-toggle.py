#!/usr/bin/env python
import re
import shutil
import subprocess
import sys
import os

webserver_restart_cmd = "valet restart"
xdebug_file = "/opt/homebrew/etc/php/%s/conf.d/ext-xdebug.ini"


def get_php_version():
    res = subprocess.check_output(["php", "--version"])
    m = re.match(r"PHP (\d+\.\d+).+", res)
    if m:
        return m.group(1)
    else:
        print "Cannot find PHP version"
        exit(-1)


def disable_xdebug(_xdebug_file):
    directory, filename = os.path.split(_xdebug_file)
    shutil.move(_xdebug_file, os.path.join(directory, filename.split(".")[0] + ".disabled"))


def enable_xdebug(_xdebug_file):
    directory, filename = os.path.split(_xdebug_file)
    shutil.move(os.path.join(directory, filename.split(".")[0] + ".disabled"), _xdebug_file)


if __name__ == "__main__":
    output = ""
    php_version = get_php_version()
    xdebug_file = xdebug_file % php_version
    if not xdebug_file:
        output = "xdebug already disabled"
    try:
        if sys.argv[1] == "enable":
            enable_xdebug(xdebug_file)
            os.system(webserver_restart_cmd)
            output = "Xdebug enabled"
        elif sys.argv[1] == "disable":
            disable_xdebug(xdebug_file)
            os.system(webserver_restart_cmd)
            output = "Xdebug disabled"
        else:
            output = "Run with enable or disable"
    except IndexError:
        output = "Run with enable or disable"
    print(output)

