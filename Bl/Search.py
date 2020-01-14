#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import webbrowser
from Da import ResZmz
from Da import ResVhao
from View import ResultView
import urllib.request, urllib.parse, urllib.error

class Search :

	def __init__ (self, master) :
		self.master = master
		self.ResWindow = ResultView.GUI(self.master)

	def showResult (self, key) :
		searchKey = key.get()
	
		self.ResWindow.showList(searchKey)
		self.ResWindow.listRst = ''
		data = ''
		
		self.ResWindow.getDetail = lambda data = data : self.__searchMovDetails(data)

		threading.Thread(target = lambda key = searchKey : self.__searchMov(key)).start()

		self.ResWindow.updateList()

	def __searchMov (self, key) :
		# 开启两重匹配找寻
		self.mainSearcher = ResZmz.Searcher()
		self.subSearcher = ResVhao.Searcher()
		mainResult = self.mainSearcher.find(key)
		subResult = self.subSearcher.find(key)
		
		mainResult.append({'title':'\n--------以下为低质量资源:--------\n','url':''})
		mainResult.extend(subResult)

		self.ResWindow.listRst = mainResult

	def __searchMovDetails (self, data):  
		self.ResWindow.resRst = ''
		self.ResWindow.showRes()

		# 开启多线程
		threading.Thread(target = lambda data = data : self.__getDetails(data)).start()

		self.ResWindow.updateRes()

	def __getDetails (self, data) :
		if data['url'] != '' :
			if data['source'] == 'zmz' :
				result = self.mainSearcher.getLink(data['url'])
			else :
				result = self.subSearcher.getLink(data['url'])

			self.ResWindow.resRst = result