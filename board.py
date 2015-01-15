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
        self.checkmate.pack(fill=X, side=LEFT)
        self.boardframe = Frame(self.parent)
        self.boardframe.pack()
        self.blackcaptured = Canvas(self.boardframe, height=Board.canvas_height, width=Board.dim_square*2, bg='antique white')
        self.blackcaptured.pack(padx=4, side=LEFT)
        self.canvas = Canvas(self.boardframe, width=Board.canvas_width, height=Board.canvas_height, bg="grey")
        self.canvas.pack(padx=3, pady=3, side=LEFT)
        self.whitecaptured = Canvas(self.boardframe, height=Board.canvas_height, width=Board.dim_square*2, bg='antique white')
        self.whitecaptured.pack(padx=4, side=LEFT)
#        self.captbwin = self.blackcaptured.create_text(2, 2, text='', anchor=NW, width=Board.dim_square*2)
#        self.captwwin = self.whitecaptured.create_text(2, 2, text='', anchor=NW, width=Board.dim_square*2)
        turnframe = Frame(parent)
        turnframe.pack()
        self.whose_turn = Label(turnframe, text='')
        self.whose_turn.pack(pady=4, anchor="w")

    def swap_colors(self, color):
        if color == Board.color1:
            return Board.color2
        else:
            return Board.color1


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
