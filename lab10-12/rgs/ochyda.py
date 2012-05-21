import numpy as np
import pylab as py
import random
import time


lista = range(26)

py.ion()
py.clf()

typy = []
while lista:
       rand = random.randint(0,len(lista)-1)
       
       if rand < 13:
            typy.append('neutral')
       else:
            typy.append('emo')         
             
       imnr = str(lista.pop(rand)) + '.jpg'
       im = py.imread(imnr)
       py.imshow(im,origin = 'lower')
       py.draw()
       raw_input('nacisnij enter')
       py.clf()

print typy       
File_name = 'emo.dat'    
with open(File_name, 'w') as f:
     for i in  typy:
        f.write("%s\n" % i)
    
py.show()
