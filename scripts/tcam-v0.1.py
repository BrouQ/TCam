# tcam v0.1

import cv2
import os
import time
from pathlib import Path

home = str(Path.home())
os.chdir(home + "/TCam/scripts/")
print('Working directory changed to: {}'.format(os.getcwd()))

start_time = time.time()

cap_t = cv2.VideoCapture(3) # thermal camera
cap_v = cv2.VideoCapture(2) # visible camera

#cap.set(3,1920) # sirka
#cap.set(4,1080) # vyska
#cap.set(10,0) # brightness

n = 0 # pocet fotek

while True:
    success_t, img_t = cap_t.read()
    success_v, img_v = cap_v.read()
    image_t_cropped = img_t[0:120, 0:160]
    image_t_cropped_resized = cv2.resize(image_t_cropped, (img_v.shape[1],img_v.shape[0]))
    
    alpha = 0.5
    beta = (1.0 - alpha)
    tmp = cv2.addWeighted(img_v, alpha, image_t_cropped_resized, beta, 0.0)

    #cv2.imshow('Termal', img_t)
    cv2.imshow("Visible", img_v)
    #cv2.imshow("Thermal Cropped Image " + str(n), image_t_cropped)
    cv2.imshow("Thermal Cropped Resized Image " + str(n), image_t_cropped_resized)
    cv2.imshow("Alpha", tmp)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        cv2.destroyAllWindows()        
        break
    
    if key == ord('i'):
        n += 1
        print('Foto {}'.format(n))

        image_t = img_t.copy()
        image_v = img_v.copy()

        cv2.imshow('Thermal Image ' + str(n), image_t_cropped_resized)
        cv2.imshow("Visible Image " + str(n), image_v)

        # save image
        filename_t = 'data/{}_T_foto{}.png'.format(start_time, n)
        retval_t = cv2.imwrite(filename_t, image_t_cropped_resized)
        filename_v = 'data/{}_V_foto{}.png'.format(start_time, n)
        retval_v = cv2.imwrite(filename_v, image_v)
        
        if retval_t == True and retval_v == True:        
            print('Images saved :-)')
        else:
            print('Nepovedlo se :-(')
        
