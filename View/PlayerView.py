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
import webbrowser
from selenium import webdriver

from Lib import Tools

class GUI :

	def __init__ (self, master) :
		self.master = master
		self.authDownload = ''
		self.watchLinkStat = {'err': 0, 'msg': ''}
		self.downLinkStat = {'err': 0, 'msg': ''}
		self.Tools = Tools.Tools()

	def showDlLink (self, link) :
		window = Tkinter.Toplevel()
		window.title('下载链接')
		window.resizable(width = 'false', height = 'false')
		if self.Tools.isWin() :
			window.iconbitmap(self.Tools.getRes('biticon.ico'))

		topZone = Tkinter.Frame(window, bd = 0, bg="#444")
		topZone.pack(expand = True, fill = 'both')

		textZone = Tkinter.Text(topZone, height = 8, width = 50, bd = 10, bg="#444", fg = '#ddd', highlightthickness = 0, selectbackground = '#116cd6')
		textZone.grid(row = 0, column = 0, sticky = '')
		textZone.insert('insert', link)

		dlBtn = Tkinter.Button(topZone, text = '下载', width = 10, fg = '#222', highlightbackground = '#444', command =  lambda url = link : webbrowser.open_new(url))
		dlBtn.grid(row = 1, column = 0, pady = 5)

	def showWatchLink (self) :
		if self.watchLinkStat['err'] == 0 :
			if self.watchLinkStat['msg'] == '' :
				self.timer = self.master.after(50, self.showWatchLink)
			else :
				webbrowser.open_new(self.watchLinkStat['msg'])
		elif self.watchLinkStat['err'] == 1 :
			tkMessageBox.showinfo('Error', '云端未能完成该任务，请等待云端下载完成or换个资源试试！')
		elif self.watchLinkStat['err'] == 2 :
			tkMessageBox.showinfo('Notice', '磁力链接目前不支持在线观看，待后续版本更新。\r\n暂时请手动下载或上传链接至百度云！')
		elif self.watchLinkStat['err'] == 3 :
			self.showAuthCode(self.watchLinkStat['msg'])

	def showCloudLink (self) :
		if self.downLinkStat['err'] == 0 :
			if self.downLinkStat['msg'] == '' :
				self.timer = self.master.after(50, self.showCloudLink)
			else :
				window = Tkinter.Toplevel()
				window.title('离线下载链接')
				window.resizable(width = 'false', height = 'false')
				if self.Tools.isWin() :
					window.iconbitmap(self.Tools.getRes('biticon.ico'))

				topZone = Tkinter.Frame(window, bd = 0, bg="#444")
				topZone.pack(expand = True, fill = 'both')

				textZone = Tkinter.Text(topZone, height = 8, width = 50, bd = 10, bg="#444", fg = '#ddd', highlightthickness = 0, selectbackground = '#116cd6')
				textZone.grid(row = 0, column = 0, sticky = '')
				textZone.insert('insert', self.downLinkStat['msg'])

				dlBtn = Tkinter.Button(topZone, text = '下载', width = 10, fg = '#222', highlightbackground = '#444', command =  lambda url = self.downLinkStat['msg'] : webbrowser.open_new(url))
				dlBtn.grid(row = 1, column = 0, pady = 5)

		elif self.downLinkStat['err'] == 1 :
			tkMessageBox.showinfo('Error', '云端未能完成该任务，请等待云端下载完成or换个资源试试！')
		elif self.downLinkStat['err'] == 2 :
			tkMessageBox.showinfo('Notice', '磁力链接目前不支持离线下载，待后续版本更新。\r\n暂时请手动下载或上传链接至百度云！')
		elif self.downLinkStat['err'] == 3 :
			self.showAuthCode(self.downLinkStat['msg'])

	def showAuthCode (self, imgUrl) : 
		self.authWindow = Tkinter.Toplevel()
		self.authWindow.title('验证码')
		self.authWindow.resizable(width = 'false', height = 'false')
		if self.Tools.isWin() :
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
		if self.Tools.isWin() :
			chromeDriver = self.Tools.getRes('chromedriver.exe')
		else :
			chromeDriver = self.Tools.getRes('chromedriver')

		# try:
		self.browser = webdriver.Chrome(executable_path = chromeDriver)
		self.browser.get(loginUrl)

		self.browser.maximize_window() 

		self.slave = Tkinter.Toplevel()
		self.slave.title('Login')
		self.slave.resizable(width = 'false', height = 'false')
		if self.Tools.isWin() :
			self.slave.iconbitmap(self.Tools.getRes('biticon.ico'))

		mainFrame = Tkinter.Frame(self.slave, bd = 0, bg="#444")
		mainFrame.pack(expand = True, fill = 'both', ipadx = '10')

		msgLabel = Tkinter.Label(mainFrame, text="请于页面中登陆百度云账号\r\n登陆成功后点击下方「获取cookies」按钮", fg = '#ddd', bg="#444", anchor = 'center')
		msgLabel.grid(row = 0, column = 1, pady = 5)

		loginBtn = Tkinter.Button(mainFrame, text = '获取cookies', width = 20, fg = '#222', highlightbackground = '#444', command = lambda cb = callback : self.__getLoginInput(cb))
		loginBtn.grid(row = 4, column = 1, pady = 5)

		mainFrame.grid_columnconfigure(0, weight=1)
		mainFrame.grid_columnconfigure(2, weight=1)
		# except Exception as e:
		# 	tkMessageBox.showinfo('Notice', '为保障密码安全：登陆功能将完全在Chrome浏览器中进行。\r\n所以需要Chrome支持。\r\n请先安装Google Chrome浏览器。')

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
			self.slave.destroy()
			tkMessageBox.showinfo('Success', '登陆成功')
			callback(cookieStr)
		else :
			tkMessageBox.showinfo('Error', result['msg'])

	def __getAuthInput (self) :
		authKey = self.authKeyInput.get()
		self.authDownload(authKey)
		self.authWindow.destroy()		

