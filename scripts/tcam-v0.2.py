# tcam v0.2
# zobrazuje teplotu prepocitanou z prumerne hodnoty vyrezu z sedeho original obrazku (img_t)
# nacita teplotu ze sondy v oddelenem vlaknu, zobrazuje rozdil hodnoty tepltoy referencni oproti namerene kamerou
# priprava na korekci matice referencni teplotou

import cv2
import os
import time
from pathlib import Path
import numpy as np
import threading

#------------------------------------------------------------------------------

# vycitani teploty z cidla
enable_ref_t = True
file_ref_t = "/sys/bus/w1/devices/28-00000c1370bd/w1_slave"
ref_t = 30 #refencni tepolota z externi sondy, aktualizuje se ve smycce

# kalibrace hodnot na absolutni teploty
value_min = 0
value_max = 255
t_min = 25.0 # temperature corresponding to value_min [deg]
t_max = 49.7 # temperature correcponding to value_max [deg]
a = (t_max - t_min)/(value_max - value_min)
b = t_min - a*value_min


#------------------------------------------------------------------------------

def get_t(value):
    return (a*value+b)

def get_ref_t_thread():
    global ref_t
    while enable_ref_t:
        f=open(file_ref_t, "r")
        for i, line in enumerate(f):
            if i==0:
                valid = line.find("YES") >= 0
            if i==1 and valid:
                ref_t = int(line[line.find("t=")+2:])
                print("referencni teplota: {:.3f}".format(ref_t/1000))
        f.close()            

#------------------------------------------------------------------------------
#                                   MAIN
#------------------------------------------------------------------------------

home = str(Path.home())
os.chdir(home + "/TCam/scripts/")
print('Working directory changed to: {}'.format(os.getcwd()))

start_time = time.time()

cap_t = cv2.VideoCapture(3) # thermal camera
cap_v = cv2.VideoCapture(2) # visible camera

#cap.set(3,1920) # sirka
#cap.set(4,1080) # vyska
#cap.set(10,0) # brightness

n = 0 # citac ulozenych fotek

# spusteni vlakna pro nacitani teploty z cidla
threading.Thread(target=get_ref_t_thread, args=()).start()

while True:
    # vycteni dat z kamery
    success_t, img_t = cap_t.read()
    success_v, img_v = cap_v.read()
    image_t_cropped = img_t[0:120, 0:160]
    
    # vyrez pro urceni referencni teploty    
    p = np.array([[100,90],[130,110]])
    image_t_cropped_copy = np.copy(image_t_cropped)
    image_t_cropped_copy[p[0,1]:p[1,1],   p[0,0]] = 0
    image_t_cropped_copy[p[0,1]:p[1,1]+1, p[1,0]] = 0
    image_t_cropped_copy[p[0,1],          p[0,0]:p[1,0]] = 0
    image_t_cropped_copy[p[1,1],          p[0,0]:p[1,0]+1] = 0
    cv2.imshow('Thermal orig with reference region', image_t_cropped_copy)
    roi = image_t_cropped[p[0,1]:p[1,1], p[0,0]:p[1,0]]
    roi_mean = np.mean(roi)
    roi_t = get_t(roi_mean)
    print('Mean of reference region: {:.1f} = {:.1f} deg'.format(roi_mean, roi_t))
    
    # korekce teploty podle cidla
    #image_t_cropped -= (roi_t - ref_t)
    
    # resize
    image_t_cropped_resized = cv2.resize(image_t_cropped, (img_v.shape[1],img_v.shape[0]))

    # pridani textu do obrazku
    #mujtext = "w: {}, h: {}, t: {:.1f}, ref: {:.3f}".format(image_t_cropped_resized.shape[1], image_t_cropped_resized.shape[0], roi_t, ref_t/1000)
    mujtext = "w: {}, h: {}, rozdil: {:.3f}".format(image_t_cropped_resized.shape[1], image_t_cropped_resized.shape[0], roi_t-ref_t/1000)
    cv2.putText(
      img_v, #numpy array on which text is written
      mujtext, #text
      (10,50), #position at which writing has to start
      cv2.FONT_HERSHEY_SIMPLEX, #font family
      1, #font size
      (209, 80, 0, 255), #font color
      2) #font stroke

    alpha = 0.5
    beta = (1.0 - alpha)
    tmp = cv2.addWeighted(img_v, alpha, image_t_cropped_resized, beta, 0.0)

    # show images
    cv2.imshow('Termal orig', img_t)
    cv2.imshow("Visible", img_v)
    #cv2.imshow("Thermal Cropped Image " + str(n), image_t_cropped)
    cv2.imshow("Thermal Cropped Resized Image " + str(n), image_t_cropped_resized)
    cv2.imshow("Alpha", tmp)


    # ------------------- osetreni vstupu z klavesnice ------------------------
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        enable_ref_t = False
        time.sleep(1)
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
        
