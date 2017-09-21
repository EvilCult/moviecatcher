#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter
import tkMessageBox

from Da import BdApi
from Lib import Tools
import PlayerView

class GUI :

	def __init__ (self) :
		self.winTitle = 'Config'
		self.Tools = Tools.Tools()
		self.save = ''

	def show (self, data) :
		self.slave = Tkinter.Toplevel()
		self.slave.title(self.winTitle)
		self.slave.resizable(width = 'false', height = 'false')
		if self.Tools.isWin() :
			self.slave.iconbitmap(self.Tools.getRes('biticon.ico'))

		mainFrame = Tkinter.Frame(self.slave, bd = 0, bg="#444")
		mainFrame.pack(expand = True, fill = 'both', ipadx = '10')

		pathLabel = Tkinter.Label(mainFrame, text="网盘存放路径", fg = '#ddd', bg="#444", anchor = 'center')
		pathLabel.grid(row = 0, column = 1, pady = 5)

		self.path = Tkinter.Entry(mainFrame, width = 25, bd = 0, bg = "#222", fg = "#ddd", highlightthickness = 1, highlightcolor="#111", highlightbackground = '#111', selectbackground = '#116cd6', justify='center')
		self.path.grid(row = 1, column = 1, pady = 5)
		self.path.insert('end', data['path'])

		updateTimelabel = Tkinter.Label(mainFrame, text="自动检测更新", fg = '#ddd', bg="#444", anchor = 'center')
		updateTimelabel.grid(row = 2, column = 1)

		utFrame = Tkinter.Frame(mainFrame, bd = 0, bg="#444")
		utFrame.grid(row = 3, column = 1, pady = 5)

		self.chkUpdateTime = Tkinter.IntVar()
		self.chkUpdateTime.set(int(data['udrate']))
		r1 = Tkinter.Radiobutton(utFrame, text="每天", fg = '#ddd', bg="#444", variable=self.chkUpdateTime, value=1)
		r1.grid(row = 0, column = 0, sticky = 'e')
		r2 = Tkinter.Radiobutton(utFrame, text="每周", fg = '#ddd', bg="#444", variable=self.chkUpdateTime, value=2)
		r2.grid(row = 0, column = 1, sticky = 'e')
		r3 = Tkinter.Radiobutton(utFrame, text="每月", fg = '#ddd', bg="#444", variable=self.chkUpdateTime, value=3)
		r3.grid(row = 0, column = 2, sticky = 'e')

		cfgBtn = Tkinter.Button(mainFrame, text = '保存配置', width = 20, fg = '#222', highlightbackground = '#444', command = self.saveCfg)
		cfgBtn.grid(row = 4, column = 1, pady = 5)

		mainFrame.grid_columnconfigure(0, weight=1)
		mainFrame.grid_columnconfigure(2, weight=1)

	def saveCfg (self) :
		data = {
			'path' : self.path.get(),
			'ariarpc' : '',
			'ariapath' : '',
			'udrate' : self.chkUpdateTime.get()
		}

		result = self.save(data)

		if result['stat'] == 1 :
			self.slave.destroy()
			tkMessageBox.showinfo('Success', '更新成功')
		else :
			tkMessageBox.showinfo('Error', result['msg'])

