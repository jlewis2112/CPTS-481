#! /usr/bin/env python3

"""
Joseph Lewis
HW 5
Tic Tac Toe
"""
#run python3 tictactoe.py

from tkinter import Tk
from tkinter import Frame
from tkinter import Button
from tkinter import *

"""
Tic Tac Toe Board class
"""
class TicTacToeBoard(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.board={'A1':" ", 'A2': " ", 'A3': " ", 'B1': " ", 'B2': "X", 'B3': " ", 'C1': " ", 'C2': " ", 'C3': " "}
        self.clockwise = {"A1":"A2", "A2":"A3", "A3":"B3", "B3":"C3", "C3":"C2", "C2":"C1", "C1":"B1", "B1":"A1"}
        self.opposite = {"A1":"C3", "A2":"C2", "A3":"C1", "B1":"B3", "B3":"B1", "C1":"A3", "C2":"A2", "C3":"A1"}
        self.prev = "B2"
        self.C = ""#the 2nd previous move in the sudo code
        self.game = True #is game going
        self.userTurn = True #is it the users turn
        self.moves = 1 #the move counter
        #set up the board
        self.A1 = Button(self, text="", font=('times', 20, 'bold'), command= lambda: self.update("A1"))
        self.A2 = Button(self, text="", font=('times', 20, 'bold'), command= lambda: self.update("A2"))
        self.A3 = Button(self, text="", font=('times', 20, 'bold'), command= lambda: self.update("A3"))
        self.B1 = Button(self, text="", font=('times', 20, 'bold'), command= lambda: self.update("B1"))
        self.B2 = Button(self, text="X", font=('times', 20, 'bold'), command= lambda: self.update("B2"))
        self.B3 = Button(self, text="", font=('times', 20, 'bold'), command= lambda: self.update("B3"))
        self.C1 = Button(self, text="", font=('times', 20, 'bold'), command= lambda: self.update("C1"))
        self.C2 = Button(self, text="", font=('times', 20, 'bold'), command= lambda: self.update("C2"))
        self.C3 = Button(self, text="", font=('times', 20, 'bold'), command= lambda: self.update("C3"))
        self.quitter = Button(self, text="QUIT", command= self.quit)
        self.pack(fill=BOTH, expand = 1)
        self.message = Label(text = "Your Turn!")
        self.message.place(x=0, y=270)
        self.A1.config(height = 2, width = 3)
        self.A2.config(height = 2, width = 3)
        self.A3.config(height = 2, width = 3)
        self.B1.config(height = 2, width = 3)
        self.B2.config(height = 2, width = 3)
        self.B3.config(height = 2, width = 3)
        self.C1.config(height = 2, width = 3)
        self.C2.config(height = 2, width = 3)
        self.C3.config(height = 2, width = 3)
        self.A1.place(x=0, y=0)
        self.A2.place(x=70, y=0)
        self.A3.place(x=140, y=0)
        self.B1.place(x=0, y=70)
        self.B2.place(x=70, y=70)
        self.B3.place(x=140, y=70)
        self.C1.place(x=0, y=140)
        self.C2.place(x=70, y=140)
        self.C3.place(x=140, y=140)
        self.quitter.place(x = 140, y = 270)
        
        
        
        
    """
    When the button is pressed update board and computers move
    """   
    def update(self, buttonP):
        button = getattr(self, buttonP) 
        if(self.userTurn and self.game and button['text'] == ""):
            self.moves += 1
            self.C = self.prev
            self.prev = buttonP
            self.board[buttonP] = "O"
            button.config(text = "O")
            self.userTurn = False
            winner = self.check() #check for a winner
            if(winner != None):
                self.endGame(winner)
            elif(winner == None and self.moves >= 9):
                self.endGame(winner)
            else:
                self.message.config(text = "My Turn")
                self.computerTurn()
    """
    determine the computers move
    """           
    def computerTurn(self):
        if self.moves == 2: #move clockwise
            cw = self.clockwise[self.prev]
            (getattr(self, cw)).config(text = "X")
            self.board[cw] = 'X'
            self.C = self.prev
            self.prev = cw
            self.moves += 1
        else:
            op = self.opposite[self.C]
            if(self.board[op] != "X" and self.board[op] != "O"):
                (getattr(self, op)).config(text = "X")
                self.board[op] = 'X'
                self.C = self.prev
                self.prev = op
                self.moves += 1
            else: 
                moveMade = False
                attempt = self.prev
                while(moveMade == False):
                    cw = self.clockwise[attempt]
                    if(self.board[cw] == " "):
                        (getattr(self, cw)).config(text = "X")
                        self.board[cw] = 'X'
                        self.C = self.prev
                        self.prev = cw
                        self.moves += 1
                        moveMade = True
                    else:
                        attempt = self.clockwise[attempt]
                        
        if(self.game):
            winner = self.check()
            if(winner != None):
                self.endGame(winner)
            elif(winner == None and self.moves >= 9):
                self.endGame(winner)
            else:
                self.userTurn = True
                self.message.config(text= "Your Turn!")
                        
                              
    """
    Check to see 3 in a row
    """        
    def check(self):
        if(self.board['A1'] != " " and self.board['A2'] == self.board['A1'] and self.board['A3'] == self.board['A1']):
            return self.board['A1']
        elif(self.board['B1'] != " " and self.board['B2'] == self.board['B1'] and self.board['B3'] == self.board['B1']):
            return self.board['B1']
        elif(self.board['C1'] != " " and self.board['C2'] == self.board['C1'] and self.board['C3'] == self.board['C1']):
            return self.board['C1']
        elif(self.board['A1'] != " " and self.board['B1'] == self.board['A1'] and self.board['C1'] == self.board['A1']):
            return self.board['A1']
        elif(self.board['A2'] != " " and self.board['B2'] == self.board['A2'] and self.board['C2'] == self.board['A2']):
            return self.board['A2']
        elif(self.board['A3'] != " " and self.board['B3'] == self.board['A3'] and self.board['C3'] == self.board['A3']):
            return self.board['A3']
        elif(self.board['A1'] != " " and self.board['B2'] == self.board['A1'] and self.board['C3'] == self.board['A1']):
            return self.board['A1']
        elif(self.board['C1'] != " " and self.board['B2'] == self.board['C1'] and self.board['A3'] == self.board['C1']):
            return self.board['C1']
        else:
            return None
            
    """
    Game is over time to find the winner
    """        
    def endGame(self, winner):
        self.game = False
        if(winner == None):
            self.message.config(text = "Cats Game")
        else:
            if winner == "X":
                self.message.config(text = "I WIN!")
            elif winner == "O":
                self.message.config(text = "You Win")         
    """
    end program
    """ 
    def quit(self):
        quit()
      
root = Tk()
root.title("Tic Tac Toe")
root.geometry("210x315")#using geometry manager grid for some reason had a error
board = TicTacToeBoard(root)
#board.grid()
root.mainloop()
