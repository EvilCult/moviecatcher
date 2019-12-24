#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter
import tkinter.messagebox

from Bl import Play
from Lib import Tools

class GUI :

	def __init__ (self, master) :
		self.master = master
		self.Tools = Tools.Tools()
		self.listRst = ''
		self.resRst = ''
		self.getDetail = ''

	def showList (self, searchKey) :
		rstWindow = tkinter.Toplevel()
		rstWindow.title('资源列表')
		rstWindow.resizable(width = 'false', height = 'false')
		if self.Tools.isWin() :
			rstWindow.iconbitmap(self.Tools.getRes('biticon.ico'))
		
		titleFrame = tkinter.Frame(rstWindow, bd = 0, bg="#444")
		titleFrame.pack(expand = True, fill = 'both')

		titleLabel = tkinter.Label(titleFrame, text = '关键词 :「 ' + searchKey + ' 」的搜索结果', fg = '#ddd', bg="#444", font = ("Helvetica", "12"))
		titleLabel.grid(row = 1, column = 1, pady = 10)

		titleFrame.grid_columnconfigure(0, weight=1)
		titleFrame.grid_columnconfigure(2, weight=1)

		self.frame = tkinter.Frame(rstWindow, bd = 0, bg="#222")
		self.frame.pack(expand = True, fill = 'both')

		self.window = tkinter.Listbox(self.frame, height = 14, width = 40, bd = 0, bg="#222", fg = '#ddd', selectbackground = '#116cd6', highlightthickness = 0)
		self.window.grid(row = 0, column = 0, padx = 10, pady = 10)
		self.window.bind('<Double-Button-1>', self.__getMovDetails)

		try : 
			self.window.delete(0, 100)
		except : 
			pass

	def updateList (self) :
		if self.listRst != '' :
			idx = 0
			for x in self.listRst :
				self.window.insert(idx, x['title'])
				idx += 1
		else :
			self.timer = self.frame.after(50, self.updateList)

	def showRes (self) :
		self.resWindow = tkinter.Toplevel()
		self.resWindow.title(self.target['title'])
		self.resWindow.resizable(width = 'false', height = 'false')
		if self.Tools.isWin() :
			self.resWindow.iconbitmap(self.Tools.getRes('biticon.ico'))
		self.resWindow.config(background='#444')

		self.resFrame = tkinter.Frame(self.resWindow, bd = 0, bg="#444")
		self.resFrame.grid(row = 0, column = 0, sticky = '')

		btnZone = tkinter.Frame(self.resWindow, bd = 10, bg="#444")
		btnZone.grid(row = 1, column = 0, sticky = '')

		self.resList = tkinter.Listbox(self.resFrame, height = 8, width = 50, bd = 0, bg="#222", fg = '#ddd',selectbackground = '#116cd6', highlightthickness = 0)
		self.resList.grid(row = 0, sticky = '')

		viewBtn = tkinter.Button(btnZone, text = '查看连接', width = 10, fg = '#222', highlightbackground = '#444', command = self.__taskShow)
		viewBtn.grid(row = 0, column = 0, padx = 5)

		watchBtn = tkinter.Button(btnZone, text = '在线观看', width = 10, fg = '#222', highlightbackground = '#444', command = self.__taskWatch)
		watchBtn.grid(row = 0, column = 1, padx = 5)

		dlBtn = tkinter.Button(btnZone, text = '离线下载', width = 10, fg = '#222', highlightbackground = '#444', command = self.__taskDownload)
		dlBtn.grid(row = 0, column = 2, padx = 5)

	def updateRes (self) :
		if self.resRst != '' :
			if len(self.resRst) > 0:
				idx = 0
				for x in self.resRst :
					self.resList.insert(idx, x[0])
					idx += 1
			else :
				self.resList.insert(0, '该资源已被和谐，暂时无法播放。')
		else :
			self.timer = self.resFrame.after(50, self.updateRes)

	def __getMovDetails (self, event) : 
		idx = int(self.window.curselection()[0])

		self.target = self.listRst[idx]

		self.getDetail(self.target)

	def __getChoose (self) :
		if self.resList.curselection() == () :
			tkinter.messagebox.showinfo('Notice', '请选择一个文件进行操作！')
		else :
			idx = int(self.resList.curselection()[0])

			target = self.resRst[idx]

	def __taskWatch (self) :
		if self.resList.curselection() == () :
			tkinter.messagebox.showinfo('提示', '请选择一个文件进行操作！')
		else :
			idx = int(self.resList.curselection()[0])

			target = self.resRst[idx]

			Player = Play.Play(self.master)
			Player.watchLink(target)

	def __taskShow (self) :
		if self.resList.curselection() == () :
			tkinter.messagebox.showinfo('提示', '请选择一个文件进行操作！')
		else :
			idx = int(self.resList.curselection()[0])

			target = self.resRst[idx]

			Player = Play.Play(self.master)
			Player.showLink(target)

	def __taskDownload (self) :
		if self.resList.curselection() == () :
			tkinter.messagebox.showinfo('提示', '请选择一个文件进行操作！')
		else :
			idx = int(self.resList.curselection()[0])

			target = self.resRst[idx]

			Player = Play.Play(self.master)
			Player.dlLink(target)
