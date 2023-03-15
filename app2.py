import tkinter
from tkinter import StringVar
from tkinter import filedialog as fd
from bs4 import BeautifulSoup as bs
import numpy as np
import csv

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

ipadding = {'ipadx': 10, 'ipady': 10}

# DEFINE TK SETUP
root = tkinter.Tk()
root.wm_title("ELECTROCHEM ANALYZER DINA")

# VARIABLES
filename = StringVar()
initial_time_string = StringVar()
final_time_string = StringVar()
final_time_bool = False

def openFile():
    filename.set(fd.askopenfilename())



fig = Figure(figsize=(5, 4), dpi=100)

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

# START TKINTER
label1 = tkinter.Label(root, text="1) Abrir archivo .mta")
label1.pack(**ipadding, expand=True, fill=tkinter.BOTH, side=tkinter.LEFT)
openbutton = tkinter.Button(root, text="Abrir", command=openFile)
openbutton.pack(**ipadding, expand=True, fill=tkinter.BOTH, side=tkinter.LEFT)
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(**ipadding, fill=tkinter.X)

tkinter.mainloop()