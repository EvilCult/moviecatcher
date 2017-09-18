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
		self.udInfo = []

	def show (self) :
		self.slave = Tkinter.Toplevel()
		self.slave.title(self.winTitle)
		self.slave.resizable(width = 'false', height = 'false')
		self.slave.iconbitmap(self.Tools.getRes('biticon.ico'))

		self.frame = Tkinter.Frame(self.slave, bd = 0, bg="#444")
		self.frame.pack(expand = True, fill = 'both', ipadx = '5', ipady = '5')

		titleLabel = Tkinter.Label(self.frame, text = self.app['title'], fg = '#ddd', bg="#444", font = ("Helvetica", "16", 'bold'), anchor = 'center')
		titleLabel.grid(row = 0, column = 1, pady = 5)

		version = str(self.app['ver']) + ' Build (' + str(self.app['build']) + ')'
		verlabel = Tkinter.Label(self.frame, text = 'Version : ' + version, fg = '#ddd', bg="#444", font = ("Helvetica", "10"), anchor = 'center')
		verlabel.grid(row = 1, column = 1)

		self.information = Tkinter.Text(self.frame, height = 8, width = 35, bd = 0, fg = '#ddd', bg="#222", highlightthickness = 1, highlightcolor="#111", highlightbackground = '#111', selectbackground = '#116cd6', font = ("Helvetica", "12"))
		self.information.grid(row = 2, column = 1, pady = 10)
		self.information.insert('end', '更新检测中。。。')

		self.frame.grid_columnconfigure(0, weight=1)
		self.frame.grid_columnconfigure(2, weight=1)

	def updateInfo (self) :
		if self.udInfo != [] :
			if self.udInfo['version'] != '' :
				version = str(self.udInfo['version'])
			else :
				version = str(self.app['ver']) + ' Build (' + str(self.app['build']) + ')'
			verlabel = Tkinter.Label(self.frame, text = 'Version : ' + version, fg = '#ddd', bg="#444", font = ("Helvetica", "10"), anchor = 'center')
			verlabel.grid(row = 1, column = 1)

			self.information = Tkinter.Text(self.frame, height = 8, width = 35, bd = 0, fg = '#ddd', bg="#222", highlightthickness = 1, highlightcolor="#111", highlightbackground = '#111', selectbackground = '#116cd6', font = ("Helvetica", "12"))
			self.information.grid(row = 2, column = 1, pady = 10)
			self.information.delete('0.0', 'end')
			self.information.insert('end', self.udInfo['msg'])

			btn = Tkinter.Button(self.frame, text = 'Download', width = 10, fg = '#222', highlightbackground = '#444', command = lambda target = self.udInfo['dUrl'] : webbrowser.open_new(target))
			btn.grid(row = 3, column = 1)
		else :
			self.timer = self.frame.after(50, self.updateInfo)

	def close (self) :
		self.slave.withdraw()

