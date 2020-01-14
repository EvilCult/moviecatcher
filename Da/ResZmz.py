#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from Lib import Tools

class Searcher :

	def __init__ (self) :
		self.Tools = Tools.Tools()
		self.page = 1
		self.zCookie = ''
		self.zmzUserInfo = {
			'username': 'moviecatcher',
			'password': '666666'
		}

	def find (self, keyword) :
		self.result = []
		#keyword = keyword.encode("UTF8")
		self.getList(keyword)
		return self.result

	def login (self) :
		url = 'http://www.zmz2019.com/User/Login/ajaxLogin'
		requestHeader = [
			'Origin:http://www.zmz2019.com',
			'Host:www.zmz2019.com',
			'Referer:http://www.zmz2019.com/user/login',
			'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
			'X-Requested-With:XMLHttpRequest'
		]
		postData = {
			'account': self.zmzUserInfo['username'],
			'password': self.zmzUserInfo['password'],
			'remember': '1',
			'url_back': 'http://www.zmz2019.com/'
		}
		html = self.Tools.getPage(url, requestHeader, postData)
		#zmz2019网站改版后，cookie应重新获取正确的，否则登录失败
		string = ''
		for s,v in html['header'].items():
			if s=='Set-Cookie':
				if re.findall('Max-Age=0',v):
					pass
				else:
					string += v
			else:
				pass
		s = re.findall('(GINFO=uid[\s\S]*?);',string)
		v = re.findall('(GKEY=[\s\S]*?);',string)
		string = s[0] + ';' + v[0] + ';'

		self.zCookie = 'Cookie: ' + self.Tools.fmtCookie(string)

	def getList (self, keyword) :
		url = 'http://www.zmz2019.com/search/index/?page=' + str(self.page) + '&keyword=' + str(keyword) + '&type='
		html = self.Tools.getPage(url)

		data = re.findall(r"search-result([\s\S]*?)pages-padding", html['body'])
		page = re.findall(r"\.\.\.(\d*?)<span></span>", html['body'])

		if page != [] and page != [''] :				
			page = int(page[-1])							#每次都会出现在-1的位置
		else :
			page = 1
		
		try:
			resultlist = re.findall(r"search-item([\s\S]*?)f4 time", data[0])

			for x in resultlist :
				resultType = re.findall(r"<em.*?>([\s\S]*?)</em>", x)[0]
				
				if resultType == '电影':
					self.result.append({
						'title': r'[电影]'+re.findall(r"list_title\">([\s\S]*?)</strong>", x)[0],
						'url': 'http://www.zmz2019.com' + re.findall(r"<a href=\"([\s\S]*?)\"><img", x)[0],
						'source' : 'zmz'
					})
				elif resultType == '电视剧':
					self.result.append({
						'title': r'[电视剧]'+re.findall(r"list_title\">([\s\S]*?)</strong>", x)[0],
						'url': 'http://www.zmz2019.com' + re.findall(r"<a href=\"([\s\S]*?)\"><img", x)[0],
						'source' : 'zmz'
					})
				else:
					pass

		except Exception as e:
			pass

		if self.page < page :
			self.page += 1
			self.getList(keyword)
		else :
			return self.result

	def getLink (self, url) :
		self.login()
		result = []
		url = url.replace('resource', 'resource/list')
		requestHeader = [self.zCookie]
		html = self.Tools.getPage(url, requestHeader)

		data = re.findall(r"media-list([\s\S]*?)</ul>", html['body'])
	
		try:
			for x in data :
				resultType = re.findall(r"class=\"it\">([\s\S]*?)</h2>", x)[0]
				resultData = re.findall(r"class=\"fr\"([\s\S]*?)</div>", x)
				resultInfo = re.findall(r"class=\"fl\"([\s\S]*?)</div>", x)

				if resultType != '离线+在线' and  resultType != 'RMVB' and resultData !=[] :
					for idx, item in enumerate(resultData) :
						resultlist = re.findall(r"<a href=\"([\s\S]*?)\" type=\"([\s\S]*?)\">", item)
						movInfo = re.findall(r"<a title=\"([\s\S]*?)\" href", resultInfo[idx])
						for mov in resultlist :
							if mov[1] == 'ed2k' or mov[1] == 'magnet':
								temp = (
									resultType + '-' + movInfo[0],
									mov[0]
								)

								result.append(temp)
				
		except Exception as e:
			pass
		result_set = list(set(result))
		result_set.sort(key = result.index)

		return result_set