import tkinter as tk
from Game import conny4

class GUI:
    def __init__(self, game = conny4()):
        self.game = game
        self.root = tk.Tk()
        self.root.geometry('1001x1001+100+100')
        for i in range(7):
            self.root.columnconfigure(i, weight = 1)
            self.root.rowconfigure(i, weight = 1)
        for i in range(7):
            tk.Button(self.root,text = 'DROP',command=lambda i = i: self.move(pos = i)).grid(column=i, row = 0)
        for i in range(6):
            for j in range(7):
                    canvas = tk.Canvas(self.root, width=143, height = 143)
                    canvas.grid(row=i+1,column=j)
                    canvas.create_oval(10,10,133,133)
        self.translate_board()
        
    def move(self, pos):
        self.game.turn(pos)
        self.translate_board()
        
    def translate_board(self):
        colour = {-1: 'yellow', 1:'red'}
        for row in range(6):
            for col in range(7):
                if self.game.board[row,col] == 0:
                    pass
                if self.game.board[row,col] == 1 or self.game.board[row,col] == -1:
                    canvas = tk.Canvas(self.root, width=143, height = 143)
                    canvas.grid(row=row+1,column=col)
                    canvas.create_oval(10,10,133,133, fill = colour[self.game.board[row,col]] )
    
    def go(self):
        self.root.mainloop()

game = GUI()
game.go()
