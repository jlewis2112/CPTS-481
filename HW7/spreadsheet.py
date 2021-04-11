#! /usr/bin/env python3

"""
Joseph Lewis
HW 7
Spreadsheet Module
"""

from tkinter import Tk
from tkinter import Frame
from tkinter import Button
from tkinter import messagebox
from tkinter import *
from math import *



class Cell():
    def __init__(self, row, col, equation = "", code = None, value=None):
        self.row = row
        self.col = col
        self.expression = equation
        self.code = code
        self.value = value
        
    def __str__(self):
        return str(self.value)
        
    def __repr__(self):
        return str(self.value)
        
        

class Spreadsheet(Frame):
    def __init__(self, root = None, nRows = 0, nCols = 0):
        Frame.__init__(self, root)
        self.root = root
        self.root.bind("<Return>", self.setCell)
        self.nRows = nRows
        self.nCols = nCols
        lengthX = self.nCols*75 + 40 #use geometry to create length and width
        lengthY = self.nRows*24 + 60
        lw = (str(lengthX)+"x"+str(lengthY))
        root.geometry(lw)
        root.configure(bg='grey')
        self.gridx = [[Cell(r,c) for c in range(nCols)] for r in range(nRows)]
        self.symTable = {}
        self.dependers = {}
        self.board = Frame(self)
        self.board.pack(side='top')
        self.focusBox = Frame(self)
        self.focusBox.pack(side='bottom')
        self.focusBox.focus_set()
        self.focus = ("a", 0)
        self.focusLabel = None
        self.focusEntry = None
        self.remover = None
        self.restore = 0
        #set labels A B C and 1 2 3 ect
        labler = Label(self.board)
        labler.grid(row=0, column=0)
        for x in range(self.nCols):
            colLabel = Label(self.board, text=str(x), borderwidth = 1, relief = "solid", width = 8)
            colLabel.grid(row=0, column=x+1)
        for y in range(self.nRows):
            rowLabel = Label(self.board, text=chr(ord('A')+y), borderwidth = 1, relief = "solid", width = 3)
            rowLabel.grid(row=y+1, column=0)
        # build all of the cells
        for c in range(nCols):
            for r in range(nRows):
                cellx =  Label(self.board, bg="white", borderwidth = 1, relief = "solid", width = 8)
                cellx.grid(row=r+1, column=c+1)
                cellx.bind("<Button-1>", lambda event,rl = r, cl = c: self.setFocus(coords = (rl,cl)))
        #create the focus on the excell sheet
        self.createFocus()
    
    
    def createFocus(self, coords = None, error = None):
        if(error != None):
            self.focusLabel = Label(self.focusBox, text=self.focus[0]+str(self.focus[1])+":", borderwidth = 0, relief = "solid", width = 5)
            self.focusLabel.grid(row=0, column=0)
            self.focusEntry = Entry(self.focusBox, width = 16)
            self.focusEntry.insert(END, str(error))
            self.focusEntry.grid(row = 0, column = 1)
        elif(coords == None):
            self.focusLabel = Label(self.focusBox, text=self.focus[0]+str(self.focus[1])+":", borderwidth = 0, relief = "solid", width = 5)
            self.focusLabel.grid(row=0, column=0)
            cellx = self.getCell((self.focus[0], self.focus[1]))
            self.focusEntry = Entry(self.focusBox, width = 16)
            self.focusEntry.insert(END, str(cellx.expression))
            self.focusEntry.grid(row = 0, column = 1)
        else:
            y = coords[0]
            x = coords[1]
            #adjust cords to integers if needed
            if(isinstance(y,str) == True):
                y = ord(y) - ord('a')
            if(isinstance(x,str) == True):
                x = int(x)
            self.focusLabel = Label(self.focusBox, text=self.focus[0]+str(self.focus[1])+":", borderwidth = 0, relief = "solid", width = 5)
            self.focusLabel.grid(row=0, column=0)
            cellx = self.getCell((self.focus[0], self.focus[1]))
            self.focusEntry = Label(self.focusBox, text=str(cellx.value), borderwidth = 0, relief = "solid", width = 16)
            self.focusEntry.grid(row=0, column = 1)
        frame = self.board
        if coords != None:
            yy = coords[0]
            xx = coords[1]
            if(isinstance(yy,str) == True):
                yy = ord(yy) - ord('a')
            if(isinstance(xx,str) == True):
                xx = int(xx)
        else:
            xx = ord(self.focus[0]) - ord('a')
            yy = int(self.focus[1])
        for child in frame.children.values():
            info = child.grid_info()
            if(int(info['row'])-1 == int(xx) and int(info['column'])-1 == int(yy)):
                child.config(bg="Yellow")
            else:
                child.config(bg="white")
 
 

    def setFocus(self, event = None, coords=None, error = None):
        if(error != None):
            self.createFocus(coords = coords, error = error)
        else:
            y = coords[0]
            x = coords[1]
            if(isinstance(y, int) == True):
                self.focus = (chr(y+97), x)
            else:
                self.focus = (y,x)
            self.createFocus()                   

    def getCell(self, event = None, coords = None):
        if(coords == None):
            y = self.focus[0]
            x = self.focus[1]
        else:
            y = coords[0]
            x = coords[1]
        if(isinstance(y,str) == True):
            y = ord(y) - ord('a')
        if(isinstance(x,int) == False):
            x = int(x)
        return self.gridx[y][x]

    def myisDigit(self, strx):
        print("entered")
        if "." in strx:
            strx.replace(".", '')
        return strx.isdigit()

            
    def setCell(self, event = None, coords = None, expression = None):
        if(coords == None): #no coords assume focus box
            coords = (self.focus[0], self.focus[1])
        if(expression == None or expression == ""):
            expression = self.focusEntry.get()
        y = coords[0]
        x = coords[1]
        if(isinstance(y, str) == True):
            y = ord(y) - ord('a')
        if(isinstance(x, str) == True):
            x = int(x)
        #try and evaluate error
        oldExpression = self.gridx[y][x].expression
        oldValue = self.gridx[y][x].value
        try:
            self.gridx[y][x].expression = expression
            self.evaluation((y,x))
            self.dependencyDealing((y,x),(y,x))
            self.setLabel(frame = self.board, coords = (y,x))
            self.updateTable(coords = (y,x))
        except:
            self.restore = 1
            sym = str(chr(y+97))+str(x)
            symx = str(chr(self.remover[0]+97))+str(self.remover[1])
            self.gridx[y][x].value = oldValue
            self.gridx[y][x].expression = oldExpression
            try:
                self.dependers[sym] = []
            except:
                print("nothing depending on it")
            print(sym)
            messagebox.showerror("Error", "An error has occured entering this value")
            for x in range(self.nCols):
                for y in range(self.nRows):
                    if self.gridx[y][x].expression != "":
                        self.evaluation((y,x))
            self.restore = 0
            
        
    def evaluation(self, coords = None):
        if(coords == None):
            y = self.focus[0]
            x = self.focus[1]
        else:
            y = coords[0]
            x = coords[1]
        if(isinstance(y, str) == True):
            y = ord(y) - ord('a')
        try:
            self.gridx[y][x].value = eval(str(self.gridx[y][x].expression))
            print(str(self.gridx[y][x].value))
            self.updateTable(coords = (y,x), value = self.gridx[y][x].value)
        except:
            valueEp = 0
            for symbol in self.symTable:
                if symbol in self.gridx[y][x].expression:
                    valueEp = 1
                    self.gridx[y][x].value = self.symEvaluation(self.gridx[y][x].expression, coords = (y,x))
                    print("value2 : " + str(self.gridx[y][x].value))
            if valueEp == 0:
                self.gridx[y][x].value = ""
                messagebox.showerror("Error", "An error has occured entering this value")
                
                
            
                
    def symEvaluation(self, expression, coords = None):
        for sym in self.symTable:
            if sym in expression:
                if sym in self.dependers:
                    if(isinstance(coords[0], int)):
                        symx = str(chr(coords[0]+97))+str(coords[1])
                    else:
                        symx = str(coords[0])+str(coords[1])
                    if symx not in self.dependers[sym]:
                        self.dependers[sym].append(symx)
                else:
                    self.addDependency(sym, coords)
                if self.myisDigit(str(self.symTable[sym])) == False:
                    print("isFalse")
                    symz = "'"+ str(self.symTable[sym]) + "'"
                else:
                    symz = str(self.symTable[sym])
                expression = expression.replace(sym, symz)
        try:
            print("expression: "+ expression)
            result = eval(expression)
            print("result: " + str(result))
            return result
        except:
            messagebox.showerror("Error", "An error has occured entering this value")
            return ""

    def addDependency(self, sym, coords):
        if(isinstance((sym[0]), int)):
            x = chr(sym[0]+97)
            sym = str(x)+str(sym[1:])
        if(isinstance(coords[0], int)):
            y = chr(coords[0]+97)
        else:
            y = coords[0]
        setsym = str(y)+str(coords[1])
        self.dependers[sym] = [setsym]

    def updateTable(self, coords = None, value = None):
        if(coords == None):
            y = self.focus[0]
            x = self.focus[1]
        else:
            y = coords[0]
            x = coords[1]
        if(isinstance(y, int) == True):
            y = chr(y+97)
        val = str(y) + str(x)
        if(value == None):
            cellx =  self.getCell((y,x))
            self.symTable[val] = cellx.value
        else:
            self.symTable[val] = value
    
    def setLabel(self, frame = None, coords = None):
        if(frame == None):
            frame = self.board
        if(coords == None):
            coords = (focus[0], focus[1])
        for child in frame.children.values():
            info = child.grid_info()
            if(int(info['row'])-1 == int(coords[0]) and int(info['column'])-1 == int(coords[1])):
                child.config(text=str(self.gridx[coords[0]][coords[1]].value))
            
    def dependencyDealing(self, coords, cCoords = None):
        if(isinstance(coords,tuple)):
            if(isinstance(coords[0], int)):
                row = chr(coords[0]+97)
            else:
                row = coords[0]
            coordx = str(row)+str(coords[1])
        else:
            coordx = coords
        if coordx in self.dependers:
            for loc in self.dependers[coordx]:
                r = loc[0]
                c = loc[1:]
                if(isinstance(r, str) == True):
                    r = ord(r) - ord('a')
                if(isinstance(c, str) == True):
                    c = int(c)
                cordx = (r,c)
                if cordx == cCoords and self.restore != 1:
                    self.remover = coords
                    raise OverflowError()
                else:
                    self.evaluation((r,c))
                    valuex = self.gridx[r][c].value
                    self.updateTable(coords = (r,c), value = valuex)
                    self.dependencyDealing((r,c), cCoords)
                    self.setLabel(frame = self.board, coords = (r, c))
