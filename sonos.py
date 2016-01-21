#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Sonos-GUI-URI

This is the first attempt to create a window to stream a URI to the Sonos Speakers.

Author: Jim Scherer
"""

from Tkinter import Tk, LEFT, RIGHT, BOTH, RAISED, Listbox, StringVar, END, X, Scale, HORIZONTAL
from ttk import Frame, Style, Label, Button, Entry

import tkMessageBox as mbox

import soco as sonosLib

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.sonos = sonosLib.SoCo('192.168.11.226')

        self.initUI()


    def initUI(self):

        self.parent.title("Sonos URI")

        self.pack(fill=BOTH, expand=1)

        self.style = Style()
        self.style.theme_use("default")


# Slider

        frame0 = Frame(self)
        frame0.pack(fill=BOTH)

        muteButton = Button(frame0, text="Mute", width=4)
        muteButton.pack(side=LEFT, padx=2)
        muteButton.bind('<Button-1>', self.onMute)

        self.volume = Scale(frame0, from_=0, to=100, orient=HORIZONTAL, showvalue=0)
        self.volume.set(self.sonos.volume)
        self.volume.pack(side=LEFT, padx=2)
        self.volume.bind('<ButtonRelease>', self.onSlide)

        stopButton = Button(frame0, text="Stop", width=4)
        stopButton.pack(side=LEFT, padx=2)
        stopButton.bind('<Button-1>', self.onStop)

        prevButton = Button(frame0, text="<< Prev", width=6)
        prevButton.pack(side=LEFT, padx=(150,2))
        prevButton.bind('<Button-1>', self.onSend)

        self.playButton = Button(frame0, text="Play", width=4)
        self.playButton['text'] = 'Pause' if self.sonos.get_current_transport_info()['current_transport_state']=='PLAYING' else 'Play'
        self.playButton.pack(side=LEFT, padx=2)
        self.playButton.bind('<Button-1>', self.onPlayPause)

        nextButton = Button(frame0, text="Next >>", width=6)
        nextButton.pack(side=LEFT, padx=2)
        nextButton.bind('<Button-1>', self.onNext)

# Frame
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        self.pack(fill=BOTH, expand=True)

# Listbox
        lb = Listbox(frame)
        for i in sonosLib.discover():
            lb.insert(END, i.player_name)

        lb.bind("<<ListboxSelect>>", self.onSelect)

        lb.pack(pady=15)
        self.varLb = StringVar()
        self.lblLb = Label(frame, text=0, textvariable=self.varLb)
        self.lblLb.pack()
# Uri
        self.lblUri = Label(frame, text="URI")
        self.lblUri.pack(side=LEFT, padx=2, pady=2)

        self.entryUri = Entry(frame)
        self.entryUri.pack(side=LEFT, padx=2, fill=X, expand=True)

        sendButton = Button(frame, text="Send")
        sendButton.pack(side=RIGHT, padx=2)
        sendButton.bind('<Button-1>', self.onSend)

        self.varSentfile = StringVar()
        self.lblSentfile = Label(self, text=None, width=100, textvariable=self.varSentfile)
        self.lblSentfile.pack(side=LEFT, padx=1, pady=1)


#        mbox.showinfo('Test Message', 'Got Here')

    def onSlide(self, val):

        self.sonos.volume=self.volume.get()

    def onMute(self, var):

        self.sonos.mute = not self.sonos.mute

    def onStop(self, var):

        self.sonos.stop()

    def onPlayPause(self, var):

        if self.sonos.get_current_transport_info()['current_transport_state']=='PLAYING':
            self.sonos.pause()
            self.playButton['text'] = "Play"
        elif self.sonos.get_current_transport_info()['current_transport_state']=='PAUSED_PLAYBACK':
            self.sonos.play()
            self.playButton['text'] = "Pause"
        elif self.sonos.get_current_transport_info()['current_transport_state']=="STOPPED":
            self.sonos.play()
            self.playButton['text'] = "Pause"
        else:
            mbox.showerror('System Error', 'Error determinng if system is playing')

    def onPrevious(self, var):

        self.sonos.previous()

    def onNext(self, var):

        self.sonos.next()

    def onSend(self, val):

        audioUrl = self.entryUri.get()

        if urlExist(audioUrl):
            self.sonos.play_uri(self.entryUri.get())
            track = self.sonos.get_current_track_info()
            self.varSentfile.set(track['title'])
            self.sonos.pause()
        else:
            mbox.showerror("URI Error","URI does not exist!" )

        self.entryUri.delete(0, END)


    def onSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)

        self.varLb.set(value)

import urllib2

def urlExist(url):
    request = urllib2.Request(url)
    request.get_method = lambda : 'HEAD'
    try:
        response = urllib2.urlopen(request)
        return True
    except:
        return False

def main():

    root = Tk()
    ex = Example(root)
    root.geometry("900x350+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()