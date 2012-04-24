import numpy as np
import pylab as py
import random
import time

def loslista(dl):
    lista = [random.randint(0,1) for i in xrange(dl)]
    return lista
py.figure(dpi = 120)
py.ion()

py.imshow(np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,1,0,0], [0,0,0,0,0], [0,0,0,0,0]]), cmap = py.cm.Blues, interpolation = 'nearest')
time.sleep(2)

punkty = []
for i in range(75):
    P = random.randint(0,3)
    
    if P == 0:
        M = np.array([[0,0,1,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]])
        T = 'u'
    if P == 1:
        M = np.array([[0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]])
        T = 'l'
    if P == 2:
        M = np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,1,0,0]])
        T = 'd'
    if P == 3:
        M = np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,1], [0,0,0,0,0], [0,0,0,0,0]])
        
        T = 'r'
                
            
    py.clf()
    py.imshow(M, cmap = py.cm.Blues, interpolation = 'nearest')
    py.draw()
    stop = time.time()
    punkty.append((T,stop))   
    time.sleep(2)
    py.clf()
    py.imshow(np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,1,0,0], [0,0,0,0,0], [0,0,0,0,0]]), cmap = py.cm.Blues, interpolation = 'nearest')
    py.draw()
    time.sleep(2)
print punkty
File_name = 'punkty.dat'    
with open(File_name, 'w') as f:
     for i in  punkty:
        f.write("%s, %s \n" % i)
    
py.show()

