#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

from Lib import Tools
import Config

class Aria2 :

	def __init__ (self) :
		self.Tools = Tools.Tools()
		self.Cfg = Config.Config()

		cfgInfo = self.Cfg.get()

		self.ariaHost = cfgInfo['ariarpc']
		self.ariaGuiPath = cfgInfo['ariapath']

	def chkAria (self) :
		try :
			os.system('open -a "' + str(self.ariaGuiPath) + '"')
		except Exception as e:
			self.ariaGuiPath = ''

		param = {
			"jsonrpc": "2.0",
			"method": "aria2.getGlobalStat",
			"id": 1,
			"params": [],
		}
		ariaRpc = json.JSONEncoder().encode([param])

		try:
			ariaStat = self.Tools.getPage(self.ariaHost, [], ariaRpc)
			if ariaStat['code'] == 200 :
				return True
			else :
				return False
		except Exception as e:
			return False

	def download (self, fileUrl, fileName) :
		rpc = self.__getRpc(fileUrl, fileName)
		dlStat = self.Tools.getPage(self.ariaHost, [], rpc)

		if self.ariaGuiPat != '':
			os.system('open -a "' + str(self.ariaGuiPath) + '"')
		else :
			webbrowser.open_new('http://aria2c.com/')

	def __getRpc (self, fileUrl, fileName) :
		link = [fileUrl]
		conf = {
			"out": fileName,
			"split": "20",
			"max-connection-per-server": "20",
			"seed-ratio": "0"
		}

		dlTemplate = {
			"jsonrpc": "2.0",
			"method": "aria2.addUri",
			"id": 1,
			"params": [link, conf],
		}

		ariaRpc = json.JSONEncoder().encode([dlTemplate])

		return ariaRpc