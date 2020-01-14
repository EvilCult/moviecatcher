#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import re
import ssl
import os
import platform
import sys
import chardet        #判断网页编码方式的库
import string

class Tools :

	def __init__ (self) :
		pass

	def getPage (self, url, requestHeader = [], postData = {}) :
		url = urllib.parse.quote_plus(url,safe=string.printable)			#解决了不能打开含中文网址的问题，同时“空格”由“+”代替
		if postData == {} :
			request = urllib.request.Request(url)
		elif isinstance(postData, str) :
			request = urllib.request.Request(url, postData)
		else :
			request = urllib.request.Request(url, urllib.parse.urlencode(postData).encode('utf-8'))

		for x in requestHeader :
			headerType = x.split(':')[0]
			headerCon = x.replace(headerType + ':', '')
			request.add_header(headerType, headerCon)

		try : 
			ctx = ssl.create_default_context()
			ctx.check_hostname = False
			ctx.verify_mode = ssl.CERT_NONE
			response = urllib.request.urlopen(request, context = ctx)
			header = response.headers
			body = response.read()
			jiema =  lambda coding : 'gbk' if coding=='GB2312' else coding		#加上编码，这里需要把GB2312转为GBK编码
			body = body.decode(jiema(chardet.detect(body)['encoding']))			#加上编码解码
			code = response.code
		except urllib.error.HTTPError as e:
			header = e.headers
			body = e.read()
			code = e.code

		result = {
			'code': code,
			'header': header,
			'body': body
		}

		return result

	def fmtCookie (self, string) :
		result = re.sub(r"path\=\/.", "", string)
		result = re.sub(r"(\S*?)\=deleted.", "", result)
		result = re.sub(r"expires\=(.*?)GMT;", "", result)
		result = re.sub(r"domain\=(.*?)tv.", "", result)
		result = re.sub(r"httponly", "", result)
		result = re.sub(r"\s", "", result)

		return result

	def urlencode(self, str) :
		reprStr = repr(str).replace(r'\x', '%')
		return reprStr[1:-1]

	def getRes (self, fileName) :
		if getattr(sys, 'frozen', False):
			base_path = os.path.join(sys._MEIPASS, 'RES')
		else:
			base_path = os.path.join(os.path.abspath("../"), 'Resources')

		filePath = os.path.join(base_path, fileName)

		return filePath

	def isWin (self) :
		osType = platform.system()

		if osType == 'Windows' :
			return True
		else :
			return False