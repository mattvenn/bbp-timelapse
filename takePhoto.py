#!/usr/bin/python

import pickle
import datetime
import os
path = "/home/bristolbikeproject/timelapse/"
image_path = path + "images/"
state = "state"

def capture_image():
    now = datetime.datetime.now()
    filename = now.strftime("%Y-%m-%d-%H-%M-%S")
    output = image_path + filename + '.jpg'
    time=25 # 1/20s
    shootmode=1 #time priority
    command = """gphoto2 --set-config /main/capturesettings/shootingmode=%d \
--set-config /main/capturesettings/shutterspeed=%d \
--set-config /main/capturesettings/focusingpoint=0 \
--set-config /main/capturesettings/afdistance=0 \
--capture-image-and-download \
--quiet \
--filename %s
    """ % (shootmode,time,output)

    status = os.system(command)  
    return status

def get_pic_number():
    try:
        f = open(path+state)
        num = pickle.load(f)
    except IOError:
        num = 0
    return num
   
def write_pic_number(num):
    f = open(path+state,'w')
    pickle.dump(num,f)

if __name__=="__main__":  
    num = get_pic_number()
    if capture_image() == 0:
        print "took photo %d" % num
        write_pic_number(num+1)
