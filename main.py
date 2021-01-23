from tkinter import *
#import Rpi.GPIO as GPIO
from time import sleep
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
class ValuesandAnswers():
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
        questions=[["a1","b1","c1","d1","e1"],
                   ["a2","b2","c2","d2","e2"], 
                   ["a3","b3","c3","d3","e3"]]
        if location[0] == 0:
            if location[1] == 0:
                JepdyBoard.Que.insert(END, questions[0][0])
            elif location[1] == 1:
                JepdyBoard.Que.insert(END, questions[0][1])
            elif location[1] == 2:
                JepdyBoard.Que.insert(END, questions[0][2])
            elif location[1] == 3:
                JepdyBoard.Que.insert(END, questions[0][3])
            elif location[1] == 4:
                JepdyBoard.Que.insert(END, questions[0][4])
        elif location[0] == 1:
            if location[1] == 0:
                JepdyBoard.Que.insert(END, questions[1][0])
            elif location[1] == 1:
                JepdyBoard.Que.insert(END, questions[1][1])
            elif location[1] == 2:
                JepdyBoard.Que.insert(END, questions[1][2])
            elif location[1] == 3:
                JepdyBoard.Que.insert(END, questions[1][3])
            elif location[1] == 4:
                JepdyBoard.Que.insert(END, questions[1][4])
        else:
            if location[1] == 0:
                JepdyBoard.Que.insert(END, questions[2][0])
            elif location[1] == 1:
                JepdyBoard.Que.insert(END, questions[2][1])
            elif location[1] == 2:
                JepdyBoard.Que.insert(END, questions[2][2])
            elif location[1] == 3:
                JepdyBoard.Que.insert(END, questions[2][3])
            elif location[1] == 4:
                JepdyBoard.Que.insert(END, questions[2][4])

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

class JepdyBoard(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

    def Setup(self):
        #Create jeoparady board buttons
        for row_index in range(2,5):
            Grid.rowconfigure(self, row_index, weight=1)
            #number of columns
            for col_index in range(5):
                Grid.columnconfigure(self, col_index, weight=1)
                btn = Button(self, command=lambda location=((row_index-2),col_index): JepdyBoard.BtnClick(self, location), text=f"${200*(row_index+1)}")
                if row_index == 2:
                    btn.grid(row=row_index, column=col_index, sticky=N+S+E+W, padx=10, pady=(20, 10))
                else:
                    btn.grid(row=row_index, column=col_index, sticky=N+S+E+W, padx=10, pady=10)
        self.pack(expand=1, fill=BOTH)

    #Create entry to enter answers
        JepdyBoard.Answering = Entry(self,font=Letters ,width = 10)
        JepdyBoard.Answering.grid(row=(row_index+1), column=1, sticky=N+S+E+W, ipady=10, columnspan=(col_index-1))
        JepdyBoard.Answering.bind("<Return>", self.PressEnter)

        #Labels to show score, question, and maybe who's turn it is.
        JepdyBoard.Que = Text(self, bg="light grey", width=1, height=5 , state=DISABLED, font=Letters)
        JepdyBoard.Que.grid(row=0, column=1, rowspan=2, columnspan = 3, sticky=N+S+E+W)

    def BtnClick(self, location):
        #location is (row,column)
        print(f"{location[0]}x{location[1]}")
        ValuesandAnswers.Questions(self, location)
    
    def PressEnter(self, Anything):
        JepdyBoard.Answering.delete(0, END)

window = Tk()
window.title("Ready Set Study!")
WIDTH = 800
HEIGHT = 400
window.geometry("{}x{}".format(WIDTH, HEIGHT))
GBoard = JepdyBoard(window)
GBoard.Setup()
window.mainloop()