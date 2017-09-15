#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading

from Da import ResZmz
from Da import ResGdyy
from View import ResultView

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
		self.mainSearcher = ResZmz.Searcher()
		self.subSearcher = ResGdyy.Searcher()
		mainResult = self.mainSearcher.find(key)
		subResult = self.subSearcher.find(key)
		
		mainResult.append({'title':'以下为低质量资源:--------','url':''})
		mainResult.extend(subResult)

		self.ResWindow.listRst = mainResult

	def __searchMovDetails (self, data):  
		self.ResWindow.resRst = ''
		self.ResWindow.showRes()

		threading.Thread(target = lambda data = data : self.__getDetails(data)).start()

		self.ResWindow.updateRes()

	def __getDetails (self, data) :
		if data['url'] != '' :
			if data['source'] == 'zmz' :
				result = self.mainSearcher.getLink(data['url'])
			else :
				result = self.subSearcher.getLink(data['url'])

			self.ResWindow.resRst = result