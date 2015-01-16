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
        inpt.pack(pady=7)
        self.checkmate = Label(inpt, text='')
        self.checkmate.pack(fill=X)
        self.boardframe = Frame(self.parent)
        self.boardframe.pack()
        self.blackcaptured = Canvas(self.boardframe, height=Board.canvas_height, width=Board.dim_square*2, bg='antique white')
        self.canvas = Canvas(self.boardframe, width=Board.canvas_width, height=Board.canvas_height, bg="grey")
        self.whitecaptured = Canvas(self.boardframe, height=Board.canvas_height, width=Board.dim_square*2, bg='antique white')

        self.whitecaptured.pack(padx=4, side=LEFT)
        self.canvas.pack(padx=3, pady=3, side=LEFT)
        self.blackcaptured.pack(padx=4, side=LEFT)
        turnframe = Frame(parent)
        turnframe.pack()
        self.whose_turn = Label(turnframe, text='')
        self.whose_turn.pack(pady=4, anchor="w")

    def swap_colors(self, color):
        if color == Board.color1:
            return Board.color2
        else:
            return Board.color1


def main():
    root = Tk()
    root.title("Chess")
    gui = Board(root)
    root.mainloop()

if __name__ == "__main__":
    main()

#
