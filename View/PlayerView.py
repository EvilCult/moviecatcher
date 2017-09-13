#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter
import urllib2
import ssl
import io
import PIL.Image
import PIL.ImageTk
import tkMessageBox

class GUI :

	def __init__ (self) :
		self.authDownload = ''

	def showDlLink (self, link) :
		window = Tkinter.Toplevel()
		window.title('下载链接')
		window.resizable(width = 'false', height = 'false')

		topZone = Tkinter.Frame(window, bd = 0, bg="#444")
		topZone.pack(expand = True, fill = 'both')

		textZone = Tkinter.Text(topZone, height = 8, width = 50, bd = 10, bg="#444", fg = '#ddd', highlightthickness = 0)
		textZone.grid(row = 0, column = 0, sticky = '')
		textZone.insert('insert', link)

	def showAuthCode (self, imgUrl) : 
		self.authWindow = Tkinter.Toplevel()
		self.authWindow.title('验证码')
		self.authWindow.resizable(width = 'false', height = 'false')
		self.authWindow.config(background='#444')

		winTop = Tkinter.Frame(self.authWindow, bd = 10, bg = '#444')
		winTop.grid(row = 0, column = 0, sticky = '')

		ctx = ssl.create_default_context()
		ctx.check_hostname = False
		ctx.verify_mode = ssl.CERT_NONE
		image = urllib2.urlopen(imgUrl, context = ctx).read()
		imgData = io.BytesIO(image)
		pilImage = PIL.Image.open(imgData)
		tkImg = PIL.ImageTk.PhotoImage(pilImage)

		label = Tkinter.Label(winTop, image = tkImg, bd = 0, bg = '#111', relief = 'solid')
		label.img = tkImg
		label.grid(row = 0, column = 0, sticky = '', pady = 5)

		self.authKeyInput = Tkinter.Entry(winTop, width = 20, bd = 0, bg = "#222", fg = "#ddd", highlightthickness = 1, highlightcolor="#111", highlightbackground = '#111', justify='center')
		self.authKeyInput.grid(row = 1, column = 0, pady = 5)
		self.authKeyInput.insert('end', '')

		btn = Tkinter.Button(winTop, text = '确认', width = 10, fg = '#222', highlightbackground = '#444', command = self.__getAuthInput)
		btn.grid(row = 2, column = 0, pady = 5)

	def showLoginWindow (self, callback = '') :
		self.slave = Tkinter.Toplevel()
		self.slave.title('Login')
		self.slave.resizable(width = 'false', height = 'false')
		self.slave.geometry('250x150+200+200')

		mainFrame = Tkinter.Frame(self.slave, bd = 0, bg="#444")
		mainFrame.pack(expand = True, fill = 'both')

		unameLabel = Tkinter.Label(mainFrame, text="百度用户名", fg = '#ddd', bg="#444", anchor = 'center')
		unameLabel.grid(row = 0, column = 1, pady = 5)

		self.uname = Tkinter.Entry(mainFrame, width = 25, bd = 0, bg = "#222", fg = "#ddd", highlightthickness = 1, highlightcolor="#111", highlightbackground = '#111', selectbackground = '#116cd6', justify='center')
		self.uname.grid(row = 1, column = 1, pady = 5)

		pwdlabel = Tkinter.Label(mainFrame, text="密码", fg = '#ddd', bg="#444", anchor = 'center')
		pwdlabel.grid(row = 2, column = 1)

		self.pwd = Tkinter.Entry(mainFrame, width = 25, bd = 0, bg = "#222", fg = "#ddd", highlightthickness = 1, highlightcolor="#111", highlightbackground = '#111', selectbackground = '#116cd6', show="*", justify='center')
		self.pwd.grid(row = 3, column = 1, pady = 5)

		cfgBtn = Tkinter.Button(mainFrame, text = '登陆', width = 20, fg = '#222', highlightbackground = '#444', command = lambda cb = callback : self.__getLoginInput(cb))
		cfgBtn.grid(row = 4, column = 1, pady = 5)

		mainFrame.grid_columnconfigure(0, weight=1)
		mainFrame.grid_columnconfigure(2, weight=1)

	def __getLoginInput (self, callback = '') :
		loginUname = self.uname.get()
		loginPwd = self.pwd.get()

		data = {'uname': loginUname, 'pwd': loginPwd}

		result = callback(data)

		if result['stat'] == 1 :
			self.slave.withdraw()
			tkMessageBox.showinfo('Success', '登陆成功')
		else :
			tkMessageBox.showinfo('Error', result['msg'])

	def __getAuthInput (self) :
		authKey = self.authKeyInput.get()
		self.authDownload(authKey)
		self.authWindow.withdraw()		

