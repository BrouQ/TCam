import cv2
#import numpy as np
import os
import time
from pathlib import Path

home = str(Path.home())
os.chdir(home)
print('Working directory changed to: {}'.format(os.getcwd()))


start_time = time.time()

cap = cv2.VideoCapture(3)

# sirka
#cap.set(3,1920)

# vyska
#cap.set(4,1080)

# brightness
#cap.set(10,0)

# pocet fotek
n = 0

while True:
    success, img = cap.read()
    cv2.imshow('Termal', img)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    
    if key == ord('i'):
        n += 1
        print('Foto {}'.format(n))
#        image = np.copy(img)
        image = img.copy()
        cv2.imshow('Image ' + str(n), image)
        
        # save image
        filename = 'data/{}_foto{}.png'.format(start_time, n)
        retval = cv2.imwrite(filename, image)
        if retval == True:        
            print('Image saved :-)')
        else:
            print('Nepovedlo se :-(')
        
