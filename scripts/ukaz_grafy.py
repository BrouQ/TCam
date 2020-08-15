# zobrazuje prubeh z logu tcam-v0.3 ...

import numpy as np
import matplotlib.pyplot as plt

#datafile = "experiment_3-log.csv"
datafile = "log.csv"

data = np.loadtxt(datafile, delimiter="; ", skiprows=1)
data = data[10:,:]

timestamp = data[:,0]
cas = data[:,0] - data[0,0]
cam = data[:,1]
ref = data[:,2]
diff = data[:,3]

'''
plt.figure(1)
plt.plot(cas, cam)
plt.xlabel("čas [s]")
plt.ylabel("teplota [°C]")
plt.title("Kamera")

#plt.figure(2)
plt.plot(cas, ref)
plt.xlabel("čas [s]")
plt.ylabel("teplota [°C]")
plt.title("Čidlo")
'''
#plt.figure(3)
plt.plot(cas, diff)
plt.xlabel("čas [s]")
plt.ylabel("rozdíl v teplotě [°C]")
plt.title("Diference")

plt.show()
