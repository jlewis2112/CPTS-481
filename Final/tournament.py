


"""
Joseph Lewis Project module
"""

import sqlite3
from tkinter import Tk
from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import messagebox
from tkinter import ttk
from tkinter import *


"""
Global Font Variables
"""

LARGEFONT = ("Verdana", 15)
MEDIUMFONT = ("Verdana", 10)


class Player():
    """
    This is the Player Class that represents a Player.
    It will include name and Score.
    
    >>> print("Testing Player")
    Testing Player
    """
    def __init__(self, namex, scorex = 0):
        """
        Initialization of the name Class
        
        >>> startingPlayer = Player("Billy")
        >>> print(startingPlayer)
        Billy
        """
        self.name = namex
        self.score = scorex
        
    def addScore(self, points):
        """
        Adds points to a players score
        """
        self.score = self.score + points
        
    def showScore(self):
        """
        A getter for the players score.
        
        >>> returningPlayer = Player("Sam", 15)
        >>> returningPlayer.addScore(15)
        >>> returningPlayer.showScore()
        30
        """
        return self.score
        
    def __repr__(self):
        """
        Magic Function Representing the Player's Name
        """
        return self.name
        
    def __str__(self):
        """
        Magic Function Representing the Player's Name
        """
        return self.name


class Match():
    """
    This is the match class. Two players will face eachover
    and a winner will be the players name. Also winBy describes the win.
    There is a point feature inside this class as well.
    """
    def __init__(self, player1 = None, player2 = None, match = 0, roundx = 0):
        """
        This Function initializes the Match class
        
        >>> matchUp = Match("jimmy", "jake", 2, 1)
        >>> matchUp
        2. jimmy vs jake
        """
        self.red = player1
        self.blue = player2
        self.winner = ""
        self.loser = ""
        self.winType = ""
        self.winBy = ""
        self.points = 0
        self.matchNumber = match
        self.roundx = roundx


    def winnerStr(self):
        """
        Returns the string clarifying the winner or the draw.
        This strings describes the result of the bout.
        """
        result = ""
        if self.winner == "":
            return str(self.matchNumber) + ". " + self.red + " drew with " + self.blue
        elif self.blue == None or self.blue == "":
            return str(self.matchNumber) + ". " + self.red + " had a bye"
        else:
            if self.points == 3:
                result = str(self.matchNumber) + ". " + self.winner + " won 2-0 to " + self.loser 
            if self.points == 2:
                result = str(self.matchNumber) + ". " + self.winner + " won 2-1 to " + self.loser
                
        if self.winBy != "" and self.winBy != None:
            result = result + " by " + self.winBy
        return result
        
    def setWinner(self, color, winString, how):
        """
        Sets the winner of the match up
        
        >>> matchUp = Match("jimmy", "jake", 2, 1)
        >>> matchUp.setWinner(0, "winning", 2)
        >>> matchUp.winner
        'jimmy'
        >>> matchUp.loser
        'jake'
        >>> matchUp.winBy
        'winning'
        >>> matchUp.winType
        '2-1'
        >>> matchUp.points
        2
        >>> matchUp.roundx
        1
        >>> matchUp.winnerStr()
        '2. jimmy won 2-1 to jake by winning'
        """
        self.winBy = winString
        if color == 0:
            self.winner = self.red
            self.loser = self.blue
        elif color == 1:
            self.winner = self.blue
            self.loser = self.red
        else:
            self.winner = ""
            self.loser = ""
        
        if how == 1:
            self.points = 1
            self.winType = "draw"
        elif how == 2:
            self.points = 2
            self.winType = "2-1"
        elif how == 3:
            self.points = 3
            self.winType = "2-0"
        elif how == 4:
            self.points = 3
            self.winType = "BYE"
        else:
            print("error when determining winner")
        
    def __repr__(self):
        """
        Magic Function that represents the match Number
        """
        if self.blue == "" or self.blue == None:
            return str(self.matchNumber) + ". " + self.red + " vs " + "BYE"   
        return str(self.matchNumber) + ". " + self.red + " vs " + self.blue
        
    def __str__(self):
        """
        Magic Function Representing the match Number
        """
        if self.blue == "" or self.blue == None:
            return str(self.matchNumber) + ". " + self.red + " vs " + "BYE"   
        return str(self.matchNumber) + ". " + self.red + " vs " + self.blue
        
        


