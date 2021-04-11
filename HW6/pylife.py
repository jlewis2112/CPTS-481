#! /usr/bin/env python3

"""
Joseph Lewis
HW 6
Game of Life
"""


from tkinter import Tk
from tkinter import Frame
from tkinter import Button
from tkinter import *
import time


            
            
            
#class cell array which stores the cells
class CellArray():
    def __init__(self): #first make them all dead
        self.grid = [[0 for y in range(20)] for x in range(20)]
     
    #function after clear key is pressed   
    def clear(self):
        self.grid = [[0 for y in range(20)] for x in range(20)]
    
    #if the key is pressed on a cell update it
    def clicked(self, locx, locy):
        if((self.grid)[locx][locy] == 0):
            (self.grid)[locx][locy] = 1
        else:
            (self.grid)[locx][locy] = 0
    
    
    def ifAlive(self, locx, locy):
        if self.grid[locx][locy] == 1:
            return True
        else:
            return False

    def countN(self, locx, locy):
        count = 0
        if(locx > 0):
            if((self.grid)[locx-1][locy] == 1):
                count += 1
        if(locy > 0):
            if((self.grid)[locx][locy-1] == 1):
                count += 1
        if(locx < 19):
            if((self.grid)[locx+1][locy] == 1):
                count += 1
        if(locy < 19):
            if((self.grid)[locx][locy+1] == 1): 
                count += 1
        if(locx > 0 and locy > 0):
            if((self.grid)[locx-1][locy-1] == 1):
                count += 1
        if(locx > 0 and locy < 19):
            if((self.grid)[locx-1][locy+1] == 1):
                count += 1
        if(locx < 19 and locy > 0):
            if((self.grid)[locx+1][locy-1] == 1):
                count += 1
        if(locx < 19 and locy < 19):
            if((self.grid)[locx+1][locy+1] == 1): 
                count += 1
        return count
      
      

    def step(self):
        x = 0
        y = 0
        record = [[0 for x in range(20)] for y in range(20)]
        while x < 20:
            y = 0
            while y < 20:
                neighbors = self.countN(x, y)
                if neighbors > 3:
                    record[x][y] = 0
                elif self.grid[x][y] == 0:
                    if neighbors == 3:
                        record[x][y] = 1
                    else:
                        record[x][y] = 0
                else:
                    if neighbors == 2 or neighbors == 3:
                        record[x][y] = 1
                    else:
                        record[x][y] = 0
                y += 1
            x += 1
        x = 0
        y = 0
        while x < 20:
            y = 0
            while y < 20:
                self.grid[x][y] = record[x][y]
                y += 1
            x += 1
        




def click(event):
    wd = canvas.winfo_width() / 20
    hi = canvas.winfo_height() / 20
    cl = int(event.x / wd)
    rw = int(event.y / hi)
    board.clicked(cl, rw)
    if(board.ifAlive(cl, rw) == True):
        color_Board[cl][rw] = canvas.create_rectangle(cl*wd, rw*hi, (cl+1)*wd, (rw+1)*hi, fill = "black")
    else:
        canvas.delete(color_Board[cl][rw])
        color_Board[cl][rw] = None


def coloring():
    rw = 0
    cl = 0
    wd = canvas.winfo_width() / 20
    hi = canvas.winfo_height() / 20
    while rw < 20:
        cl = 0
        while cl < 20:
            if(board.ifAlive(cl, rw) == False and color_Board[cl][rw] != None):
                canvas.delete(color_Board[cl][rw])
                color_Board[cl][rw] = None
            elif board.ifAlive(cl, rw):
                color_Board[cl][rw] = canvas.create_rectangle(cl*wd, rw*hi, (cl+1)*wd, (rw+1)*hi, fill = "black")
            cl += 1
        rw += 1

def stepB():
    board.step()
    coloring()

def clear():
    board.clear()
    x = 0
    y = 0
    canvas.delete("all")
    while x < 20:
        y = 0
        while y < 20:
            color_Board[x][y] = None
            y += 1 
        x += 1             
            
#end the program            
def end():
    quit()

def running():
    stepB()
    canvas.update_idletasks()
    root.after(1000, running)
        
board = CellArray()
color_Board = [[None for y in range(20)] for x in range(20)]
root = Tk()
root.title("GAME OF LIFE")
canvas = Canvas(root, width=500, height=500, bg="white", relief='ridge')
canvas.pack()
canvas.bind("<Button-1>", click)

stepper = Button(root, text="STEP", command=stepB)
stepper.pack(side = LEFT, padx = 40)
clearing = Button(root, text="CLEAR", command=clear)
clearing.pack(side = LEFT, padx = 40)
runner = Button(root, text="Run", command = running)
runner.pack(side = LEFT, padx = 40)
exit = Button(root, text="QUIT", command=end)
exit.pack(side = LEFT, padx = 40)
root.mainloop()
