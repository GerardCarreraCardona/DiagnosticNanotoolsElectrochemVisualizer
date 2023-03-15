from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from bs4 import BeautifulSoup as bs
import numpy as np
import csv
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style
import matplotlib.pyplot as plt


root = Tk()
root.title('.mta point intensity reader')
root.resizable(False, False)

filename = StringVar()
initial_time_string = StringVar()
final_time_string = StringVar()
final_time_bool = False
def openFile():
    filename.set(fd.askopenfilename())

def generatePlot(xs,ys):
    fig = Figure()
    ax1 = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig,master=root)
    canvas.grid(column=0, row=3)

def getValues(path):
    if path == "":
        return
    with open(path,"r") as file:
        data = file.read()
    xml = bs(data)
    curves = xml.find_all("curve")
    potentials = []
    intensities = []
    lengths = []
    intervals = []
    names = []

    for i,curve in enumerate(curves):
        name = curve.find("name").string
        potentials_raw_string_array = curve.find("time").text.split(',')
        potentials_raw_int_array = [eval(i) for i in potentials_raw_string_array]
        potentials_np_array = np.array(potentials_raw_int_array)
        potentials.append(potentials_np_array)
        
        intensities_raw_string_array = curve.find("i1").text.split(',')
        intensities_raw_int_array = [eval(i) for i in intensities_raw_string_array]
        intensities_np_array = np.array(intensities_raw_int_array)
        intensities.append(intensities_np_array)
        
        length = len(potentials_np_array)
        lengths.append(length)
        intervals.append(eval(curve.find("interval").text))
        names.append(name)
    return [np.resize(i,min(lengths)) for i in potentials],[np.resize(i,min(lengths)) for i in intensities],intervals,names       

def Main():
    generatePlot(1,1)
    if (filename.get() == ""):
        return
    x1,y1,inters,names = getValues(filename.get())
    if final_time_bool == False:
        heights = []
        for i in range(len(y1)):
            heights.append(y1[i][int(float(initial_time_string.get())/inters[i])])
        f = fd.asksaveasfile(initialfile = 'Untitled.csv',mode='w', defaultextension=".csv")
        with open(f.name,"w")as saved_file:
            writer = csv.writer(saved_file, delimiter='\t')
            writer.writerow(names)
            writer.writerow(heights)    
        quit()



frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="1) Abrir archivo .mta").grid(column=0, row=0)
ttk.Button(frm, text="Abrir", command=openFile).grid(column=2, row=0)
initial_time_entry = ttk.Label(frm, text="2) Establecer tiempo inicial (s):").grid(column=0, row=1)
ttk.Entry(frm,textvariable=initial_time_string).grid(column=2, row=1)
#ttk.Label(frm, text="3) Establecer tiempo final (s):").grid(column=0, row=2)
#ttk.Checkbutton(frm,variable = final_time_bool, onvalue = True, offvalue = False).grid(column=1, row=2)
#final_time_entry = ttk.Entry(frm).grid(column=2, row=2)
ttk.Label(frm, text="4) Guardar achivo como .csv").grid(column=0, row=4)
ttk.Button(frm, text="Guardar", command=Main).grid(column=2, row=4)
root.mainloop()