class Tournament():
    """
    This class represents the functionality of the tournament.
    
    >>> print("Testing Tournament")
    Testing Tournament
    
    """
    def __init__(self):
        """
        Initializing the tournament Class
        
        >>> newTournament = Tournament()
        """
        self.name = ""
        self.players = []
        self.rounds = 1
        self.currentRound = 1
        self.bout = 1
        self.matchUps = []
        self.matches = []
        
    def findPlayer(self, controller, name):
        """
        Finds a player is the players list and returns the index
        """
        x = 0
        for player in self.players:
            if name == str(player):
                return x
            x += 1
        return -1


    def showPlayerScore(self, player):
        """
        Used in the sorting key to sort players scores
        
        >>> testPlayer = Player("Sam", 15)
        >>> newTournament = Tournament()
        >>> newTournament.showPlayerScore(testPlayer)
        15
        """
        return player.showScore()

    def sortPlayers(self):
        """
        Sorts the players by there score. Used for final standings and
        pairings.
        >>> Tourney = Tournament()
        >>> Tourney.players.append(Player("Sam5", 5))
        >>> Tourney.players.append(Player("Sam1", 9))
        >>> Tourney.players.append(Player("Sam2", 8))
        >>> Tourney.players.append(Player("Sam3", 7))
        >>> Tourney.players.append(Player("Sam4", 6))
        >>> Tourney.sortPlayers()
        >>> Tourney.players
        [Sam1, Sam2, Sam3, Sam4, Sam5]
        """
        self.players.sort(key=self.showPlayerScore)
        self.players = self.players[::-1]
        
    def findMatchUps(self, controller = None):
        """
        This function determines matchups between players.
        Match ups are determined by similar scores. If the
        amount of players are odd, then the player with the
        lowest score gets a bye.
        >>> Tourney = Tournament()
        >>> Tourney.players.append(Player("Sam5", 5))
        >>> Tourney.players.append(Player("Sam1", 9))
        >>> Tourney.players.append(Player("Sam2", 8))
        >>> Tourney.findMatchUps()
        >>> Tourney.matchUps
        [1. Sam1 vs Sam2, 2. Sam5 vs BYE]
        """
        self.sortPlayers()
        x=0
        y=1
        result = []
        self.matchUps = []
        while y < len(self.players):
            self.matchUps.append(Match(str(self.players[x]), str(self.players[y]), self.bout, self.currentRound))
            x += 2
            y += 2
            self.bout += 1
        if (len(self.players) % 2) == 1:
            self.matchUps.append(Match(str(self.players[-1]), "", self.bout, self.currentRound))
            self.bout += 1


class OverPage(Frame):
    """
    This class is the final frame appearing when the tournament is over.
    It will show the winner and notify that the certificate and 
    match stats are added in the text files
    """
    def __init__(self, parent, controller):
        """
        Initializing the Tournament Over frame
        """
        Frame.__init__(self, parent)
        label = Label(self, text="Tournament Over", font = LARGEFONT)
        label.grid(row = 0, column =  0, padx=0, pady = 3)
        self.startButton = Button(self, text="Click to process results", command = lambda : self.showResults(parent, controller))
        self.startButton.grid(row = 1, column = 1, padx = 10, pady = 10)
        
    def showResults(self, parent, controller):
        """
        This function prints the bout and
        placing results in the needed text files
        """
        self.startButton.grid_remove()
        placeFile = open("placings.txt", "w")
        matchFile = open("boutResult.txt", "w")
        for match in tourny.matches:
            matchFile.write(match + "\n")
        tourny.sortPlayers()
        x = 1
        space = 0
        prevPlayer = None
        y = 0 
        for player in tourny.players:
            if prevPlayer == None or player.score == prevPlayer.score:
                space += 1
                text = str(x)+". "+str(player)+" "+str(player.score)
                placeFile.write(text + "\n")
            else:
                x = x + space
                space = 1
                text = str(x)+". "+str(player)+" "+str(player.score)
                placeFile.write(text + "\n")
            y += 1
            prevPlayer = player
        placeFile.close()
        matchFile.close()
        label = Label(self, text="Results have been printed", font = LARGEFONT)
        label.grid(row = 4, column =  0, padx=0, pady = 3)
        


