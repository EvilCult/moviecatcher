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
		keyword = keyword.encode("UTF8")
		self.getList(keyword)
		return self.result

	def getList (self, keyword) :
		url = 'http://www.3gdyy.com/search.htm'
		header = [
			'Host:www.3gdyy.com',
			'Origin:http://www.3gdyy.com',
			'Pragma:no-cache',
			'Referer:http://www.3gdyy.com/search.htm',
			'Upgrade-Insecure-Requests:1',
			'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
		]
		post = {'keyword': str(keyword)}
		html = self.Tools.getPage(url, header, post)

		data = re.findall(r"<a href=\"(thread-\d*?.htm)\">(.*?)</a>", html['body'])

		try:
			for x in data :
				self.result.append({
					'title': x[1],
					'url': 'http://www.3gdyy.com/' + x[0],
					'source': 'gdyy'
				})
		except Exception as e:
			pass

		return self.result


	def getLink (self, url) :
		result = []

		header = [
			'Host:www.3gdyy.com',
			'Origin:http://www.3gdyy.com',
			'Pragma:no-cache',
			'Referer:http://www.3gdyy.com/search.htm',
			'Upgrade-Insecure-Requests:1',
			'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
		]
		html = self.Tools.getPage(url, header)

		data = re.findall(r"<tr>[\s\S]*?<td class=\"post2\">[\s\S]*?<a href=\"(.*?)\">(.*?)</a>[\s\S]*?</td>[\s\S]*?<td align=\"center\" class=\"post2\">(.*?)</td>[\s\S]*?</tr>", html['body'])

		try:
			for x in data :
				temp = (
					'[' + x[2] + ']' + x[1],
					x[0]
				)

				result.append(temp)
				
		except Exception as e:
			pass

		return result