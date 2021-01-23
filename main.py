from tkinter import *
class JepdyBoard(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

    def Setup(self):
        #Create jeoparady board buttons
        for row_index in range(3):
            Grid.rowconfigure(self, row_index, weight=1)
            #number of columns
            for col_index in range(5):
                Grid.columnconfigure(self, col_index, weight=1)
                btn = Button(self, command=lambda location=(row_index,col_index): JepdyBoard.BtnClick(self, location), text=f"${200*(row_index+1)}")
                if row_index == 0:
                    btn.grid(row=row_index, column=col_index, sticky=N+S+E+W, padx=10, pady=(80, 10))
                else:
                    btn.grid(row=row_index, column=col_index, sticky=N+S+E+W, padx=10, pady=10)
        self.pack(expand=1, fill=BOTH)

    def BtnClick(self, location):
        #location is (row,column)
        print(f"{location[0]}x{location[1]}")

window = Tk()
window.title("Ready Set Study!")
WIDTH = 800
HEIGHT = 400
window.geometry("{}x{}".format(WIDTH, HEIGHT))
GBoard = JepdyBoard(window)
GBoard.Setup()
window.mainloop()