class MatchPage(Frame):
    """
    This class is a frame that runs the tournament matches.
    It consists of the match description with buttonds determining the 
    winner.  There will be 5 buttons to determine the type of match ending
    and a text bar you can type in more detail. These buttons be pressed 
    more than once to change the result. Once each match is 
    completed press the confirm button to end the round.
    """
    def __init__(self, parent, controller):
        """
        Initializing the match frame
        """
        Frame.__init__(self, parent)
        label = Label(self, text="(note: the structure red vs blue and best 2 of 3 games)", font = MEDIUMFONT)
        label.grid(row = 0, column =  0, padx=0, pady = 3)
        label = Label(self, text="RED      vs      BLUE", font = MEDIUMFONT)
        label.grid(row = 1, column =  0, padx=2, pady = 5)
        self.startButton = Button(self, text="Click to start matches", command = lambda : self.startMatches(parent, controller))
        self.startButton.grid(row = 1, column = 2, padx = 10, pady = 10)
        self.frameStorage = []
        
    def startMatches(self, parent, controller):
        """
        After matches begin, display the interface showing
        and determining the winner of the matches.
        """
        self.roundLabel = Label(self, text= "Round "+str(tourny.currentRound)+" out of "+str(tourny.rounds), font = MEDIUMFONT, justify=LEFT)
        self.roundLabel.grid(row = 3, column =  0, padx=5, pady = 5)
        self.nameLabel = Label(self, text= " in " + str(tourny.name), font = MEDIUMFONT)
        self.nameLabel.grid(row = 3, column = 1, padx=5, pady=5)
        tourny.findMatchUps()
        self.startButton.grid_remove()
        self.endButton = Button(self, text="Confirm results", command = lambda : self.endRound(parent, controller))
        self.endButton.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.matchLength = len(tourny.matchUps)
        print("lengthx: " + str(self.matchLength))
        x = 0
        while x < self.matchLength:
            label2 = Label(self, text=tourny.matchUps[x], font = MEDIUMFONT)
            label2.grid(row = 4+x, column = 0, padx=2, pady=5)
            if tourny.matchUps[x].blue != "":
                entry = Entry(self, width = 30)
                entry.insert(END, "name,2-0,winning")
                entry.grid(row = 4+x, column = 1, padx=1, pady=5)
                self.frameStorage.append([label2, entry])
            else:
                winLabel = Label(self, text="win by default", font = MEDIUMFONT)
                winLabel.grid(row = 4+x, column = 1, padx=1, pady=5)
                self.frameStorage.append([label2, winLabel])  
            x += 1
            
            
        self.labelNote = Label(self, text="Note: enter the match details in the following form(tie leave text box blank):", font = MEDIUMFONT)
        self.labelNote.grid(row = 4+x, column = 0, padx=5, pady=5)
        self.labelNote2 = Label(self, text="{winner name},{match record ie 2-0},{details}", font = MEDIUMFONT)
        self.labelNote2.grid(row = 5+x, column = 0, padx=5, pady=5)

           
    def endRound(self, parent, controller):
        """
        This function is executed when the round is over.
        It sets the winner and adds points.
        """
        MsgBox = messagebox.askquestion('confirm results', 'Are the results correct', icon = 'warning')
        if MsgBox == 'yes':
            if self.recordResults(parent, controller) == 1:
                self.roundLabel.grid_remove()
                self.labelNote.grid_remove() 
                self.nameLabel.grid_remove()
                self.labelNote2.grid_remove()
                self.endButton.grid_remove()
                self.startButton.grid(row = 1, column = 2, padx = 10, pady = 10)
                for row in self.frameStorage:
                    for dud in row:
                        dud.grid_remove()
                tourny.currentRound += 1
                if tourny.currentRound <= tourny.rounds: 
                    controller.showFrame(ContinuePage)
                else:
                    controller.showFrame(OverPage)
                self.frameStorage = []
            else:
                messagebox.showerror("Error", "Match data was entered incorrectly")
                       
        
    def recordResults(self, parent, controller):
        """
        This is the function to record results in match ups.
        This function will check if an error has occured then return 1 or 0.
        """
        x = 0
        matchList = []
        for match in tourny.matchUps:
            if match.blue == None or match.blue == "":
                match.setWinner(0, "by bye", 4)
            elif self.frameStorage[x][1].get() == "":
                match.setWinner(2, "by draw", 1)
            else:
                matchText = self.frameStorage[x][1].get()
                matchList = matchText.split(',')
                print(matchList)
                if len(matchList) == 2:
                    matchList.append("")
                if matchList[0] == match.red:
                    if matchList[1] == "2-0":
                        match.setWinner(0, matchList[2], 3)
                    elif matchList[1] == "2-1":
                        match.setWinner(0, matchList[2], 2)
                    else:
                        print("hey1")
                        return 0
                elif matchList[0] == match.blue:
                    if matchList[1] == "2-0":
                        match.setWinner(1, matchList[2], 3)
                    elif matchList[1] == "2-1":
                        match.setWinner(1, matchList[2], 2)
                    else:
                        return 0
                else:
                    print(matchList[0])
                    return 0
            x += 1
        
        for match in tourny.matchUps:
            if match.winner == "":
                redL = tourny.findPlayer(controller, match.red)
                tourny.players[redL].addScore(1)
                blueL = tourny.findPlayer(controller, match.blue)
                tourny.players[blueL].addScore(1)
            else:
                loc = tourny.findPlayer(controller, match.winner)
                tourny.players[loc].addScore(match.points)
            tourny.matches.append(match.winnerStr())
        return 1   



