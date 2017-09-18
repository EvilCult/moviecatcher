#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import webbrowser
import tkMessageBox
import time

from Da import BdApi
from Da import Aria2
from Da import Config
from View import PlayerView

class Play :

	def __init__ (self, master) :
		self.master = master
		self.bdAuth = {}
		self.Cfg = Config.Config()

		cfgInfo = self.Cfg.get()

		self.BD = BdApi.BdApi()

		if cfgInfo['bdc'] == '' :
			self.BDLogin = False
		else :
			self.BDLogin = True

		self.Aria = Aria2.Aria2()
		self.Player = PlayerView.GUI()

	def watchLink (self, target) :
		if self.BDLogin :
			self.downloadUrl = target[1]

			linkType =  self.downloadUrl[0:6]
			if linkType != 'magnet' : 
				threading.Thread(target = self.__bdPlay).start()
			else : 
				tkMessageBox.showinfo('Notice', '磁力链接无法在线观看，请下载或手动上传视频至百度云！')
		else :
			tkMessageBox.showinfo('Error', '本功能需要云支持，请于菜单栏「Edit -> Baidu Login」登录百度云。')

	def dlLink (self, target) :
		ariaStat = self.Aria.chkAria()
		if ariaStat :
			if self.BDLogin :
				self.downloadUrl = target[1]
				self.dlFileName = target[0]

				linkType =  self.downloadUrl[0:6]
				if linkType != 'magnet' :
					threading.Thread(target = self.__bdDownload).start()
				else : 
					self.Aria.download(self.downloadUrl, self.dlFileName);
			else :
				tkMessageBox.showinfo('Error', '本功能需要云支持，请于菜单栏「Edit -> Baidu Login」登录百度云。')
		else :
			tkMessageBox.showinfo('Error', 'Aria2配置不正确，请确认已运行Aria2服务。')

	def showLink (self, target) :
		self.downloadUrl = target[1]
		self.Player.showDlLink(self.downloadUrl)

	def __bdlogin (self) :
		self.Player.showLoginWindow(self.BD.saveLogin)

	def __bdPlay (self) :
		result = self.BD.addTask(self.downloadUrl, self.bdAuth)
		if result['err'] == 0 :
			taskID = result['taskID']
			playUrl = self.BD.getPlayUrl(taskID)
			if playUrl != '' :
				webbrowser.open_new(playUrl)
			else :
				tkMessageBox.showinfo('Error', '云端未能完成该任务，请等待云端下载完成or换个资源试试！')
		else :
			self.bdAuth = {
				'vcode': result['vcode'],
				'input': ''
			}
			self.__authCode(result['img'], 'play')

	def __bdDownload (self) :
		result = self.BD.addTask(self.downloadUrl, self.bdAuth)
		if result['err'] == 0 :
			taskID = result['taskID']
			dlUrl = self.BD.getDlUrl(taskID)
			if dlUrl != '' :
				self.Aria.download(dlUrl, self.dlFileName)
			else :
				tkMessageBox.showinfo('Error', '云端未能完成该任务，请等待云端下载完成or换个资源试试！')
		else :
			self.bdAuth = {
				'vcode': result['vcode'],
				'input': ''
			}
			self.__authCode(result['img'], 'download')

	def __authCode (self, imgUrl, authType) :
		authKey = ''

		if authType == 'play':
			self.Player.authDownload = lambda authKey = authKey : self.__authPlay(authKey)
		else :
			self.Player.authDownload = lambda authKey = authKey : self.__authDownload(authKey)

		self.Player.showAuthCode(imgUrl)

	def __authPlay (self, authKey) :
		self.bdAuth['input'] = authKey

		threading.Thread(target = self.__bdPlay).start()

	def __authDownload (self, authKey) :
		self.bdAuth['input'] = authKey

		threading.Thread(target = self.__bdDownload).start()