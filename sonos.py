#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Sonos-GUI-URI

This is the first attempt to create a window to stream a URI to the Sonos Speakers.

Author: Jim Scherer
"""

from Tkinter import Tk, LEFT, RIGHT, BOTH, RAISED, Listbox, StringVar, END, X
from ttk import Frame, Style, Label, Button, Entry
import tkMessageBox as mbox

import soco


class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.initUI()


    def initUI(self):

        self.parent.title("Sonos URI")

        self.pack(fill=BOTH, expand=1)

        self.style = Style()
        self.style.theme_use("default")

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        self.pack(fill=BOTH, expand=True)

        lb = Listbox(frame)
        for i in soco.discover():
            lb.insert(END, i.player_name)

        lb.bind("<<ListboxSelect>>", self.onSelect)

        lb.pack(pady=15)

        self.var = StringVar()
        self.label = Label(frame, text=0, textvariable=self.var)
        self.label.pack()

        self.lblUri = Label(frame, text="URI", width=6)
        self.lblUri.pack(side=LEFT, padx=5, pady=5)

        self.entryUri = Entry(frame)
        self.entryUri.pack(fill=X, padx=5, expand=True)

        self.lblPlayfile = Label(frame, text=0, textvariable=self.entryUri)

        closeButton = Button(self, text="Close", command=self.parent.destroy)
        closeButton.pack(side=RIGHT, padx=5, pady=5)
        okButton = Button(self, text="OK", command=self.onOk)
        okButton.pack(side=RIGHT)

    def onOk(self):
        mbox.showinfo("Info", self.parent.entryUri.val)

    def onSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)

        self.var.set(value)

def main():

    root = Tk()
    ex = Example(root)
    root.geometry("900x350+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()