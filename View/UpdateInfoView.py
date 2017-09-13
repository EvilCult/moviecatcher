#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter
import webbrowser

from Lib import Tools
from Da import AppBase

class GUI :

	def __init__ (self) :
		self.winTitle = 'Update'
		self.Tools = Tools.Tools()
		self.app = AppBase.info

	def show (self, info) :
		self.slave = Tkinter.Toplevel()
		self.slave.title(self.winTitle)
		self.slave.resizable(width = 'false', height = 'false')
		self.slave.geometry('300x220+200+200')

		frame = Tkinter.Frame(self.slave, bd = 0, bg="#444")
		frame.pack(expand = True, fill = 'both')

		titleLabel = Tkinter.Label(frame, text = self.app['title'], fg = '#ddd', bg="#444", font = ("Helvetica", "16", 'bold'), anchor = 'center')
		titleLabel.grid(row = 0, column = 1, pady = 5)

		if info['version'] != '' :
			version = str(info['version'])
		else :
			version = str(self.app['ver']) + ' Build (' + str(self.app['build']) + ')'
		verlabel = Tkinter.Label(frame, text = 'Version : ' + version, fg = '#ddd', bg="#444", font = ("Helvetica", "10"), anchor = 'center')
		verlabel.grid(row = 1, column = 1)

		information = Tkinter.Text(frame, height = 8, width = 35, bd = 0, fg = '#ddd', bg="#222", highlightthickness = 1, highlightcolor="#111", highlightbackground = '#111', selectbackground = '#116cd6', font = ("Helvetica", "12"))
		information.grid(row = 3, column = 1, pady = 10)
		information.insert('end', info['msg'])

		btn = Tkinter.Button(frame, text = 'Download', width = 10, fg = '#222', highlightbackground = '#444', command = lambda target = info['dUrl'] : webbrowser.open_new(target))
		btn.grid(row = 4, column = 1)

		frame.grid_columnconfigure(0, weight=1)
		frame.grid_columnconfigure(2, weight=1)


