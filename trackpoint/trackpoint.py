#! /usr/bin/python2

import os
import shutil
from myconfig import *
import sys

gTemp="/tmp/trackpoint"
gPath="/sys/devices/platform/i8042/serio1"

#def init():
#    try:
#        cfg_file = open(gCfg)
#    except IOError as e:
#        print 'No config file found!'

def backup():
    if not os.path.isdir(gTemp):
        os.mkdir(gTemp)
    shutil.copy(gPath+'/press_to_select',gTemp)
    shutil.copy(gPath+'/sensitivity'    ,gTemp)
    shutil.copy(gPath+'/speed'          ,gTemp)

def restore():
    if not os.path.isdir(gTemp):
        return 1
    shutil.copy(gTemp,gPath+'/press_to_select')
    shutil.copy(gTemp,gPath+'/sensitivity'    )
    shutil.copy(gTemp,gPath+'/speed'          )

def start():
    if gEnable == 1:
        print "Setting trackpoint values"
        backup()

        fout = open(gPath+'/press_to_select','w')
        if gPress_to_select == 1:
            fout.writelines('1')
        else:
            fout.writelines('0')
        fout.close()

        fout = open(gPath+'/sensitivity','w')
        if gSensitivity:
            fout.writelines(str(gSensitivity))
        fout.close()

        fout = open(gPath+'/speed','w')
        if gSpeed:
            fout.writelines(str(gSpeed))
        fout.close()
    print 'Done'

def stop():
    print 'Restoring the previous values'
    restore()
    print 'Done'

def restart():
    stop()
    start()

if sys.argv[1] == "start":
    start()
elif sys.argv[1] == "restart":
    restart()
elif sys.argv[1] == "stop":
    stop()

# vim: tw=88
