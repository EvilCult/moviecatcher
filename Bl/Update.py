#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time

from Lib import Tools
from Da import AppBase
from Da import Config
from Da import Updater
from View import UpdateInfoView

class Update :

	def __init__ (self) :
		self.winTitle = 'Information'
		self.Tools = Tools.Tools()
		self.app = AppBase.info
		self.Updater = Updater.Updater()
		self.Cfg = Config.Config()
		self.UdView = UpdateInfoView.GUI()

	def chkUpdate (self, force = False) :
		threading.Thread(target = lambda force = force : self.__check(force)).start()

	def __check (self, force) :
		now = int(time.time())
		cfgInfo = self.Cfg.get()

		if force == False :
			if cfgInfo['udrate'] == 1:
				updateTime = int(cfgInfo['udtime']) + 86400
			elif cfgInfo['udrate'] == 2:
				updateTime = int(cfgInfo['udtime']) + 86400 * 7
			elif cfgInfo['udrate'] == 3:
				updateTime = int(cfgInfo['udtime']) + 86400 * 30
			else :
				updateTime = int(cfgInfo['udtime']) + 86400 * 7
		else :
			updateTime = 0

		if updateTime < now :
			info = self.Updater.check(self.app['build'])

			self.Cfg.save({'udtime': now})

			if force == True or info['update'] == True :
				self.UdView.show(info)
