import numpy as np
import pylab as py
import random
import time


#numPlots = 9
#numRows = 3
#numCols = 3
#plt.ion()
#for j in range(5):
        #plt.clf()
        #for i in range(j):
                #plt.subplot(numRows,numCols,i + 1, axisbg='y')
        #plt.draw()
        #plt.clf()
        #time.sleep(2)
 
#plt.show()
#import numpy as np
#import matplotlib.pyplot as plt
 
#numPlots = 9
#numRows = 3
#numCols = 3
 
#plt.figure(figsize=(10,10))
 
#for i in range(numPlots):
    #plt.subplot(numRows,numCols,i + 1, axisbg='y')
 
#plt.show()

def loslista(dl):
    lista = [random.randint(0,1) for i in xrange(dl)]
    return lista

py.ion()

krzyzyki = []
for i in range(300):
    T = 0
    P = random.randint(0,4)
    
    if P == 0:
        M = np.array([[0,1,0], [1,1,1], [0,1,0]])
    else:
        M = np.array([loslista(3), loslista(3), loslista(3)])
        
    if np.all(M == np.array([[0,1,0], [1,1,1], [0,1,0]])):
        print 'T'
        T = 1

            
    py.clf()
    py.imshow(M, cmap = py.cm.Blues, interpolation = 'nearest')
    py.draw()
    stop = time.time()
    if T:
        krzyzyki.append(stop)
        T = 0    
    time.sleep(1)
    py.clf()
    py.imshow(np.zeros((3,3)), cmap = py.cm.Blues, interpolation = 'nearest')
    py.draw()
    time.sleep(1)
print krzyzyki
File_name = 'krzyze.dat'    
with open(File_name, 'w') as f:
     for i in  krzyzyki:
        f.write("%s\n" % i)
    
py.show()