class PlayerRoundPage(Frame):
    """
    This class is a frame that will be used to 
    enter the players and the number of rounds in 
    the tournament.
    """        
    def __init__(self, parent, controller):
        """
        Initialize the class holding the frame
        """
        self.playerNumber = 1
        Frame.__init__(self, parent)
        label = Label(self, text="Fill in the information", font = LARGEFONT)
        label.grid(row = 0, column =  1, padx=5, pady = 5)
        label1 = Label(self, text="Enter # of rounds", font = MEDIUMFONT)
        label1.grid(row = 2, column =  1, padx=5, pady = 5)
        entry1 = Entry(self, width = 25)
        entry1.insert(END, "enter rounds here")
        entry1.grid(row = 3, column = 1)
        label2 = Label(self, text="Enter Players: use enter player button to add a player", font = MEDIUMFONT)
        label2.grid(row = 5, column =  1, padx=5, pady = 5)
        self.entry2 = Entry(self, width = 25)
        self.entry2.insert(END, "player"+str(self.playerNumber))
        self.entry2.grid(row = 6, column = 1)
        button1 = Button(self, text="enter player", command = lambda : self.addPlayer(self.entry2.get(), parent, controller))
        button1.grid(row = 6, column = 2, padx = 10, pady = 10)
        button1 = Button(self, text="Submit Information", command = lambda : self.addInformation(entry1.get(), parent, controller))
        button1.grid(row = 3, column = 2, padx = 10, pady = 10)
        
    def addPlayer(self, name, parent, controller):
        """
        After the add player button is pressed,
        a player is added to the players list of the tournament class.
        """
        testName = name.replace(" ","")
        namex =  name
        if testName == "" or testName == None:
            messagebox.showerror("Error", "Please enter a player name")
        elif tourny.findPlayer(self, namex) != -1:
            messagebox.showerror("Error", "This name is already used")
        elif ',' in namex:
            messagebox.showerror("Error", "Cant use , in the name")   
        else:
            self.playerNumber += 1
            newPlayer = Player(namex)
            tourny.players.append(newPlayer)
            print(str(tourny.players))
            label = Label(self, text="Welcome "+namex, font = MEDIUMFONT)
            label.grid(row = self.playerNumber+6, column =  1, padx=5, pady = 5)
            self.entry2.delete(0, END)
            self.entry2.insert(END, "player"+str(self.playerNumber))
             
    def addInformation(self, rounds, parent, controller):
        """
        This function checks to see if the entered information is
        correct. If the information is correct then we set the tournament
        values in tourny.
        """
        if len(tourny.players) <= 1:
            messagebox.showerror("Error", "Need to enter 2 or more players")
        elif rounds.replace(" ", "") == "0":
            messagebox.showerror("Error", "Number of rounds needs to be greater than 0")   
        elif rounds.isdigit() == False:
            messagebox.showerror("Error", "Number of rounds needs to be a digit")
        elif rounds[0] == '0':
            messagebox.showerror("Error", "Number of rounds entry cannot start with a zero")
        else:
            print("success")
            tourny.rounds = int(rounds)
            controller.showFrame(ContinuePage)
                          

