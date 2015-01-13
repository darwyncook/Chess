__author__ = 'cook'
import tkinter as tk
import board  as bd
import chess_pieces as cp

root = tk.Tk()
root.title("Chess")
board = bd.Board(root)
chess_set = cp.Pieces(board)
root.mainloop()
