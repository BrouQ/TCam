#!/bin/bash

modprobe v4l2loopback exclusive_caps=0,0 video_nr=1,2,3
/usr/bin/flirone-v4l2-tcam/flirone /usr/bin/flirone-v4l2-tcam/palettes/Iron2.raw
