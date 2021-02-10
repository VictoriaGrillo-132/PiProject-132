#####################################################################################
# Team Name: Team Java
# Group Members: Austen Belmonte, Josue Gaona, Victoria Grillo
# Description: Pi-Project. Study game that uses variations of different style games.
#####################################################################################

from tkinter import * 
#import Rpi.GPIO as GPIO
from random import randint
import tkinter
Letters=("Times New Roman", 14)

'''
#Setting up the leds and buttons
GPIO.setmode(GPIO.BCM)
led1 = None
led2 = None
button1 = None
button2 = None
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(button1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(button2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
'''

#This could possibly useless and be moved into the JepdyBoard class
class ValsandAns():
    questions = [["How is Abstraction defined as?","Multiple inheritance is _______?","A Queue is a _____.","A Dictionary can be defined as?","Zero in a state means it is what?"],
                ["True or False: A pyhton list size is not fixed.","True or False: A Stack is a FIFO Structure.","What does R in Flip Flop stand for?","_ _ _ _ _ _ _-This word means it selects a register.","_ _ _ _ _ _ _ (space) _ _ _ _ _ _ _-Is the name of an equation in computer science."], 
                ["What does S in Flip Flop stand for?","An abbreviation for multiplexer is?","What letter holds the state in a flip flop until signed changes it?","A Flip Flop is used to store what two numbers? ","What is 5 in binary?"]]
    def __init__(self, points):
        self.points = points

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value
    
    def Questions(self, location):
        JepdyBoard.Que.config(state=NORMAL)
        JepdyBoard.Que.delete("1.0", END)
        #print question to question box
        JepdyBoard.Que.insert(END, ValsandAns.questions[location[0]][location[1]])
        JepdyBoard.Que.config(state=DISABLED)
            
    def ChoosePerson(self):
        global led1, led2, button1, button2
        if GPIO.input(button1) == GPIO.HIGH:
            GPIO.output(led1, GPIO.HIGH)
            sleep(.5)
            GPIO.output(led1, GPIO.LOW)
            return 1
        elif GPIO.input(button2) == GPIO.HIGH:
            GPIO.output(led2, GPIO.HIGH)
            sleep(.5)
            GPIO.output(led2, GPIO.LOW)
            return 2

class Player:
    def __init__(self, name):
        self.name = name
        self._points = 0

    @property
    def points(self):
        return self._points
    
    @points.setter
    def points(self, value):
        self._points = value
        PlayersFrame.updatePlayerLabels(self)

    @property
    def active(self):
        return self._active
    
    @active.setter
    def active(self, value):
        self._active = value
        PlayersFrame.updatePlayerLabels(self)

class PlayerFrame(Frame): 
    def __init__(self, parent):
        Frame.__init__(self, parent)
        PlayerFrame.Player1Label = Label(self, font=("Times New Roman", 20))
        PlayerFrame.Player2Label = Label(self, font=("Times New Roman", 20))
        PlayerFrame.Player1Label.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)
        PlayerFrame.Player2Label.grid(row=0, column=5, sticky=NSEW, padx=10, pady=10)
        PlayerFrame.infoLabel = Label(self, text="Hello", font=("Times New Roman", 32))
        PlayerFrame.infoLabel.grid(row=0, column=4, sticky=NSEW, pady=10)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(4, weight=1)
        self.pack(anchor=N, expand=1, fill=X)
        self.activePlayer = 0

    @property
    def activePlayer(self):
        return self._activePlayer

    @activePlayer.setter
    def activePlayer(self, value):
        self._activePlayer = value
        self.updatePlayerLabels(Players[value])

    def updatePlayerLabels(self, player):        
        PlayerFrame.Player1Label.configure(text="{}\n$ {}".format(Players[0].name, Players[0].points), foreground=["Gold2", "Black"][self.activePlayer])
        PlayerFrame.Player2Label.configure(text="{}\n$ {}".format(Players[1].name, Players[1].points), foreground=["Black", "Gold2"][self.activePlayer])

    def addPoints(self, pts):
        Players[self.activePlayer].points += pts
    
    def Switch(self):
        #swap active players
        self.activePlayer = abs(self.activePlayer-1)

