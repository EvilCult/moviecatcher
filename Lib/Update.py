#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib.request, urllib.error, urllib.parse

class Update :

	def __init__ (self) :
		self.updateSource = 'http://evilcult.github.io/Video-Downloader/version.json'

	def check (self, appVer) :
		result = {
			'update' : False,
			'msg' : '当前已是最新版本。'
		}
		server = self.__getServerInfo()
		if server != False :
			if float(appVer) < float(server['appVer']) :
				result['update'] = True
				result['version'] = server['version']
				result['msg'] = server['info']
				result['dUrl'] = server['dUrl']
		else :
			result['msg'] = '网络故障，请稍后再试(GFW的问题你懂的)'

		return result

	def __getServerInfo (self) :
		try:
			response = urllib.request.urlopen(self.updateSource)
			jsonStr = response.read().decode('utf-8')
			appInfo =  json.JSONDecoder().decode(jsonStr)
		except Exception as e:
			appInfo = False
		
		return appInfo	

