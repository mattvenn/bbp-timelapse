#!/usr/bin/python

import datetime
import os
path = "/home/bristolbikeproject/timelapse/images/"

def capture_image():
	now = datetime.datetime.now()
	filename = now.strftime("%y-%m-%d-%H-%M-%S")
	output = path + filename + '.jpg'
	command = "fswebcam --set brightness=50%% --no-banner -r 800x600 -d /dev/video0 %s" % output
	os.system(command)	


if __name__=="__main__":  
	capture_image()
