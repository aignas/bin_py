#! /usr/bin/python2

import os
import shutil
import myconfig as g
import sys

#def init():
#    try:
#        cfg_file = open(gCfg)
#    except IOError as e:
#        print 'No config file found!'

def backup():
    if not os.path.isdir(g.Temp):
        os.mkdir(g.Temp)
    shutil.copy(g.Path+'/press_to_select',g.Temp)
    shutil.copy(g.Path+'/sensitivity'    ,g.Temp)
    shutil.copy(g.Path+'/speed'          ,g.Temp)

def restore():
    if not os.path.isdir(g.Temp):
        return 1
    shutil.copy(g.Temp,g.Path+'/press_to_select')
    shutil.copy(g.Temp,g.Path+'/sensitivity'    )
    shutil.copy(g.Temp,g.Path+'/speed'          )

def start():
    if g.Enable == 1:
        print "Setting trackpoint values"
        backup()

        fout = open(g.Path+'/press_to_select','w')
        if g.Press_to_select == 1:
            fout.writelines('1')
        else:
            fout.writelines('0')
        fout.close()

        fout = open(g.Path+'/sensitivity','w')
        if g.Sensitivity:
            fout.writelines(str(g.Sensitivity))
        fout.close()

        fout = open(g.Path+'/speed','w')
        if g.Speed:
            fout.writelines(str(g.Speed))
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
