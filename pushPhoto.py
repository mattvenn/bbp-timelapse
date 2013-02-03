#!/usr/bin/python
import os

path = "/home/bristolbikeproject/timelapse/"
imagepath = path + "images/"

def get_newest():
	filelist = os.listdir(imagepath)
	newest = max(filelist, key=lambda x: os.stat(imagepath+x).st_mtime)
	return newest
	
def scp(fromfile,to):
	command = "scp %s bbp@mattvenn.net:~/timelapse/%s" % ( fromfile, to )
	os.system(command)

def mk_index(fromfile):
	f = open("index.html",'w')
	f.write('<html><img src="latest.jpg"><p>%s</p></html>' % fromfile)
	f.close()

if __name__=="__main__":  
	newest = get_newest()
	#the photo
	scp(imagepath + newest,"latest.jpg")
	#the index
	mk_index(newest)
	scp(path + "index.html", "index.html")
