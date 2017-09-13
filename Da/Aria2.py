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

	def download (self, fileUrl, fileName) :
		os.system('open -a "' + str(self.ariaGuiPath) + '"')
		rpc = self.__getRpc(fileUrl, fileName)
		dlStat = self.Tools.getPage(self.ariaHost, [], rpc)
		os.system('open -a "' + str(self.ariaGuiPath) + '"')

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