import numpy as np
import pylab as py

class EyeTracker(object):
    def __init__(self):
        self.x = 5
        self.y = 5
        
    def run(self):
        py.figure(dpi = 110, figsize = (12,6))
        py.ion()
        self.display()
        
    def display(self):    
        board = np.zeros((11, 11))
        board[self.x][self.y] = 1
                   
        py.clf()
        py.imshow(board,
                cmap = py.cm.Greens,
                interpolation = 'nearest')
        py.draw()
            
    def move_square(self, decision):
        """
        """
        if decision == "u":
            self.x = (self.x - 1) % 11
        elif decision == "d":
            self.x = (self.x + 1) % 11
        elif decision == "l":
            self.y = (self.y - 1) % 11
        elif decision == "r":
            self.y = (self.y + 1) % 11
        self.display()
                
