#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter
import urllib2
import ssl
import io
import PIL.Image
import PIL.ImageTk
import tkMessageBox
import time
from selenium import webdriver

from Lib import Tools

class GUI :

	def __init__ (self) :
		self.authDownload = ''
		self.Tools = Tools.Tools()

	def showDlLink (self, link) :
		window = Tkinter.Toplevel()
		window.title('下载链接')
		window.resizable(width = 'false', height = 'false')
		window.iconbitmap(self.Tools.getRes('biticon.ico'))

		topZone = Tkinter.Frame(window, bd = 0, bg="#444")
		topZone.pack(expand = True, fill = 'both')

		textZone = Tkinter.Text(topZone, height = 8, width = 50, bd = 10, bg="#444", fg = '#ddd', highlightthickness = 0)
		textZone.grid(row = 0, column = 0, sticky = '')
		textZone.insert('insert', link)

	def showAuthCode (self, imgUrl) : 
		self.authWindow = Tkinter.Toplevel()
		self.authWindow.title('验证码')
		self.authWindow.resizable(width = 'false', height = 'false')
		self.authWindow.iconbitmap(self.Tools.getRes('biticon.ico'))
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
		loginUrl = 'https://pan.baidu.com/'
		chromeDriver = self.Tools.getRes('chromedriver')

		try:
			self.browser = webdriver.Chrome(executable_path = chromeDriver)
			self.browser.get(loginUrl)

			self.browser.maximize_window() 

			self.slave = Tkinter.Toplevel()
			self.slave.title('Login')
			self.slave.resizable(width = 'false', height = 'false')
			self.slave.iconbitmap(self.Tools.getRes('biticon.ico'))

			mainFrame = Tkinter.Frame(self.slave, bd = 0, bg="#444")
			mainFrame.pack(expand = True, fill = 'both', ipadx = '10')

			msgLabel = Tkinter.Label(mainFrame, text="请于页面中登陆百度云账号\r\n登陆成功后点击下方「获取cookies」按钮", fg = '#ddd', bg="#444", anchor = 'center')
			msgLabel.grid(row = 0, column = 1, pady = 5)

			loginBtn = Tkinter.Button(mainFrame, text = '获取cookies', width = 20, fg = '#222', highlightbackground = '#444', command = lambda cb = callback : self.__getLoginInput(cb))
			loginBtn.grid(row = 4, column = 1, pady = 5)

			mainFrame.grid_columnconfigure(0, weight=1)
			mainFrame.grid_columnconfigure(2, weight=1)
		except Exception as e:
			tkMessageBox.showinfo('Notice', '以示清白：登陆功能需Chrome支持。\r\n请先安装Google Chrome浏览器。')

	def __getLoginInput (self, callback = '') :
		time.sleep(5)

		if self.browser.title == u'百度网盘-全部文件' :
			cookies =  self.browser.get_cookies()
			cookieStr = ''
			for x in cookies :
				cookieStr += x['name'] + '=' + x['value'] + '; '

			result = {'stat': 1, 'msg': '获取成功'}
		else :
			result = {'stat': 2, 'msg': '获取失败'}

		self.browser.quit()

		if result['stat'] == 1 :
			self.slave.withdraw()
			tkMessageBox.showinfo('Success', '登陆成功')
			callback(cookieStr)
		else :
			tkMessageBox.showinfo('Error', result['msg'])

	def __getAuthInput (self) :
		authKey = self.authKeyInput.get()
		self.authDownload(authKey)
		self.authWindow.withdraw()		

