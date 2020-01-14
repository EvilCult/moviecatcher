#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter
import tkinter.messagebox

from Da import BdApi
from Lib import Tools
from . import PlayerView

class GUI :

	def __init__ (self) :
		self.winTitle = 'Config'
		self.Tools = Tools.Tools()
		self.save = ''

	def show (self, data) :
		self.slave = tkinter.Toplevel()
		self.slave.title(self.winTitle)
		self.slave.resizable(width = 'false', height = 'false')
		if self.Tools.isWin() :
			self.slave.iconbitmap(self.Tools.getRes('biticon.ico'))

		mainFrame = tkinter.Frame(self.slave, bd = 0, bg="#444")
		mainFrame.pack(expand = True, fill = 'both', ipadx = '10')

		pathLabel = tkinter.Label(mainFrame, text="网盘存放路径", fg = '#ddd', bg="#444", anchor = 'center')
		pathLabel.grid(row = 0, column = 1, pady = 5)

		self.path = tkinter.Entry(mainFrame, width = 25, bd = 0, bg = "#222", fg = "#ddd", highlightthickness = 1, highlightcolor="#111", highlightbackground = '#111', selectbackground = '#116cd6', justify='center')
		self.path.grid(row = 1, column = 1, pady = 5)
		self.path.insert('end', data['path'])

		updateTimelabel = tkinter.Label(mainFrame, text="自动检测更新", fg = '#ddd', bg="#444", anchor = 'center')
		updateTimelabel.grid(row = 2, column = 1)

		utFrame = tkinter.Frame(mainFrame, bd = 0, bg="#444")
		utFrame.grid(row = 3, column = 1, pady = 5)

		self.chkUpdateTime = tkinter.IntVar()
		self.chkUpdateTime.set(int(data['udrate']))
		r1 = tkinter.Radiobutton(utFrame, text="每天", fg = '#ddd', bg="#444", variable=self.chkUpdateTime, value=1)
		r1.grid(row = 0, column = 0, sticky = 'e')
		r2 = tkinter.Radiobutton(utFrame, text="每周", fg = '#ddd', bg="#444", variable=self.chkUpdateTime, value=2)
		r2.grid(row = 0, column = 1, sticky = 'e')
		r3 = tkinter.Radiobutton(utFrame, text="每月", fg = '#ddd', bg="#444", variable=self.chkUpdateTime, value=3)
		r3.grid(row = 0, column = 2, sticky = 'e')

		cfgBtn = tkinter.Button(mainFrame, text = '保存配置', width = 20, fg = '#222', highlightbackground = '#444', command = self.saveCfg)
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
			tkinter.messagebox.showinfo('Success', '更新成功')
		else :
			tkinter.messagebox.showinfo('Error', result['msg'])

