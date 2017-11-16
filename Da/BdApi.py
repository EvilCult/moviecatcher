#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
import urllib
import base64
import time

from Lib import Tools
import Config

class BdApi :

	def __init__ (self) :
		self.Tools = Tools.Tools()
		self.Cfg = Config.Config()

		cfgInfo = self.Cfg.get()
		self.bdInfo = {
			'saveDir': cfgInfo['path'],
			'cookie': 'Cookie:' + cfgInfo['bdc']
		}

		if cfgInfo['bdc'] != '' :
			self.__getBdInfo()

	def saveLogin (self, cookieStr = '') :
		data = {'bdc': cookieStr}
		self.Cfg.save(data)

	def getBtInfo (self, url, auth = {}) :
		bdApi = 'https://pan.baidu.com/rest/2.0/services/cloud_dl?channel=chunlei&web=1&app_id=250528&bdstoken={}&clienttype=0'.format(self.bdInfo['token'])

		postData = {
			'method' : 'query_magnetinfo',
			'app_id' : '250528',
			'source_url' : url,
			'save_path' : '/' + self.bdInfo['saveDir'] + '/',
			'type' : '4'
		}

		if auth != {} :
			postData['input'] = auth['input']
			postData['vcode'] = auth['vcode']

		html = self.Tools.getPage(bdApi, self.requestHeader, postData)
		if html['code'] == 200 : 
			body = html['body']
			info = json.JSONDecoder().decode(body)

			idx = 1 
			for x in info:
				fileName = x['file_name'].split('/')
				fileName.pop(0)
				fileName = '/'.join(fileName)
				# some code...
				idx += 1

			result = {
				'err': 0,
				'btInfo': info['magnet_info']
			}
		else :
			body = html['body']
			info = json.JSONDecoder().decode(body)

			result = {
				'err': 1,
				'vcode': info['vcode'],
				'img': info['img']
			}

		return result

	def addTask (self, url, auth = {}, btIdx = 0) :
		bdApi = 'https://pan.baidu.com/rest/2.0/services/cloud_dl?channel=chunlei&web=1&app_id=250528&bdstoken={}&clienttype=0'.format(self.bdInfo['token'])
		postData = {
			'method' : 'add_task',
			'app_id' : '250528',
			'source_url' : url,
			'save_path' : '/' + self.bdInfo['saveDir'] + '/',
			'type' : '3'
		}

		if auth != {} :
			postData['input'] = auth['input']
			postData['vcode'] = auth['vcode']

		html = self.Tools.getPage(bdApi, self.requestHeader, postData)
		if html['code'] == 200 : 
			body = html['body']
			info = json.JSONDecoder().decode(body)
			result = {
				'err': 0,
				'taskID': info['task_id']
			}
		else :
			body = html['body']
			info = json.JSONDecoder().decode(body)

			result = {
				'err': 1,
				'vcode': info['vcode'],
				'img': info['img']
			}

		return result

	def getPlayUrl (self, taskID) :
		taskID = str(taskID)
		bdApi = 'https://yun.baidu.com/rest/2.0/services/cloud_dl?need_task_info=1&status=255&start=0&limit=10&method=list_task&app_id=250528&channel=chunlei&web=1&app_id=250528&bdstoken={}&clienttype=0'.format(self.bdInfo['token'])
		html = self.Tools.getPage(bdApi, self.requestHeader)
		if html['code'] == '200' : 
			body =  html['body']
		else :
			body =  html['body']

		info = json.JSONDecoder().decode(body)
		taskInfo = info['task_info']

		try:
			for x in taskInfo :
				if taskID == x['task_id'] :
					savePath = urllib.quote(x['save_path'].encode("UTF8"))
					playUrl = 'https://yun.baidu.com/play/video#video/path=' + savePath
					break 
		except Exception as e:
			playUrl = ''

		return (playUrl)

	def getDlUrl (self, taskID, retry = 0) :
		taskID = str(taskID)
		fID = self.__tIdTofId(taskID)
		fID = '["' + str(fID) + '"]'
		bdApi = 'https://yun.baidu.com/api/download?type=dlink&fidlist={}&timestamp={}&sign={}&channel=chunlei&clienttype=0&web=1&app_id=250528'.format(
			urllib.quote(fID),
			self.bdInfo['time'],
			urllib.quote(self.bdInfo['sign'])
		)
		
		html = self.Tools.getPage(bdApi, self.requestHeader)
		if html['code'] == '200' : 
			body =  html['body']
		else :
			body =  html['body']

		info = json.JSONDecoder().decode(body)

		if info['errno'] == 0 :
			try:
				dlLink = info['dlink'][0]['dlink']
			except Exception as e:
				dlLink = ''

			return dlLink
		else :
			if retry < 3 :
				retry += 1
				time.sleep(3)
				self.getDlUrl(taskID, retry)
			else :
				return ''

	def __getBdInfo (self) :
		bdApi = 'https://yun.baidu.com/disk/home?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0'
		self.requestHeader = [
			self.bdInfo['cookie'],
			'Host:pan.baidu.com',
			'Origin:https://pan.baidu.com',
			'Referer:https://pan.baidu.com/disk/home',
			'User-Agent:netdisk;5.3.4.5;PC;PC-Windows;5.1.2600;WindowsBaiduYunGuanJia'
		]
		html = self.Tools.getPage(bdApi, self.requestHeader)

		yunData = re.findall(r"var context\=([\s\S]*?)yunData", html['body'])

		if len(yunData) > 0 :
			yunData = yunData[0]
		else :
			yunData = ''

		self.bdInfo['username'] = re.findall(r'"username":"(.*?)"', yunData)[0]
		self.bdInfo['token'] = re.findall(r'"bdstoken":"(.*?)"', yunData)[0]
		self.bdInfo['time'] = re.findall(r'"timestamp":(.*?),', yunData)[0]

		bdSign1 = re.findall(r'"sign1":"(.*?)"', yunData)[0]
		bdSign3 = re.findall(r'"sign3":"(.*?)"', yunData)[0]
		self.bdInfo['sign'] = self.__getSign(bdSign3, bdSign1)

	def __getSign (self, j, r):
			a = []
			p = []
			o = ''
			v = len(j)

			for q in xrange(256):
				a.append(ord(j[q % v]))
				p.append(q)

			u = 0
			for q in xrange(256):
				u = (u + p[q] + a[q]) % 256
				t = p[q]
				p[q] = p[u]
				p[u] = t

			i = 0
			u = 0
			for q in xrange(len(r)):
				i = (i + 1) % 256
				u = (u + p[i]) % 256
				t = p[i]
				p[i] = p[u]
				p[u] = t
				k = p[((p[i] + p[u]) % 256)]
				o += chr(ord(r[q]) ^ k)

			return base64.b64encode(o)

	def __tIdTofId (self, taskID) :
		taskID = str(taskID)
		bdApi = 'https://yun.baidu.com/rest/2.0/services/cloud_dl?need_task_info=1&status=255&start=0&limit=10&method=list_task&app_id=250528&channel=chunlei&web=1&app_id=250528&bdstoken={}&clienttype=0'.format(self.bdInfo['token'])
		html = self.Tools.getPage(bdApi, self.requestHeader)
		if html['code'] == '200' : 
			body =  html['body']
		else :
			body =  html['body']

		info = json.JSONDecoder().decode(body)
		taskInfo = info['task_info']

		savePath = ''
		for x in taskInfo :
			if taskID == x['task_id'] :
				savePath = x['save_path']
				break

		bdApi = 'https://yun.baidu.com/api/list?order=time&desc=1&showempty=0&web=1&page=1&num=100&dir=%2F{}&channel=chunlei&web=1&app_id=250528&bdstoken={}&clienttype=0'.format(self.bdInfo['saveDir'], self.bdInfo['token'])
		html = self.Tools.getPage(bdApi, self.requestHeader)
		if html['code'] == '200' : 
			body =  html['body']
		else :
			body =  html['body']

		info = json.JSONDecoder().decode(body)
		fileInfo = info['list']

		fId = 0
		for x in fileInfo :
			if savePath == x['path'] :
				fId = x['fs_id']
				break
		return fId