class InitialPage(Frame):
    """
    This Frame will be used to create a new tournament.
    Features will include the title, enter players, enter number of rounds,
    and enter tournament name.  After data is entered there will be
    a start tournament button. There will be an error message if info was
    not entered correctly. Otherwise the tournament round frame will show 
    up.
    """
    def __init__(self, parent, controller):
        """
        Initialize the IntialPage for creating a new tournament.
        """
        Frame.__init__(self, parent)
        label = Label(self, text="Enter Tournament Name", font = LARGEFONT)
        label.grid(row = 0, column =  1, padx=5, pady = 5)
        entry1 = Entry(self, width = 25)
        entry1.insert(END, "tournament name")
        entry1.grid(row = 1, column = 1)
        button1 = Button(self, text="enter", command = lambda : self.checkName(parent, controller, entry1.get()))
        button1.grid(row = 1, column = 2, padx = 10, pady = 10)
        
    def checkName(self, parent, controller, name):
        """
        Sets and checks the tournament name
        """
        testName = name.replace(" ","")
        namex =  name
        if testName == "" or testName == None:
            messagebox.showerror("Error", "Please enter a tournament Name")
        else:
            tourny.name = namex
            app.title(namex)
            print("named: " + tourny.name)
            controller.showFrame(PlayerRoundPage)
        
    
class ContinuePage(Frame):
    """
    This Frame will be used to create a new tournament.
    Features will include the title, enter players, enter number of rounds,
    and enter tournament name.  After data is entered there will be
    a start tournament button. There will be an error message if info was
    not entered correctly. Otherwise the tournament round frame will show 
    up.
    """
    def __init__(self, parent, controller):
        """
        Initialize the Continue Page.
        """
        Frame.__init__(self, parent)
        self.standingGrid = []
        label2 = Label(self, text="Ready to Continue", font=LARGEFONT)
        label2.grid(row = 2, column =  4, padx=5, pady = 5)
        button1 = Button(self, text="start matches", command = lambda : 
        self.begin(controller))
        button1.grid(row = 6, column = 4, padx = 10, pady = 10)
        button2 = Button(self, text="save and quit", command = lambda : self.save())
        button2.grid(row = 6, column = 5, padx = 10, pady = 10)
        self.buttonS = Button(self, text="show standings", command = lambda : self.displayStandings())
        self.buttonS.grid(row = 6, column = 7, padx = 10, pady = 10)
        
    def save(self):
        """
        Saves information to the database and quits
        """
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        sql_create_tourney = """ CREATE TABLE IF NOT EXISTS tournament ( id integer PRIMARY KEY, name text NOT NULL, current_round integer NOT NULL, rounds integer NOT NULL, current_bout integer NOT NULL);"""
        sql_create_match = """ CREATE TABLE IF NOT EXISTS matches ( id integer PRIMARY KEY, result text NOT NULL);"""
        sql_create_player = """ CREATE TABLE IF NOT EXISTS players ( id integer PRIMARY KEY, name text NOT NULL, points integer NOT NULL); """
        c.execute(sql_create_tourney)
        c.execute(sql_create_match)
        c.execute(sql_create_player)
        #add tournament
        tourneyLabel = "INSERT INTO tournament VALUES ( 1," + "'" +tourny.name + "', "+ str(tourny.currentRound) + ", "+ str(tourny.rounds)+ ", " + str(tourny.bout) + ")"
        c.execute(tourneyLabel)
        x = 1
        for match in tourny.matches:
            addMatch = "INSERT INTO matches VALUES ( " + str(x) + ", '" + match +"' )"
            print(addMatch)
            c.execute(addMatch)
            x += 1
        x = 1
        for player in tourny.players:
            addPlayer = "INSERT INTO players VALUES ( " + str(x) + ", '" + str(player) + "', " + str(player.score) + " )" 
            c.execute(addPlayer)
            x += 1
        conn.commit()
        conn.close()
        quit()
        
    def begin(self, controller):
        """
        Remove the placing labels and move to the
        match frame.
        """
        for labelx in self.standingGrid:
            labelx.grid_remove()
        self.buttonS.grid(row = 6, column = 7, padx = 10, pady = 10)
        controller.showFrame(MatchPage)
        
    def displayStandings(self):
        """
        Displays the standings of the players
        in the tournament.
        """
        tourny.sortPlayers()
        self.buttonS.grid_remove()
        x = 1
        space = 0
        prevPlayer = None
        y = 0 
        for player in tourny.players:
            if prevPlayer == None or player.score == prevPlayer.score:
                space += 1
                label = Label(self, text=str(x)+". "+str(player)+" "+str(player.score), font=MEDIUMFONT)
                label.grid(row = 7+y, column =  4, padx=5, pady = 5)
                self.standingGrid.append(label)
            else:
                x = x + space
                space = 1
                label = Label(self, text=str(x)+". "+str(player)+" "+str(player.score), font=MEDIUMFONT)
                label.grid(row = 7+y, column =  4, padx=5, pady = 5)
                self.standingGrid.append(label)
            y += 1
            prevPlayer = player
                
            
        



