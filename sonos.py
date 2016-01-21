#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Sonos-GUI-URI

This is the first attempt to create a window to stream a URI to the Sonos Speakers.

Author: Jim Scherer
"""

from Tkinter import Tk, LEFT, RIGHT, BOTH, RAISED, Listbox, OptionMenu, StringVar, END, X, Scale, HORIZONTAL
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

        self.btnMute = Button(frame0, text="Mute", width=6)
        self.btnMute.pack(side=LEFT, padx=2)
        self.btnMute.bind('<Button-1>', self.myMute)

        self.volume = Scale(frame0, from_=0, to=100, orient=HORIZONTAL, showvalue=0)
        self.myVolume('refresh')
        self.volume.pack(side=LEFT, padx=2)
        self.volume.bind('<ButtonRelease>', self.onSlide)

        btnStop = Button(frame0, text="Stop", width=4)
        btnStop.pack(side=LEFT, padx=2)
        btnStop.bind('<Button-1>', self.onStop)

        btnPrev = Button(frame0, text="<< Prev", width=6)
        btnPrev.pack(side=LEFT, padx=(150,2))
        btnPrev.bind('<Button-1>', self.onPrevious)

        self.btnPlayPause = Button(frame0, text="Play", width=5)
        self.myPlayPause('refresh')
        self.btnPlayPause.pack(side=LEFT, padx=2)
        self.btnPlayPause.bind('<Button-1>', self.myPlayPause)

        btnNext = Button(frame0, text="Next >>", width=6)
        btnNext.pack(side=LEFT, padx=2)
        btnNext.bind('<Button-1>', self.onNext)

        self.lstSonos = sonosLib.discover()
        self.lstSonosPlayerName = []
        for i in self.lstSonos:
            self.lstSonosPlayerName.append(i.player_name)
        self.varSonosPlayerName = StringVar()
        self.varSonosPlayerName.set(self.sonos.player_name)
        self.dropSonosPlayerName = OptionMenu(frame0,self.varSonosPlayerName,*self.lstSonosPlayerName, command=self.onDropSonos)
        self.dropSonosPlayerName.pack()

# Frame
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        self.pack(fill=BOTH, expand=True)

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

    def onDropSonos(self, val):

        pn = self.varSonosPlayerName.get()
        for i in self.lstSonos:
            if i.player_name == pn:
                self.sonos = i
                self.myUIRefresh()
                break

    def onSlide(self, val):

        self.sonos.volume=self.volume.get()

    def onMute(self, var):

        self.sonos.mute = not self.sonos.mute

    def onStop(self, var):

        self.sonos.stop()

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
            self.myPlayPause('pause')
        else:
            mbox.showerror("URI Error","URI does not exist!" )

        self.entryUri.delete(0, END)


    def onSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)

        self.varLb.set(value)

    def myPlayPause(self, var):

        if var == 'refresh':
            pass
        elif var == 'play':
            self.sonos.play()
        elif var == 'pause':
            self.sonos.pause()
        else:  # toggle
            if self.sonos.get_current_transport_info()['current_transport_state']=='PLAYING':
                self.sonos.pause()
            elif self.sonos.get_current_transport_info()['current_transport_state']=='PAUSED_PLAYBACK':
                self.sonos.play()
            elif self.sonos.get_current_transport_info()['current_transport_state']=="STOPPED":
                self.sonos.play()

        self.btnPlayPause['text'] = 'Pause' if self.sonos.get_current_transport_info()['current_transport_state']=='PLAYING' else 'Play'


    def myVolume(self, var):

        if var == 'refresh':
            self.volume.set(self.sonos.volume)

    def myMute(self, var):

        if var == 'refresh':
            pass
        elif var == 'mute':
            self.sonos.mute = True
        elif var == 'unmute':
            self.sonos.mute = False
        else: # toggle
            self.sonos.mute = not self.sonos.mute
        self.btnMute['text'] = 'Unmute' if self.sonos.mute else 'Mute'

    def myUIRefresh(self):

        self.myVolume('refresh')
        self.myMute('refresh')
        self.myPlayPause('refresh')

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