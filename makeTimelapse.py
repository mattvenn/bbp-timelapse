#!/usr/bin/python
import os

path = "/home/bristolbikeproject/timelapse/"
imagepath = path + "images/"

def make_filelist():
	filelist = os.listdir(imagepath)
	f = open("files.txt",'w')
	for file in filelist:
		f.write(imagepath + file + "\n")
	f.close()

def make_timelapse():
	command = "mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4 -o test.avi -mf type=jpeg:fps=10 mf://@files.txt"
	os.system(command)

if __name__=="__main__":  
	make_filelist()
	make_timelapse()