class TypeQuestion(Frame):
    #nothing is right
    right_ans=["True","False","reset","decoder","boolean algebra"]
    def __init__(self, parent, question, location):
        Frame.__init__(self, parent)

        TypeQuestion.the_que=question
        TypeQuestion.the__answer=location[1]
        self.location = location

        #Question Box
        TypeQuestion.Que = Text(self, bg="light grey", height=3, font=Letters)
        TypeQuestion.Que.insert("1.0", question)
        TypeQuestion.Que.pack(anchor=N, fill=X)
        TypeQuestion.Que.config(state=DISABLED)

        #Entry for Answering
        TypeQuestion.Ans = Entry(self, font=Letters)
        TypeQuestion.Ans.bind("<Return>", self.process)
        TypeQuestion.Ans.pack(anchor=S, fill=X, side=BOTTOM)
        TypeQuestion.Ans.focus()

        #Back Button
        TypeQuestion.back = Button(self, text="Back", command=lambda Exit="nothing": self.Leave(Exit))
        TypeQuestion.back.pack(anchor=SW, expand=1)

    def process(self, event):
        response = TypeQuestion.Ans.get()
        response = response.lower()

        if response == TypeQuestion.right_ans[TypeQuestion.the__answer]:
            self.Right()
        else:
            self.Wrong()

        TypeQuestion.Ans.delete(0, END)       

    def Right(self):
        PlayersFrame.addPoints(600)
        print(self.location)
        GBoard.DisableBtn(self.location)
        self.Leave("Right")

    def Wrong(self):
        PlayersFrame.addPoints(-600)
        PlayersFrame.Switch()
        PlayerFrame.infoLabel.configure(text="Wrong!", foreground="red")

    def Leave(self, Exit):
        if Exit == "nothing":
            self.pack_forget()
            GBoard.pack(expand=1, fill=BOTH)
            PlayerFrame.infoLabel.configure(text="")
        else:
            self.pack_forget()
            GBoard.pack(expand=1, fill=BOTH)
            PlayerFrame.infoLabel.configure(text="Correct!", foreground="green")

class TypeMulti(Frame):
    right_ans=["Ability to ignore details of parts of a system","Class inherits two or more superclasses","FIFO","Associative arrays","Low","Set","MUX", "Q", "0 or 1", "0101"]
    wrong_ans=[["Increase the system by expanding the data","Ability to focus on one part of a system","Idea of multiple methods in a class"],["Class inherits only one superclass","self contained component at a program","To links b/w separate units of a program"],["LIFO","LILO","FILO"],["Disassociative arrays","Maps values to keys","Where keys can be changed"],["High","0","1"],["Stop","Start","Step"],["MLT","M","MTX"],["S","R","F"],["1 or 2","3 or 4","2 or 4"]]
    def __init__(self, parent, question, location):
        Frame.__init__(self, parent)

        TypeMulti.the_que=question
        #location of Jeporady button that we came from
        self.location = location

        #Question Box
        TypeMulti.Que = Text(self, bg="light grey", width=70, height=3, font=Letters)
        TypeMulti.Que.insert("1.0", question)
        TypeMulti.Que.grid(row=0, column=1, columnspan=2,sticky=N)
        TypeMulti.Que.config(state=DISABLED)

        #Answer Choices
        the_ans_row = randint(1,2)
        the_ans_col = randint(1,2)
        wrongs = 2
        for row_index in range(1,3):
            Grid.rowconfigure(self, row_index, weight=1)
            #number of columns
            for col_index in range(1,3):
                Grid.columnconfigure(self, col_index, weight=1)
                if row_index == the_ans_row and col_index == the_ans_col:
                    btn = Button(self, width=20, command=lambda Right=1: TypeMulti.Right(self), text="{}".format(TypeMulti.right_ans[location[1]]), font=Letters)
                else:
                    btn = Button(self, width=20, command=lambda Wrong=1: TypeMulti.Wrong(self), text="{}".format(TypeMulti.wrong_ans[location[1]][wrongs]), font=Letters)
                    wrongs -= 1

                if row_index == 1:
                    btn.grid(row=row_index, column=col_index, sticky=N+S+E+W, padx=20, pady=(20, 20))
                else:
                    btn.grid(row=row_index, column=col_index, sticky=N+S+E+W, padx=20, pady=20)
        self.pack(expand=1, fill=BOTH)

        #Back Button
        TypeMulti.back = Button(self, text="Back", command=lambda Exit="nothing": TypeMulti.Leave(self, Exit))
        TypeMulti.back.grid(row = 3, column=0, sticky=N+W+S)

    def Right(self):
        PlayersFrame.addPoints(300)
        # disable the button we came from
        GBoard.DisableBtn(self.location)
        self.Leave("Right")
        
    
    def Wrong(self):
        PlayersFrame.addPoints(-300)
        PlayersFrame.Switch()
        #TODO better way to show that you are wrong.
        PlayerFrame.infoLabel.configure(text="Wrong!", foreground="red")


    def Leave(self, Exit):
        if Exit == "nothing":
            self.pack_forget()
            GBoard.pack(expand=1, fill=BOTH)
        else:
            self.pack_forget()
            GBoard.pack(expand=1, fill=BOTH)
            PlayerFrame.infoLabel.configure(text="Correct!", foreground="green")

