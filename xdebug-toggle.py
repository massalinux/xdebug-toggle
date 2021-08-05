#!/usr/bin/env python
import sys
import os

xdebug_file = "/etc/php/7.3/mods-available/xdebug.ini"
webserver_restart_cmd = "sudo systemctl restart apache2"


def run(enable):
    with open(xdebug_file, 'r') as inputfile:
        output = []
        for row in inputfile.readlines():
            if enable:
                output.append(row.replace('#', ''))
            else:
                if not row.startswith("#"):
                    output.append("#%s" % row)
                else:
                    output.append(row)
    with open(xdebug_file, 'w') as outputfile:
        outputfile.writelines(output)


if __name__ == "__main__":
    output = ""
    try:
        if sys.argv[1] == "enable":
            run(True)
            os.system(webserver_restart_cmd)
            output = "Xdebug enabled"
        elif sys.argv[1] == "disable":
            run(False)
            os.system(webserver_restart_cmd)
            output = "Xdebug disabled"
        else:
            output = "Run with enable or disable"
    except IndexError:
        output = "Run with enable or disable"
    print(output)

