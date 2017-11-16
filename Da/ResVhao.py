#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from Lib import Tools

class Searcher :

	def __init__ (self) :
		self.Tools = Tools.Tools()
		self.page = 1
		self.zCookie = ''

	def find (self, keyword) :
		self.result = []
		keyword = keyword.encode("gbk")
		self.getList(keyword)
		return self.result

	def getList (self, keyword) :
		url = 'http://www.6vhao.tv/e/search/index.php'
		header = [
			'Host:www.6vhao.tv',
			'Origin:http://www.6vhao.tv',
			'Pragma:no-cache',
			'Connection:keep-alive',
			'Referer:http://www.6vhao.tv',
			'Content-Type:application/x-www-form-urlencoded',
			'Upgrade-Insecure-Requests:1',
			'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
		]
		post = {
			'keyboard': str(keyword),
			'show': 'title,smalltext',
			'tempid': 1,
			'tbname': 'Article'
		}
		html = self.Tools.getPage(url, header, post)

		data = re.findall(r"listimg[\s\S]*?href=\"(.*?)\"[\s\S]*?alt=\"(.*?)\"[\s\S]*?listInfo", html['body'])

		try:
			for x in data :
				self.result.append({
					'title': x[1].decode('gbk').encode('utf-8'),
					'url': x[0],
					'source': 'vhao'
				})
		except Exception as e:
			pass

		return self.result

	def getLink (self, url) :
		result = []

		header = [
			'Host:www.6vhao.tv',
			'Origin:http://www.6vhao.tv',
			'Pragma:no-cache',
			'Connection:keep-alive',
			'Referer:http://www.6vhao.tv',
			'Content-Type:application/x-www-form-urlencoded',
			'Upgrade-Insecure-Requests:1',
			'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
		]
		html = self.Tools.getPage(url, header)

		data = re.findall(r"#ffffbb[\s\S]*?href=\"(.*?)\"[\s\S]*?>(.*?)<\/a>", html['body'])

		try:
			for x in data :
				if x[0][0:4] != 'http':
					if x[0][0:4] == 'ed2k' :
						resultType = 'ed2k'
					else :
						resultType = 'magnet'

					temp = (
						'[' + resultType + ']' + x[1].decode('gbk').encode('utf-8'),
						x[0]
					)

					result.append(temp)
				
		except Exception as e:
			pass

		return result