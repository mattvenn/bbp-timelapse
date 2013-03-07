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
    print command
    os.system(command)
    print "done"

def mk_index(fromfile):
    f = open(path + "latest_vid")
    link = f.read()
    print link
    f.close()
    f = open(path + "index.html",'w')
    f.write("""
<html>
<head>
<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
</head>
<body>
<h1>%s - <a href="%s">latest timelapse video</a></h1>
<img src="latest.jpg"> 
<body>
</html>""" % (fromfile, link))
    f.close()
    print "used %s for latest index" % fromfile

if __name__=="__main__":  
    newest = get_newest()
    #the photo
    scp(imagepath + newest,"latest.jpg")
    #the index
    mk_index(newest)
    scp(path + "index.html", "index.html")
