#works well at about 6cm
time=0.5
shootmode=TV #time priority
gphoto2 --set-config-value /main/capturesettings/shootingmode=$shootmode \
	--set-config-value /main/capturesettings/shutterspeed=$time \
	--capture-image-and-download \
