#! /usr/bin/env python

import sys

def set_thresh(bat,low,high):
    smapi_dir = ("/sys/devices/platform/smapi/BAT")
    low_path = smapi_dir + bat + "/start_charge_thresh"
    high_path = smapi_dir + bat + "/stop_charge_thresh"
    try:
        with open(low_path, 'w') as a, open(high_path, 'w') as b:
            a.writelines(str(low))
            b.writelines(str(high))

            return 0
    except IOError as e:
        print("""tp_smapi could not be interfaced.

Please ensure that tp_smapi module is loaded and you are executing the
script as root, or your user has write permissions to the following
files:

    /sys/devices/platform/smapi/BAT{0,1}/{start,stop}_charge_thresh

Operation failed: %s
""" % e.strerror)

        return 1

def print_help():
    print("""
Please specify three parameters as follows:

    ./smapi.py BAT LOWER UPPER

Where the meanings of parameters are:

    BAT - The index of the battery you want to switch
    LOW - Start charging when it has less than LOW % of charge left
    HIGH - Stop charging when it has HIGH % of charge left

Example:

    ./smapi.py 0 40 80

NOTE: For the program to run properly you need tp_smapi kernel module
with py3k working on your system.
""")

if len(sys.argv) == 4:
    set_thresh(sys.argv[1],sys.argv[2],sys.argv[3])
else:
    print_help()

# vim: tw=72:shiftwidth=4
