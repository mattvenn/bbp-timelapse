#!/usr/bin/python

import pickle
import datetime
import os
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
path = "/home/bristolbikeproject/timelapse/"
image_path = path + "images/"
state = "state"

def add_text_to_image(filename):
    img = Image.open(filename)
    now = datetime.datetime.now()
    text = now.strftime("%H:%M %A")
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf",100)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0,0,750,150],fill=(0,0,0))
    draw.text((10, 10),text,(255,255,255),font=font)
    img.save(filename,"JPEG")

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
    return (status,output)

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
    (status,filename) = capture_image()
    if status == 0:
        print "took photo %d" % num
        write_pic_number(num+1)
        #add text
        add_text_to_image(filename)
