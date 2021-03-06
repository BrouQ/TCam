# TCam (Thermal Camera DIY)
- thermal camera: FlirOne gen2, micro-usb
- platform: ubuntu 18.04 x64
- conditions:
  - be sure there is no camera on /dev/video[1,2,3]

## install guide

### Installing Prerequisities
```
sudo apt update
sudo apt upgrade
sudo reboot

sudo apt install htop vim tree cheese python3 dkms git make gcc libjpeg-dev ffmpeg vlc linux-image-generic libusb-1.0-0-dev python3-opencv python3-numpy python3-matplotlib
sudo apt install --reinstall linux-headers-`uname -r`
sudo apt autoremove
```

### Clone Project TCam
```
cd ~/
git clone https://github.com/BrouQ/TCam.git
cd ~/TCam
```

### Install v4l2loopback
- original at: https://github.com/umlaeute/v4l2loopback.git
- no changes in project copy of folder
```
cd ~/TCam/v4l2loopback/
make
sudo make install
sudo depmod -a
cd ..
```

### Install flirone driver
- original at: https://github.com/fnoop/flirone-v4l2.git
- changed src/flirone.c for this project
```
cd ~/TCam/flirone-v4l2-tcam/
make
sudo cp -R ~/TCam/flirone-v4l2-tcam /usr/bin/
cd ..
```

### Install TCam service
```
sudo cp ~/TCam/tcam-start.sh /usr/bin/tcam-start.sh
sudo chmod +x /usr/bin/tcam-start.sh
sudo cp ~/TCam/tcam.service /etc/systemd/system/
sudo systemctl enable tcam
```

## info

### Manage TCam service
```
sudo systemctl start tcam
sudo systemctl restart tcam
sudo systemctl stop tcam
systemctl enable tcam
systemctl disable tcam
```

### use flirone without service
```
sudo modprobe v4l2loopback exclusive_caps=0,0 video_nr=1,2,3
sudo /usr/bin/flirone-v4l2-tcam/flirone /usr/bin/flirone-v4l2-tcam/palettes/Iron2.raw
```

### Tests
```
ffmpeg -f v4l2 -r 9 -s 640x480 -i /dev/video3 thermal.avi
python3 ~/TCam/scripts/test1.py
```

### Files and Folders
* flirone-v4l2-tcam/
  * flir one driver, allow access to video stream on /dev/video2 and /dev/video3
* scripts/
  * include all development scripts
* v4l2loopback/
  * kernel module for virtual video
* tcam.service
  * definition of service for systemd
* tcam-start.sh
  * is called by tcam.service
  * define camera pallete

###  Git Help
- https://wiki.debian.org/UsingGit
- https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax
```
git config --global user.email "you@example.com"
git config --global user.name "Your Name"

git status
git add .
git status
git commit -a -m "Some message"
git push -u origin master

git diff
git branch new-branch
git checkout new-branch (presun do nove vetve)
git checkout master (spatky do hlavni vetve)
git show-branch
git merge new-branch (marge to mastr)
```
