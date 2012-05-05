from threading import Lock, Thread

import numpy as np
import pylab as py
import random
import time
import os

class ImgDisplay(Thread):
    def __init__(self):
        super(ImgDisplay, self).__init__()
        self.position = None
        self.grid = None
        self.lock = Lock()
        
    def run(self):
        self.square_animation()
        
    def square_animation(self):    
        py.figure(dpi = 150, figsize=(12,6))
        py.ion()

        py.imshow(np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,1,0,0], [0,0,0,0,0], [0,0,0,0,0]]),
                cmap = py.cm.Blues,
                interpolation = 'nearest')
        time.sleep(2)
        while True:
            p = random.randint(0,3)
            with self.lock:
                if p == 0:
                    self.grid = np.array([[0,0,1,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]])
                    self.position = "up"
                elif p == 1:
                    self.grid = np.array([[0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]])
                    self.position = "left"
                elif p == 2:
                    self.grid = np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,1,0,0]])
                    self.position = "down"
                elif p == 3:
                    self.grid = np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,1], [0,0,0,0,0], [0,0,0,0,0]])
                    self.position = "right"
                   
            py.clf()

            py.imshow(self.grid, cmap = py.cm.Blues, interpolation = 'nearest')
            py.draw()
            stop = time.time()
               
            time.sleep(2)
            
            py.clf()
            with self.lock:
                self.position = "centre"
                self.grid = np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,1,0,0], [0,0,0,0,0], [0,0,0,0,0]])
            py.imshow(self.grid,
                    cmap = py.cm.Blues,
                    interpolation = 'nearest')
            py.draw()
            
            time.sleep(2)
            
    def get_position(self):
        """
        """
        pos = None
        with self.lock:
            pos = self.position
        return pos

if __name__ == "__main__":
    a = ImgDisplay()
    a.start()
    a.join()
