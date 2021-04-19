#!/usr/bin/python
import read_data.read_data as rd
import plot_data.live_plot as pd
import time
import obd
from tkinter import *
import threading

connection = obd.OBD("/dev/ttys002")  # auto-connects to USB or RF port
reader = rd.DataReader(connection)
t1 = threading.Thread(target=reader.read_cmds, args=(999, 1, False, 0.05))
t1.start()
samples = 75

root = Tk()
text = "OBD2 Data Plotter"
label = Label(root, text=text)
label.pack()

cmds_lbl = Label(root, text="Supported Commands")
cmds_listbox = Listbox(root, selectmode='multiple', width=40, height=50)
i = 1
cmds = []
for cmd in connection.supported_commands:
    cmds.append(cmd.name)
cmds.sort()
for cmd in cmds:
    cmds_listbox.insert(i, cmd)
    i += 1
run_btn = Button(root, text="Graph", command=lambda listbox=cmds_listbox: cmds_listbox.delete(ACTIVE))
cmds_lbl.pack()
cmds_listbox.pack()
run_btn.pack()

quit = Button(root, text="QUIT", command=root.destroy)
quit.pack()

# The following three commands are needed so the window pops
# up on top on Windows...
root.iconify()
root.update()
root.deiconify()
root.mainloop()
t1.join()
