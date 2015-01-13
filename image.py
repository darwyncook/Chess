__author__ = 'cook'
from PIL import ImageTk
from tkinter import *


canvas_width = 300
canvas_height =300

master = Tk()

canvas = Canvas(master,
           width=canvas_width,
           height=canvas_height)
canvas.pack()

img = ImageTk.PhotoImage(file="pieces_image/kwhite.png")
canvas.create_image(32,32, anchor='c', image=img)

mainloop()
