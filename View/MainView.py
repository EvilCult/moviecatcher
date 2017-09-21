#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter

import MenuBarView
from Lib import Tools
from Bl import Search
from Da import AppBase

class GUI :

	def __init__ (self) :
		self.Tools = Tools.Tools()
		self.winTitle = AppBase.info['title']
		self.__mainWindow()

	def __mainWindow (self) :
		self.master = Tkinter.Tk()

		self.master.title(self.winTitle)
		self.master.resizable(width = 'false', height = 'false')
		if self.Tools.isWin() :
			self.master.iconbitmap(self.Tools.getRes('biticon.ico'))

		menuBar = MenuBarView.GUI(self.master)
		menuBar.show()

		self.__topBox()

	def __topBox (self) :
		self.mainTop = Tkinter.Frame(self.master, bd = 0, bg="#444")
		self.mainTop.pack(expand = True, fill = 'both', ipady = 5)

		self.searchKey = Tkinter.Entry(self.mainTop, width = 40, bd = 0, bg = "#222", fg = "#ddd", highlightthickness = 1, highlightcolor="#111", highlightbackground = '#111', selectbackground = '#116cd6', justify='center')
		self.searchKey.grid(row = 0, column = 1, padx = '10', pady = '20')
		self.searchKey.insert('end', '电影名/电视剧名')
		self.searchKey.bind('<FocusIn>', self.__cleanSearchKey)

		Searcher = Search.Search(self.master)
		self.sBtn = Tkinter.Button(self.mainTop, text = '搜索', width = 10, fg = '#222', highlightbackground = '#444', command = lambda key = self.searchKey : Searcher.showResult(key))
		self.sBtn.grid(row = 1, column = 1)

		self.mainTop.grid_columnconfigure(0, weight=1)
		self.mainTop.grid_columnconfigure(2, weight=1)

	def __cleanSearchKey(self, e) : 
		key = self.searchKey.get()

		if key == u'电影名/电视剧名' :
			self.searchKey.delete('0', 'end')

	def run (self) :
		self.master.mainloop()