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


# Audio Contols

        frame0 = Frame(self)
        frame0.pack(fill=BOTH)

        self.btnMute = Button(frame0, text="Mute", width=6)
        self.btnMute.pack(side=LEFT, padx=2)
        self.btnMute.bind('<Button-1>', self.myMute)

        self.volume = Scale(frame0, from_=0, to=100, orient=HORIZONTAL, showvalue=0)
        self.volume.pack(side=LEFT, padx=2)
        self.volume.bind('<ButtonRelease>', self.onSlide)

        btnStop = Button(frame0, text="Stop", width=4)
        btnStop.pack(side=LEFT, padx=2)
        btnStop.bind('<Button-1>', self.onStop)

        self.btnPrev = Button(frame0, text="<< Prev", width=6)
        self.btnPrev.pack(side=LEFT, padx=(150,2))
        self.btnPrev.bind('<Button-1>', self.onPrevious)

        self.btnPlayPause = Button(frame0, text="Play", width=5)
        self.btnPlayPause.pack(side=LEFT, padx=2)
        self.btnPlayPause.bind('<Button-1>', self.myPlayPause)

        self.btnNext = Button(frame0, text="Next >>", width=6)
        self.btnNext.pack(side=LEFT, padx=2)
        self.btnNext.bind('<Button-1>', self.onNext)

        self.lstSonos = sonosLib.discover()
        self.lstSonosPlayerName = []
        for i in self.lstSonos:
            self.lstSonosPlayerName.append(i.player_name)
        self.varSonosPlayerName = StringVar()
        self.varSonosPlayerName.set(self.sonos.player_name)
        self.dropSonosPlayerName = OptionMenu(frame0,self.varSonosPlayerName,*self.lstSonosPlayerName, command=self.onDropSonos)
        self.dropSonosPlayerName.pack()

# Audio Track Info

        frameTrack = Frame(self)
        frameTrack.pack(fill=BOTH, pady=(10,3))

        self.lblTrack = Label(frameTrack, text="Track")
        self.lblTrack.pack(side=LEFT)

        frameArtist = Frame(self)
        frameArtist.pack(fill=BOTH, pady=3)

        self.lblArtist = Label(frameArtist, text="Artist")
        self.lblArtist.pack(side=LEFT, padx=2, pady=2)

        frameAlbum = Frame(self)
        frameAlbum.pack(fill=BOTH, pady=3)

        self.lblAlbum = Label(frameAlbum, text="Album")
        self.lblAlbum.pack(side=LEFT, padx=2, pady=2)

# Frame
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        self.pack(fill=BOTH, expand=True)

# Uri
        self.btnZenCast = Button(frame, text="ZenCast")
        self.btnZenCast.pack(side=LEFT, padx=2)
        self.btnZenCast.bind('<Button-1>', self.onZenCast)

        self.lblUri = Label(frame, text="URI")
        self.lblUri.pack(side=LEFT, padx=2, pady=2)

        self.entryUri = Entry(frame)
        self.entryUri.pack(side=LEFT, padx=2, fill=X, expand=True)

        self.btnSend = Button(frame, text="Send")
        self.btnSend.pack(side=RIGHT, padx=2)
        self.btnSend.bind('<Button-1>', self.onSend)

        self.myUIRefresh()
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

        try:
            self.sonos.previous()
            self.myTrackInfo('refresh')
        except sonosLib.exceptions.SoCoException:
            self.btnPrev['state'] = 'disabled'
#            mbox.showerror('Sonos Previous','You are on the first track')

    def onNext(self, var):

        try:
            self.sonos.next()
            self.myTrackInfo('refresh')
        except sonosLib.exceptions.SoCoException:
            self.btnNext['state'] = 'disabled'

#            mbox.showerror('Sonos Next','You are on the last track')

    def onZenCast(self, val):

        audioUrl = 'http://traffic.libsyn.com/amberstar/Zencast' + self.entryUri.get() + '.mp3'
        self.entryUri.delete(0, END)
        self.entryUri.insert(0, audioUrl)
        self.onSend(audioUrl)

    def onSend(self, val):

        audioUrl = self.entryUri.get()

        if urlExist(audioUrl):
            self.sonos.play_uri(audioUrl)
            self.myTrackInfo('refresh')
            self.myPlayPause('pause')
            self.entryUri.delete(0, END)
        else:
            mbox.showerror('URI Error','URI '+ audioUrl + ' does not exist!' )


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

    def myTrackInfo(self, var):

        track = self.sonos.get_current_track_info()
        if var == 'refresh':
            self.lblTrack['text'] = 'Track: ' + track['title']
            self.lblArtist['text'] = 'Artist: ' + track['artist']
            self.lblAlbum['text'] = 'Album: ' + track['album']

        self.btnNext['state'] = 'normal'
        self.btnPrev['state'] = 'normal'

    def myUIRefresh(self):

        self.myVolume('refresh')
        self.myMute('refresh')
        self.myPlayPause('refresh')
        self.myTrackInfo('refresh')

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