#Just here for when we come up with 3rd game
class TypeGuess(Frame):
    right_ans=["ras","tes","yrs","uts","zvd"]
    qwert = [["q","w","e","r","t","y","u","i","o","p"],["a","s","d","f","g","h","j","k","l"],["z","x","c","v","b","n","m"]]
    def __init__(self, parent, question, location):
        Frame.__init__(self, parent)
        TypeGuess.the__answer=TypeGuess.right_ans[location[1]]
        qwerty=TypeGuess.qwert

        #Question Box
        TypeGuess.Que = Text(self, bg="light grey", height=8, font=Letters)
        TypeGuess.Que.insert("1.0", question)
        TypeGuess.Que.grid(row=0, column=3, columnspan=4, sticky=N)
        TypeGuess.Que.config(state=DISABLED)

        #Buttons for Letters
        for row_ind in range(1, len(qwerty)+1):
            Grid.rowconfigure(self, row_ind, weight=1)
            #individual keys
            for keys in range(len(qwerty[row_ind-1])):
                Grid.columnconfigure(self, keys, weight=1)
                key = Button(self, height=30, width=30, command=lambda letter=qwerty[row_ind-1][keys]: TypeGuess.process(self, letter), text="{}".format(qwerty[row_ind-1][keys]))

                if row_ind == 1:
                    key.grid(row=row_ind, column=keys, sticky=N+S+E+W, pady=(20, 20))
                elif row_ind == 3:
                    key.grid(row=row_ind, column=keys+1, sticky=N+S+E+W, pady=20)
                else:
                    key.grid(row=row_ind, column=keys, sticky=N+S+E+W, pady=20)

        self.pack(expand=1, fill=BOTH)

        #Entry for Answering
        TypeGuess.Ans = Entry(self, font=Letters)
        TypeGuess.Ans.grid(row=4, column=1, columnspan=8)
        TypeGuess.Ans.focus()

        #Back Button
        TypeGuess.back = Button(self, text="Back", command=lambda Exit="nothing": TypeGuess.Leave(self, Exit))
        TypeGuess.back.grid(row = 4, column=0, sticky=N+W+S)
        
        # Creating main label
        TypeGuess.display_used = StringVar()
        TypeGuess.display = Label(self, textvariable=TypeGuess.display_used, font=Letters)
        TypeGuess.display.grid(row=0, column=0, sticky=N+W+S+E, columnspan=2)
        TypeGuess.display_used.set("Used Letters:\n")

    def process(self, event):
        Used = TypeGuess.display_used.get()
        Used += event
        TypeGuess.display_used.set(Used)

        TypeGuess.Que.config(state=NORMAL)
        TypeGuess.Que.insert("1.0", "question")
        TypeGuess.Que.config(state=DISABLED)



    def Guessed(self):
        self.Leave("Guessed")

    def Leave(self, Exit):
        if Exit == "nothing":
            self.pack_forget()
            GBoard.pack(expand=1, fill=BOTH)
        else:
            self.pack_forget()
            GBoard.pack(expand=1, fill=BOTH)
            PlayerFrame.infoLabel.configure(text="Correct!", foreground="green")

class JepdyBoard(Frame):
    #cp=ValsandAns.ChoosePerson()
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.btns = []

    def Setup(self):
        #Create jeoparady board buttons
        for row_index in range(2,5):
            Grid.rowconfigure(self, row_index, weight=1)
            #number of columns
            for col_index in range(5):
                Grid.columnconfigure(self, col_index, weight=1)
                btn = Button(self, command=lambda location=((row_index-2),col_index): JepdyBoard.BtnClick(self, location), text="${}".format(300*(row_index-1)))
                self.btns.append(btn)
                if row_index == 2:
                    btn.grid(row=row_index, column=col_index, sticky=N+S+E+W, padx=10, pady=(20, 10))
                else:
                    btn.grid(row=row_index, column=col_index, sticky=N+S+E+W, padx=10, pady=10)
        self.pack(anchor=N, expand=1, fill=BOTH)

    def DisableBtn(self, location):
        self.btns[(location[0] * 5) + location[1]].configure(state="disabled")

    def BtnClick(self, location):
        #location is (row,column)
        #print(location)
        #Remove the jeoparady board
        self.pack_forget()
        if location[0] == 1:
            QFrame = TypeQuestion(window, ValsandAns.questions[location[0]][location[1]], location)
            QFrame.pack(expand=1, fill=BOTH)
        
        elif location[0] == 0:
            MFrame = TypeMulti(window, ValsandAns.questions[location[0]][location[1]], location)
            MFrame.pack(expand=1, fill=BOTH)

        elif location[0] == 2:
            GFrame = TypeGuess(window, ValsandAns.questions[location[0]][location[1]], location)
            GFrame.pack(expand=1, fill=BOTH)

            
        #print question in top texbox
        #ValsandAns.Questions(self, location)

window = Tk()
window.title("Ready Set Study!")
WIDTH = 800
HEIGHT = 500
window.geometry("{}x{}".format(WIDTH, HEIGHT))
#Make players frame and get their name somehow
GBoard = JepdyBoard(window)
Players = [Player("Player 1"), Player("Player 2")]
PlayersFrame = PlayerFrame(window)
#PlayersFrame.Setup()
GBoard.Setup()
window.mainloop()