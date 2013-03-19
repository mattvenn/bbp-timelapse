#!/usr/bin/python
import os
import Image
import re

path = "/home/bristolbikeproject/timelapse/"
imagepath = path + "images/"

def get_newest():
    filelist = os.listdir(imagepath)
    newest = max(filelist, key=lambda x: os.stat(imagepath+x).st_mtime)
    return newest

def resize(fromfile,to,width):
    try:
        img = Image.open(fromfile)
        isize = img.size
        ratio = float(width) / isize[0]
        newimg = img.resize((int(isize[0]*ratio),int(isize[1]*ratio)),Image.ANTIALIAS)
        newimg.save(to,"JPEG")
    except IOError:
        print "cannot create thumbnail for %s" % fromfile
    
def scp(fromfile,to):
    command = "scp %s bbp@mattvenn.net:~/timelapse/%s" % ( fromfile, to )
    print command
    os.system(command)
    print "done"

def mk_youtube():
    f = open(path + "latest_vid")
    link = f.read()
    f.close()
    f = open(path + "youtube.html",'w')
    m = re.search('watch\?v=([^&]+)&feature',link)
    embed=m.group(1)
    print "using %s as embed" % embed
    f.write("""
<html>
<head>
<style> html, body {margin:0;padding:0;} </style>
</head>
<body>
<iframe width="600" height="450" src="http://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>
</body>
</html>""" % (embed))
    f.close()

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

    #resize for thumbnail
    small_img_path = path + "latest-296.jpg"
    resize(imagepath + newest, small_img_path, 296)

    #scp the photo
    scp(small_img_path,"latest-296.jpg")

    #not making index anymore as going on the bbp website
    #the index
    #mk_index(newest)

    #the youtube embed page
    mk_youtube()
    scp(path + "youtube.html", "youtube.html")
