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
import time
import soco as sonosLib

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.lstSonos = list(sonosLib.discover())
        self.sonos = self.lstSonos[0]

        self.counter = 0
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
        self.btnMute.bind('<Button-1>', self.onMute)

        self.volume = Scale(frame0, from_=0, to=100, orient=HORIZONTAL, showvalue=0)
        self.volume.pack(side=LEFT, padx=2)
        self.volume.bind('<ButtonRelease>', self.onSlide)

        btnStop = Button(frame0, text="Stop", width=4)
        btnStop.pack(side=LEFT, padx=2)
        btnStop.bind('<Button-1>', self.onStop)

        self.btnPrev = Button(frame0, text="<< Prev", width=6)
        self.btnPrev.pack(side=LEFT, padx=(125,2))
        self.btnPrev.bind('<Button-1>', self.onPrevious)

        self.btnPlayPause = Button(frame0, text="?????", width=5)
        self.btnPlayPause.pack(side=LEFT, padx=2)
        self.btnPlayPause.bind('<Button-1>', self.onPlayPause)

        self.btnNext = Button(frame0, text="Next >>", width=6)
        self.btnNext.pack(side=LEFT, padx=2)
        self.btnNext.bind('<Button-1>', self.onNext)


        self.btnStatusLight = Button(frame0, text="Led Off", width=6)
        self.btnStatusLight.pack(side=RIGHT, padx=2)
        self.btnStatusLight.bind('<Button-1>', self.onStatusLight)

        self.lstSonosPlayerName = []
        for i in self.lstSonos:
            self.lstSonosPlayerName.append(i.player_name)
        self.varSonosPlayerName = StringVar()
        self.varSonosPlayerName.set(self.sonos.player_name)
        self.dropSonosPlayerName = OptionMenu(frame0,self.varSonosPlayerName,*self.lstSonosPlayerName, command=self.onDropSonos)
        self.dropSonosPlayerName.config(width=14)
        self.dropSonosPlayerName.pack(side=RIGHT, padx=6)

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

        frameMsg = Frame(self)
        frameMsg.pack(fill=BOTH)

        self.lblStatus = Label(frameMsg, text="")
        self.lblStatus.pack(side=LEFT, padx=2, pady=2)

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

    def onStatusLight(self, var):

        self.sonos.status_light = not self.sonos.status_light
        self.myStatusLight('refresh')

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


    def onStop(self, var):

        self.myPlayPause('stop')

    def onPlayPause(self, val):

        varCTS = self.myPlayPause('refresh')
        if varCTS=='PLAYING':
            self.myPlayPause('pause')
        elif varCTS=='PAUSED_PLAYBACK':
            self.myPlayPause('play')
        elif varCTS=='STOPPED':
            self.myPlayPause('play')

        self.myPlayPause('refresh')

    def myPlayPause(self, var):

        if var == 'play':
            self.sonos.play()
        elif var == 'pause':
            self.sonos.pause()
        elif var == 'stop':
            self.sonos.stop()

        timeUntil = time.time() + 10
        varCTS = self.sonos.get_current_transport_info()['current_transport_state']
        while varCTS == 'TRANSITIONING' or varCTS == 'UNKNOWN':
            self.lblStatus['text'] = varCTS + '.'
            time.sleep(0.1)
            varCTS = self.sonos.get_current_transport_info()['current_transport_state']
            if timeUntil < time.time():
                varCTS = 'TIMEOUT'
                break

        if varCTS=='TIMEOUT':
            self.btnPlayPause['text'] = '?????'
        elif varCTS=='PLAYING':
            self.btnPlayPause['text'] = 'Pause'
        elif varCTS=='PAUSED_PLAYBACK':
            self.btnPlayPause['text'] = 'Play'
        elif varCTS=='STOPPED':
            self.btnPlayPause['text'] = 'Play'

        self.lblStatus['text'] = varCTS

        return varCTS

    def myVolume(self, var):

        if var == 'refresh':
            self.volume.set(self.sonos.volume)

    def myStatusLight(self, var):

        if var == 'refresh':
            self.btnStatusLight['text'] = 'LED Off' if self.sonos.status_light else 'LED On'

    def myMute(self, var):

        if var == 'refresh':
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

        self.myTrackInfo('refresh')
        self.myVolume('refresh')
        self.myMute('refresh')
        self.myStatusLight('refresh')
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