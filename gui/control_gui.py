#!/usr/bin/python
import read_data.read_data as rd
import plot_data.live_plot as pd
import time
import obd
from tkinter import *
import threading
import matplotlib.pyplot as plt

import matplotlib.animation as animation


def main():
    print("Running GUI")
    run_gui()

def run_gui():

    root = Tk()
    root.title("OBD Data Tools")
    text = "OBD2 Data Plotter"
    label = Label(root, text=text).grid(row=0, columnspan=2)
    # label.pack()

    # Add Port Field
    port_var = StringVar()
    port_var.set("/dev/ttys001")
    port_lbl = Label(root, text="Connection Port").grid(row=1)
    port_entry = Entry(root, textvariable=port_var).grid(row=1, column=1)

    # Add connect Button
    connect_btn = Button(root, text="Connect", command=lambda: connect(port_var.get(), cmds_listbox))
    # connect_btn.pack()
    connect_btn.grid(row=2, columnspan=2)

    # Add list of commands
    cmds_listbox = Listbox(root, selectmode='multiple', width=40, height=40)
    cmds_listbox.grid(padx=10, sticky=NE, columnspan=2)
    # cmds_listbox.pack(padx=10, pady=10, fill=BOTH, expand=True)

    # Add Samples Field
    samples_var = IntVar()
    samples_var.set("50")
    samples_lbl = Label(root, text="Plot Samples").grid(row=4)
    samples_entry = Entry(root, textvariable=samples_var).grid(row=4, column=1)

    # Add Running Average Field
    r_average_var = IntVar()
    r_average_var.set("10")
    r_average_lbl = Label(root, text="Running Average").grid(row=5)
    r_average_entry = Entry(root, textvariable=r_average_var).grid(row=5, column=1)

    # Add Run Button
    running_average = 10
    graph_btn = Button(root, text="Graph",
                       command=lambda listbox=cmds_listbox: graph(get_selected_item(listbox), samples_var.get(),
                                                                  r_average_var.get()))
    graph_btn.grid(row=6, columnspan=2)

    quit_btn = Button(root, text="QUIT", command=root.destroy)
    quit_btn.grid(row=7, columnspan=2)

    # The following three commands are needed so the window pops
    # up on top on Windows...
    root.iconify()
    root.update()
    root.deiconify()

    root.mainloop()
    # t1.join()


def show_entry_fields(e1, e2):
    print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))


def connect(port, cmds_listbox):
    print("Connecting to port " + port)
    connection = obd.OBD(port)  # auto-connects to USB or RF port
    reader = rd.DataReader(connection)
    t1 = threading.Thread(target=reader.read_cmds, args=(999, 1, False, 0.05), daemon=True)
    t1.start()
    i = 1
    cmds = []
    for cmd in connection.supported_commands:
        cmds.append(cmd.name)
    cmds.sort()
    update_cmds_list(cmds, cmds_listbox)
    print(cmds)
    return cmds


def update_cmds_list(cmds, cmds_listbox):
    i = 0
    for cmd in cmds:
        cmds_listbox.insert(i, cmd)
        i += 1


def graph(cmds, samples, running_average):
    print(str(cmds))
    plt.close()
    ld = pd.LivePlot(cmds, samples=samples, running_average=running_average)
    plt.show()


def get_selected_item(listbox):
    items = []
    for item in listbox.curselection():
        print(listbox.get(item))
        items.append(listbox.get(item))
    return items


if __name__ == '__main__':
    main()
