#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import webbrowser
import tkMessageBox
import time

from Da import BdApi
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

		self.Player = PlayerView.GUI(self.master)

	def watchLink (self, target) :
		self.Player.watchLinkStat = {'err': 0, 'msg': ''}
		if self.BDLogin :
			self.downloadUrl = target[1]

			self.Player.showWatchLink()
			linkType =  self.downloadUrl[0:6]
			if linkType != 'magnet' : 
				threading.Thread(target = self.__bdPlay).start()
			else : 
				self.Player.watchLinkStat['err'] = 2
		else :
			tkMessageBox.showinfo('Error', '本功能需要云支持，请于菜单栏「Edit -> Baidu Login」登录百度云。')

	def dlLink (self, target) :
		self.Player.downLinkStat = {'err': 0, 'msg': ''}
		if self.BDLogin :
			self.downloadUrl = target[1]
			self.dlFileName = target[0]

			self.Player.showCloudLink()
			linkType =  self.downloadUrl[0:6]
			if linkType != 'magnet' :
				threading.Thread(target = self.__bdDownload).start()
			else : 
				self.Player.downLinkStat['err'] = 2
		else :
			tkMessageBox.showinfo('Error', '本功能需要云支持，请于菜单栏「Edit -> Baidu Login」登录百度云。')

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
				self.Player.watchLinkStat['msg'] = playUrl
			else :
				self.Player.watchLinkStat['err'] = 1
		else :
			self.bdAuth = {
				'vcode': result['vcode'],
				'input': ''
			}
			self.Player.watchLinkStat['err'] = 3
			self.Player.watchLinkStat['msg'] = result['img']
			self.Player.authDownload = lambda authKey = '' : self.__authPlay(authKey)

	def __bdDownload (self) :
		result = self.BD.addTask(self.downloadUrl, self.bdAuth)
		if result['err'] == 0 :
			taskID = result['taskID']
			dlUrl = self.BD.getDlUrl(taskID)
			if dlUrl != '' :
				self.Player.downLinkStat['msg'] = dlUrl
			else :
				self.Player.downLinkStat['err'] = 1
		else :
			self.bdAuth = {
				'vcode': result['vcode'],
				'input': ''
			}
			self.Player.downLinkStat['err'] = 3
			self.Player.downLinkStat['msg'] = result['img']
			self.Player.authDownload = lambda authKey = '' : self.__authDownload(authKey)

	def __authCode (self, imgUrl, authType) :
		authKey = ''

		if authType == 'play':
			self.Player.authDownload = lambda authKey = authKey : self.__authPlay(authKey)
		else :
			self.Player.authDownload = lambda authKey = authKey : self.__authDownload(authKey)

		self.Player.showAuthCode(imgUrl)

	def __authPlay (self, authKey) :
		self.Player.watchLinkStat = {'err': 0, 'msg': ''}
		self.bdAuth['input'] = authKey
		self.Player.showWatchLink()
		threading.Thread(target = self.__bdPlay).start()

	def __authDownload (self, authKey) :
		self.Player.downLinkStat = {'err': 0, 'msg': ''}
		self.bdAuth['input'] = authKey
		self.Player.showCloudLink()
		threading.Thread(target = self.__bdDownload).start()