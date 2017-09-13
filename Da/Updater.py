#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib2

class Updater :

	def __init__ (self) :
		self.updateSource = 'https://evilcult.github.io/moviecatcher/version.json'

	def check (self, appVer) :
		result = {
			'update' : False,
			'version' : '',
			'dUrl' : '',
			'msg' : '当前已是最新版本。'
		}
		server = self.__getServerInfo()
		if server != False :
			if int(appVer, 16) < int(server['appVer'], 16) :
				result['update'] = True
				result['version'] = server['version']
				result['msg'] = server['info']
				result['dUrl'] = server['dUrl']
		else :
			result['msg'] = '网络故障，请稍后再试(Github和GFW的问题你懂的)'

		return result

	def __getServerInfo (self) :
		try:
			response = urllib2.urlopen(self.updateSource, timeout = 3)
			jsonStr = response.read()
			appInfo =  json.JSONDecoder().decode(jsonStr)
		except Exception as e:
			appInfo = False
		
		return appInfo	

