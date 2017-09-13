#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter
import tkMessageBox

from Bl import Play

class GUI :

	def __init__ (self, master) :
		self.master = master
		self.result = ''
		self.getDetail = ''

	def showList (self, searchKey) :
		rstWindow = Tkinter.Toplevel()
		rstWindow.title('资源列表')
		rstWindow.resizable(width = 'false', height = 'false')

		titleFrame = Tkinter.Frame(rstWindow, bd = 0, bg="#444")
		titleFrame.pack(expand = True, fill = 'both')

		titleLabel = Tkinter.Label(titleFrame, text = '关键词 :「 ' + str(searchKey.encode('utf-8')) + ' 」的搜索结果', fg = '#ddd', bg="#444", font = ("Helvetica", "12"))
		titleLabel.grid(row = 1, column = 1, pady = 10)

		titleFrame.grid_columnconfigure(0, weight=1)
		titleFrame.grid_columnconfigure(2, weight=1)

		self.frame = Tkinter.Frame(rstWindow, bd = 0, bg="#222")
		self.frame.pack(expand = True, fill = 'both')

		self.window = Tkinter.Listbox(self.frame, height = 14, width = 40, bd = 0, bg="#222", fg = '#ddd', selectbackground = '#116cd6', highlightthickness = 0)
		self.window.grid(row = 0, column = 0, padx = 10, pady = 10)
		self.window.bind('<Double-Button-1>', self.__getMovDetails)

		try : 
			self.window.delete(0, 100)
		except : 
			pass

	def update (self) :
		if self.result != '' :
			idx = 0
			for x in self.result :
				self.window.insert(idx, x['title'])
				idx += 1
		else :
			self.timer = self.frame.after(50, self.update)

	def showRes (self, data) :
		self.res = data
		self.resWindow = Tkinter.Toplevel()
		self.resWindow.title(self.target['title'])
		self.resWindow.resizable(width = 'false', height = 'false')
		self.resWindow.config(background='#444')

		topZone = Tkinter.Frame(self.resWindow, bd = 10, bg="#444")
		topZone.grid(row = 0, column = 0, sticky = '')

		btnZone = Tkinter.Frame(self.resWindow, bd = 10, bg="#444")
		btnZone.grid(row = 1, column = 0, sticky = '')

		dHeight = len(self.res)
		if dHeight < 5 :
			dHeight = 5
		elif dHeight > 20 :
			dHeight = 20

		self.resList = Tkinter.Listbox(topZone, height = dHeight, width = 50, bd = 0, bg="#444", fg = '#ddd',selectbackground = '#116cd6', highlightthickness = 0)
		self.resList.grid(row = 0, sticky = '')

		if len(self.res) > 0:
			idx = 0
			for x in self.res :
				self.resList.insert(idx, x[0])
				idx += 1

			viewBtn = Tkinter.Button(btnZone, text = '查看连接', width = 10, fg = '#222', highlightbackground = '#444', command = self.__taskShow)
			viewBtn.grid(row = 0, column = 0, padx = 5)

			watchBtn = Tkinter.Button(btnZone, text = '在线观看', width = 10, fg = '#222', highlightbackground = '#444', command = self.__taskWatch)
			watchBtn.grid(row = 0, column = 1, padx = 5)

			dlBtn = Tkinter.Button(btnZone, text = '离线下载', width = 10, fg = '#222', highlightbackground = '#444', command = self.__taskDownload)
			dlBtn.grid(row = 0, column = 2, padx = 5)
		else :
			self.resList.insert(0, '该资源已被和谐，暂时无法播放。')

	def __getMovDetails (self, event) : 
		idx = int(self.window.curselection()[0])

		self.target = self.result[idx]

		self.getDetail(self.target)

	def __getChoose (self) :
		if self.resList.curselection() == () :
			tkMessageBox.showinfo('Notice', '请选择一个文件进行操作！')
		else :
			idx = int(self.resList.curselection()[0])

			target = self.res[idx]

	def __taskWatch (self) :
		if self.resList.curselection() == () :
			tkMessageBox.showinfo('提示', '请选择一个文件进行操作！')
		else :
			idx = int(self.resList.curselection()[0])

			target = self.res[idx]

			Player = Play.Play(self.master)
			Player.watchLink(target)

	def __taskShow (self) :
		if self.resList.curselection() == () :
			tkMessageBox.showinfo('提示', '请选择一个文件进行操作！')
		else :
			idx = int(self.resList.curselection()[0])

			target = self.res[idx]

			Player = Play.Play(self.master)
			Player.showLink(target)

	def __taskDownload (self) :
		if self.resList.curselection() == () :
			tkMessageBox.showinfo('提示', '请选择一个文件进行操作！')
		else :
			idx = int(self.resList.curselection()[0])

			target = self.res[idx]

			Player = Play.Play(self.master)
			Player.dlLink(target)