class StartPage(Frame):
    """
    This Class represents the home page of the tournament application.
    It will be two buttons start new tournment or load previous tournment.
    Both buttons will show the specific frame.
    """
    def __init__(self, parent, controller):
        """
        Initail function the home page frame.
        Add Title and two buttons deciding to load or create the
        Tournament.
        """
        Frame.__init__(self, parent)
        label = Label(self, text="Welcome to the swiss tournament", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 5, pady = 5)
        button1 = Button(self, text="start new tournament", command = lambda : controller.showFrame(InitialPage))
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
        button1 = Button(self, text="continue tournament", command = lambda : self.loadTourney(controller))
        button1.grid(row = 2, column = 1, padx = 10, pady = 10)
        
    def loadTourney(self, controller):
        """
        This function tries to pull the saved tournament from the
        database to continue the tournament.
        """
        try:
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute("SELECT * FROM tournament")
            rows = c.fetchall()
            x = 0
            for row in rows:
                if x == 0:
                    x = 1
                    tourny.name = row[1]
                    app.title(tourny.name)
                    tourny.currentRound = row[2]
                    tourny.rounds = row[3]
                    tourny.bout = row[4]
            c.execute('DELETE FROM tournament')
            if tourny.name == '':
                messagebox.showerror("Error", "No tournament saved")
                return    
            c.execute('SELECT * FROM players')
            rows = c.fetchall()
            for row in rows:
                newPlayer = Player(row[1], row[2])
                tourny.players.append(newPlayer)
            c.execute('DELETE FROM players')
            c.execute('SELECT * FROM matches')
            rows = c.fetchall()
            for row in rows:
                tourny.matches.append(row[1])
            conn.commit()
            conn.close()
            controller.showFrame(ContinuePage)
        except:
            messagebox.showerror("Error", "No tournament saved")
            
        
class TournamentApp(Tk):
    """
    This is the Tk class representin the root of
    the overall application.
    
    >>> tourny = Tournament()
    >>> app = TournamentApp()
    """
    def __init__(self, *args, **kwargs):
        """
        Initializing the initail tkinter application.
        """
        Tk.__init__(self, *args, **kwargs)
        self.title("swiss style Tournament")  
        container = Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}
        for F in (StartPage, ContinuePage, InitialPage, PlayerRoundPage, MatchPage, OverPage):
            frame = F(container, self) 
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.showFrame(StartPage)
        
    def showFrame(self, cont):
        """
        This function causes the application to display the needed 
        frame after a button or an error is raised.
        """
        frame = self.frames[cont]
        frame.tkraise()

tourny = Tournament()
app = TournamentApp()
app.mainloop()        
