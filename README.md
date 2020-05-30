# TCam (Threma Camera DIY)
- thermal camera: FliroOne gen2, micro-usb
- platform: ubuntu 18.04 x64
- conditions:
  - be sure there is no camera on /dev/video[1,2,3]

## install guide

### Installing Prerequisites
'''
sudo apt update
sudo apt upgrade
sudo apt install htop vim tree cheese python3 dkms git make gcc libjpeg-dev ffmpeg vlc linux-image-generic libusb-1.0-0-dev
sudo reboot
uname -a
sudo apt install linux-headers-x.xx.x-xx-generic
sudo apt autoremove
'''

### Clone Project TCam
'''
cd ~/
git clone https://github.com/BrouQ/TCam.git
cd ~/TCam
'''

### Install v4l2loopback
- original at: git clone https://github.com/umlaeute/v4l2loopback.git
- no changes in project copy of folder
'''
cd ~/TCam/v4l2loopback/
make
sudo make install
sudo depmod -a
cd ..
'''

### Install flirone driver
- original at: git clone https://github.com/fnoop/flirone-v4l2.git
- changed flirone-v4l2.c for this project
'''
cd ~/TCam/flirone-v4l2/
make
sudo mv ~/TCam/flirone-v4l2 /usr/bin/
cd ..
'''

### Install TCam service
'''
sudo cp ~/TCam/tcam-start.sh /usr/bin/tcam-start.sh
sudo chmod +x /usr/bin/tcam-start.sh
sudo cp ~/TCam/tcam.service /etc/systemd/system/
sudo systemctl enable tcam
'''

## info

### Manage TCam service
'''
sudo systemctl start tcam
sudo systemctl restart tcam
sudo systemctl stop tcam
systemctl enable tcam
systemctl disable tcam
'''

### Tests
'''
sudo modprobe v4l2loopback exclusive_caps=0,0 video_nr=1,2,3
/usr/bin/flirone-v4l2/flirone /usr/bin/flirone-v4l2/palettes/Iron2.raw
ffmpeg -f v4l2 -r 9 -s 640x480 -i /dev/video3 thermal.avi
'''

### Files and Folders
* ~/TCam/scripts
  * all develelpment scripts
* tcam.service
  * definition of service for systemd
* tcam-start.sh
  * is called by tcam.service
  * define camera pallete

###  Git Help
- https://wiki.debian.org/UsingGit
- https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax
git status
git config --global user.email "you@example.com"
git config --global user.name "Your Name"

git add .
git status
git commit -a -m "Some message"
git diff
git branch new-branch
git checkout new-branch (presun do nove vetve)
git checkout master (spatky do hlavni vetve)
git show-branch
git merge new-branch (marge to mastr)
git remote add origin https://github.com/BrouQ/TCam.git
git push -u origin master

…or push an existing repository from the command line

