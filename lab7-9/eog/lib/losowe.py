import numpy as np
import pylab as py
import random
import time
import os

class ImgDisplay(object):
    def __init__(self):
        pass
    
    def SquareAnimation(self):    
        py.figure(dpi = 150, figsize=(12,6))
        py.ion()

        py.imshow(np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,1,0,0], [0,0,0,0,0], [0,0,0,0,0]]), cmap = py.cm.Blues, interpolation = 'nearest')
        time.sleep(2)

        #punkty = []
        for i in range(15):
            P = random.randint(0,3)
            
            if P == 0:
                M = np.array([[0,0,1,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]])
                T = 'up'
            if P == 1:
                M = np.array([[0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]])
                T = 'left'
            if P == 2:
                M = np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,1,0,0]])
                T = 'down'
            if P == 3:
                M = np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,1], [0,0,0,0,0], [0,0,0,0,0]])
                
                T = 'right'
                        
                    
            py.clf()
            print T
            py.imshow(M, cmap = py.cm.Blues, interpolation = 'nearest')
            py.draw()
            stop = time.time()
            #punkty.append((T,stop))   
            time.sleep(0.8)
            
            py.clf()
            py.imshow(np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,1,0,0], [0,0,0,0,0], [0,0,0,0,0]]), cmap = py.cm.Blues, interpolation = 'nearest')
            py.draw()
            
            
            time.sleep(2)
            os.system('clear')
        #print punkty
        #File_name = 'punkty.dat'    
        #with open(File_name, 'w') as f:
        #     for i in  punkty:
        #        f.write("%s, %s \n" % i)
            
        py.show()

a = ImgDisplay()
a.SquareAnimation()
