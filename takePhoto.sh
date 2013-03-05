#works well at about 6cm
cd ~/timelapse
rm -f capt0000.jpg
time=25 # 1/20s
shootmode=1 #time priority
gphoto2 --set-config /main/capturesettings/shootingmode=$shootmode \
	--set-config /main/capturesettings/shutterspeed=$time \
	--set-config /main/capturesettings/focusingpoint=0 \
	--set-config /main/capturesettings/afdistance=0 \
	--capture-image-and-download \
    --quiet
mv capt0000.jpg images/$(date +%y-%m-%d-%H-%M-%S).jpg
