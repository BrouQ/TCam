'''
- skript pousti ovladac a pote zobrazuje video
- pokud se kamera nepripoji, ovladac se bezpecne ukonci
- klavesou "i" se uklada obrazek do slozky data
- klavesou "q" se ukonci skript, ovladac se bezpecne ukonci
'''

import time
import cv2
import numpy as np
import os
import subprocess

#======================================================

folder_driver = '/home/linux/flirone-v4l2'
palette = 'palettes/Iron2.raw'
folder_out = '/home/linux/scripts/data'
camera = 3

#======================================================

start_time = time.time()

# driver
os.chdir(folder_driver)
print('Working directory changed to: {}'.format(os.getcwd()))
print('Driver starting...')
driver = subprocess.Popen(['./flirone', palette])

print('Waiting...')
time.sleep(5)

cap = None

# kamera
try:
    cap = cv2.VideoCapture(camera)
    sirka = int(cap.get(3))
    vyska = int(cap.get(4))
    #brightness = cap.get(10)
      
except:
    driver.terminate()
    print('Driver stop')
  
if cap != None:

    print('Format: {}x{}'.format(sirka, vyska))

    # prazdny obrazek
    img = np.zeros((vyska, sirka, 3), np.uint8)

    n = 0

    while True:

        success, img = cap.read()
        
        if success:
            cv2.imshow('Video', img)

        key = cv2.waitKey(1) & 0xFF

        # quit
        if key == ord('q'):
            driver.terminate()
            print('Driver stop')
            break
        
        # uloz obrazek
        if key == ord('i'):
            n += 1
            print('Foto {}'.format(n))
            image = img.copy()
            cv2.imshow('Image ' + str(n), image)
            
            filename = '{}/{}_foto{}.png'.format(folder_out, start_time, n)
            retval = cv2.imwrite(filename, image)
            if retval == True:        
                print('Image saved :-)')
            else:
                print('Nepovedlo se :-(')

    print('Konec')

