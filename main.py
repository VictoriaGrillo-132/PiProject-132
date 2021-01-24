from tkinter import *
#import Rpi.GPIO as GPIO
from random import randint
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
    questions = [["a1","b1","c1","d1","e1"],
                ["a2","b2","c2","d2","e2"], 
                ["a3","b3","c3","d3","e3"]]
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

class TypeQuestion(Frame):
    right_ans=["r","t","y","u","z"]
    def __init__(self, parent, question, location):
        Frame.__init__(self, parent)

        TypeQuestion.the_que=question
        TypeQuestion.the__answer=location[1]

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
        print("Right")
        self.Leave("Right")

    def Wrong(self):
        print("Wrong")
        TypeQuestion.Que.config(state=NORMAL)
        TypeQuestion.Que.delete("1.0",END)
        TypeQuestion.Que.insert(END, TypeQuestion.the_que + "\nWrong")
        TypeQuestion.Que.config(state=DISABLED)

    def Leave(self, Exit):
        if Exit == "nothing":
            self.pack_forget()
            GBoard.pack(expand=1, fill=BOTH)
            JepdyBoard.Que.delete("1.0",END)
        else:
            self.pack_forget()
            GBoard.pack(expand=1, fill=BOTH)
            JepdyBoard.Que.config(state=NORMAL)
            JepdyBoard.Que.delete("1.0",END)
            JepdyBoard.Que.insert(END, "Right")
            JepdyBoard.Que.config(state=DISABLED)

class TypeMulti(Frame):
    right_ans=["V","W","X","Y","Z"]
    wrong_ans=[["A","B","C"],["D","E","F"],["G","H","I"],["J","K","L"],["M","N","O"]]
    def __init__(self, parent, question, location):
        Frame.__init__(self, parent)

        TypeMulti.the_que=question

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
                    btn = Button(self, width=20, command=lambda Right=1: TypeMulti.Right(self), text=f"{TypeMulti.right_ans[location[1]]}")
                else:
                    btn = Button(self, width=20, command=lambda Wrong=1: TypeMulti.Wrong(self), text=f"{TypeMulti.wrong_ans[location[1]][wrongs]}")
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
        print("Right")
        self.Leave("Right")
    
    def Wrong(self):
        #print("Wrong")
        TypeMulti.Que.config(state=NORMAL)
        TypeMulti.Que.delete("1.0",END)
        TypeMulti.Que.insert(END, TypeMulti.the_que + "\nWrong")
        TypeMulti.Que.config(state=DISABLED)


    def Leave(self, Exit):
        if Exit == "nothing":
            self.pack_forget()
            GBoard.pack(expand=1, fill=BOTH)
            JepdyBoard.Que.delete("1.0",END)
        else:
            self.pack_forget()
            GBoard.pack(expand=1, fill=BOTH)
            JepdyBoard.Que.config(state=NORMAL)
            JepdyBoard.Que.delete("1.0",END)
            JepdyBoard.Que.insert(END, "Right")
            JepdyBoard.Que.config(state=DISABLED)

#Just here for when we come up with 3rd game
class TypeGuess(Frame):
    right_ans=["ras","tes","yrs","uts","zvd"]
    def __init__(self, parent, question, location):
        Frame.__init__(self, parent)
        TypeQuestion.the__answer=location[1]

        #Question Box
        TypeGuess.Que = Text(self, bg="light grey", height=2, font=Letters)
        TypeGuess.Que.insert("1.0", question)
        TypeGuess.Que.pack(anchor=N, fill=X)
        TypeGuess.Que.config(state=DISABLED)

        #Entry for Answering
        TypeGuess.Ans = Entry(self, font=Letters)
        TypeGuess.Ans.bind("<Return>", self.process)
        TypeGuess.Ans.pack(anchor=S, fill=X, side=BOTTOM)
        TypeGuess.Ans.focus()

        #Back Button
        TypeGuess.back = Button(self, text="Back", command=self.Leave)
        TypeGuess.back.pack(anchor=SW, expand=1)

    def process(self, event):
        pass
        response = TypeGuess.Ans.get()
        response = response.lower()

        if response == TypeGuess.right_ans[TypeQuestion.the__answer]:
            self.Right()
        else:
            self.Wrong()

        TypeQuestion.Ans.delete(0, END)       

    def Right(self):
        print("Right")

    def Wrong(self):
        print("Wrong")

    def Leave(self):
        self.pack_forget()
        GBoard.pack(expand=1, fill=BOTH)

class JepdyBoard(Frame):
    #current player
    #cp=ValsandAns.ChoosePerson()
    
    def __init__(self, parent):
        Frame.__init__(self, parent)

    def Setup(self):
        #Create jeoparady board buttons
        for row_index in range(2,5):
            Grid.rowconfigure(self, row_index, weight=1)
            #number of columns
            for col_index in range(5):
                Grid.columnconfigure(self, col_index, weight=1)
                btn = Button(self, command=lambda location=((row_index-2),col_index): JepdyBoard.BtnClick(self, location), text=f"${300*(row_index-1)}")
                if row_index == 2:
                    btn.grid(row=row_index, column=col_index, sticky=N+S+E+W, padx=10, pady=(20, 10))
                else:
                    btn.grid(row=row_index, column=col_index, sticky=N+S+E+W, padx=10, pady=10)
        self.pack(expand=1, fill=BOTH)

        #Labels to show score, question, and maybe who's turn it is.
        JepdyBoard.Que = Text(self, bg="light grey", width=1, height=5 , state=DISABLED, font=Letters)
        JepdyBoard.Que.grid(row=0, column=1, rowspan=2, columnspan = 3, sticky=N+S+E+W)

    def BtnClick(self, location):
        #location is (row,column)
        print(f"{location[0]}x{location[1]}")
        #Remove the jeoparady board
        self.pack_forget()
        if location[0] == 1:
            QFrame = TypeQuestion(window, ValsandAns.questions[location[0]][location[1]], location)
            QFrame.pack(expand=1, fill=BOTH)
        
        elif location[0] == 0:
            MFrame = TypeMulti(window, ValsandAns.questions[location[0]][location[1]], location)
            MFrame.pack(expand=1, fill=BOTH)

        elif location[0] == 2:
            GFrame = TypeMulti(window, ValsandAns.questions[location[0]][location[1]], location)
            GFrame.pack(expand=1, fill=BOTH)

            
        #print question in top texbox
        #ValsandAns.Questions(self, location)

window = Tk()
window.title("Ready Set Study!")
WIDTH = 800
HEIGHT = 400
window.geometry("{}x{}".format(WIDTH, HEIGHT))
GBoard = JepdyBoard(window)
GBoard.Setup()
window.mainloop()