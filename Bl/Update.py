#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time

from Da import AppBase
from Da import Config
from Da import Updater
from View import UpdateInfoView

class Update :

	def __init__ (self) :
		self.app = AppBase.info
		self.Updater = Updater.Updater()
		self.Cfg = Config.Config()
		self.UdView = UpdateInfoView.GUI()

	def chkUpdate (self, force = False) :
		cfgInfo = self.Cfg.get()
		now = int(time.time())

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
			self.UdView.show()
			threading.Thread(target = self.__check).start()
			self.UdView.updateInfo()

	def __check (self) :
		now = int(time.time())

		info = self.Updater.check(self.app['build'])
		self.Cfg.save({'udtime': now})
		self.UdView.udInfo = info
