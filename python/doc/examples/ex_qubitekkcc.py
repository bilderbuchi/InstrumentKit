#Qubitekk Coincidence Counter example
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.figure import Figure

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler

import instruments as ik

import Tkinter as tk
import re
#open connection to coincidence counter. If you are using Windows, this will be a com port. On linux, it will show up in /dev/ttyusb
cc = ik.qubitekk.CC1.open_serial('COM8', 19200,timeout=1)
#i is used to keep track of time
i = 0

def clearcounts(*args):
    cc.clear_counts()
    
def getvalues(i):
    #set counts labels
    chan1counts.set(cc.channel[0].count)
    chan2counts.set(cc.channel[1].count)
    coinccounts.set(cc.channel[2].count)
    #add count values to arrays for plotting
    chan1vals.append(cc.channel[0].count)
    chan2vals.append(cc.channel[1].count)
    coincvals.append(cc.channel[2].count)
    t.append(i*0.1)
    i = i+1
    #plot values
    p1, = a.plot(t,coincvals,color="r",linewidth=2.0)
    p2, = a.plot(t,chan1vals,color="b",linewidth=2.0)
    p3, = a.plot(t,chan2vals,color="g",linewidth=2.0)
    a.legend([p1,p2,p3],["Coincidences","Channel 1", "Channel 2"])
    a.set_xlabel('Time (s)')
    a.set_ylabel('Counts (Hz)')

    canvas.show()
    #get the values again in 100 milliseconds
    root.after(100,getvalues,i)

def gateenable():
    if(gateenabled.get()):
        cc.gate_enable = 1
    else:
        cc.gate_enable = 0

def parse(*args):
    cc.dwell_time = float(re.sub("[A-z]", "", dwell_time.get()))
    cc.window = float(re.sub("[A-z]", "", window.get()))

root = tk.Tk()
root.title("Qubitekk Coincidence Counter Control Software")

#set up the Tkinter grid layout
mainframe = tk.Frame(root)
mainframe.padding = "3 3 12 12"
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

#set up the label text
dwelltime = tk.StringVar()
dwelltime.set(cc.dwell_time)

window = tk.StringVar()
window.set(cc.window)

chan1counts = tk.StringVar()
chan1counts.set(cc.channel[0].count)
chan2counts = tk.StringVar()
chan2counts.set(cc.channel[1].count)
coinccounts = tk.StringVar()
coinccounts.set(cc.channel[2].count)

gateenabled = tk.IntVar()

#set up the initial checkbox value for the gate enable
if(cc.gateenable=="enabled"):
    gateenabled.set(1)
else:
    gateenabled.set(0)

#set up the plotting area

f = Figure(figsize=(10,8), dpi=100)
a = f.add_subplot(111,axisbg='black')

t = []
coincvals = []
chan1vals = []
chan2vals = []


# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, mainframe)
canvas.get_tk_widget().grid(column=3,row=1,rowspan=8,sticky=tk.W)

#label initialization
dwelltime_entry = tk.Entry(mainframe, width=7, textvariable=dwelltime,font="Verdana 20")
dwelltime_entry.grid(column=2,row=2,sticky=(tk.W,tk.E))
window_entry = tk.Entry(mainframe, width=7, textvariable=window,font="Verdana 20")
window_entry.grid(column=2,row=3,sticky=(tk.W,tk.E))
qubitekklogo = tk.PhotoImage(file="qubitekklogo.gif")

tk.Label(mainframe,image=qubitekklogo).grid(column=1,row=1,columnspan=2)

tk.Label(mainframe, text="Dwell Time:",font="Verdana 20").grid(column=1,row=2,sticky=tk.W)
tk.Label(mainframe, text="Window size:",font="Verdana 20").grid(column=1,row=3,sticky=tk.W)

tk.Checkbutton(mainframe,font="Verdana 20",variable = gateenabled, command=gateenable).grid(column=2,row=4)
tk.Label(mainframe,text="Gate Enable: ",font="Verdana 20").grid(column=1,row=4,sticky=tk.W)


tk.Label(mainframe, text="Channel 1: ",font="Verdana 20").grid(column=1,row=5,sticky=tk.W)
tk.Label(mainframe, text="Channel 2: ",font="Verdana 20").grid(column=1,row=6,sticky=tk.W)
tk.Label(mainframe, text="Coincidences: ",font="Verdana 20").grid(column=1,row=7,sticky=tk.W)



tk.Label(mainframe, textvariable=chan1counts,font="Verdana 34",fg="white",bg="black").grid(column=2,row=5,sticky=tk.W)
tk.Label(mainframe, textvariable=chan2counts,font="Verdana 34",fg="white",bg="black").grid(column=2,row=6,sticky=tk.W)
tk.Label(mainframe, textvariable=coinccounts,font="Verdana 34",fg="white",bg="black").grid(column=2,row=7,sticky=tk.W)

tk.Button(mainframe,text="Clear Counts",font="Verdana 24",command=clearcounts).grid(column=2,row=8,sticky = tk.W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
#when the enter key is pressed, send the current values in the entries to the dwelltime and window to the coincidence counter
root.bind('<Return>',parse)
#in 100 milliseconds, get the counts values off of the coincidence counter
root.after(100,getvalues,i)
#start the GUI
root.mainloop()