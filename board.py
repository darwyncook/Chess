__author__ = 'cook'
from PIL import ImageTk
from tkinter import *


class Board():
    rows = 8
    columns = 8
    color1 = "#DDB88C"
    color2 = "#A66D4F"
    dim_square = 64
    canvas_width = columns * dim_square
    canvas_height = rows * dim_square
    def __init__(self, parent):
        self.parent = parent
        inpt = Frame(self.parent)
        inpt.pack(pady=7, anchor=W)
        self.checkmate = Label(inpt, text='')
        self.checkmate.pack(fill=X, anchor=W, side=LEFT)
        boardframe = Frame(self.parent)
        boardframe.pack()
        self.blackcaptured = Canvas(boardframe, height=Board.canvas_height, width=Board.dim_square, bg='antique white')
        self.blackcaptured.pack(padx=4, side=LEFT)
        self.canvas = Canvas(boardframe, width=Board.canvas_width, height=Board.canvas_height, bg="grey")
        self.canvas.pack(padx=8, pady=8, ipadx=3, ipady=3, side=LEFT)
        self.whitecaptured = Canvas(boardframe, height=Board.canvas_height, width=Board.dim_square, bg='antique white')
        self.whitecaptured.pack(padx=4, side=LEFT)
        self.captbwin = self.blackcaptured.create_text(2, 2, text='', anchor=NW, width=Board.dim_square)
        self.captwwin = self.whitecaptured.create_text(2, 2, text='', anchor=NW, width=Board.dim_square)
        turnframe = Frame(parent)
        turnframe.pack()
        self.whose_turn = Label(turnframe, text='')
        self.whose_turn.pack(pady=4, anchor="w")

#        img = ImageTk.PhotoImage(file="pieces_image/kwhite.png")
#        self.canvas.create_image(32,32, anchor='c', image=img)
#        self.canvas.create_image(0, 0, image=img, tags=('black night', "occupied"), anchor="c")
  #      self.canvas.coords('black knight', 32, 32)
        self.draw_board()
 #       i = self.canvas.create_text(canvas_width / 2, canvas_height / 2, text="Python")
 #       self.canvas.coords(i, (30,30))

    def swap_colors(self, color):
        if color == Board.color1:
            return Board.color2
        else:
            return Board.color1

    def draw_board(self, highlight=[]):
        color = self.color2
        for r in range(self.rows):
            color = self.swap_colors(color)
            for c in range(self.columns):
                temp = color
                if [c,7-r] in highlight:
                    color = "yellow"
                x1 = (c * self.dim_square)
                y1 = ((7-r) * self.dim_square)
                x2 = x1 + self.dim_square
                y2 = y1 + self.dim_square
                self.canvas.create_rectangle(x1, y1, x2, y2,
                fill=color, tags="area")
                color = temp
                color = self.swap_colors(color)
#        image = Image.open("pieces_image/kwhite.png")
#        photo = ImageTk.PhotoImage(image)
    #    photo = ImageTk.PhotoImage(file='pieces_image/kwhite.png')
    #    self.canvas.create_image(0, 0, image=photo, tags=('black night', "occupied"), anchor="c", state=NORMAL)
    #    self.canvas.coords('black knight', 32, 32)


def main():
    root = Tk()
    root.title("Chess")
    gui = Board(root)
    root.mainloop()

if __name__ == "__main__":
    main()

#
