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
		self.ResWindow.result = ''
		data = ''
		self.ResWindow.getDetail = lambda data = data : self.__searchMovDetails(data)

		threading.Thread(target = lambda key = searchKey : self.__searchMov(key)).start()

		self.ResWindow.update()

	def __searchMov (self, key) :
		self.mainSearcher = ResZmz.Searcher()
		self.subSearcher = ResGdyy.Searcher()
		mainResult = self.mainSearcher.find(key)
		subResult = self.subSearcher.find(key)
		
		mainResult.append({'title':'以下为低质量资源:--------','url':''})
		mainResult.extend(subResult)

		self.ResWindow.result = mainResult

	def __searchMovDetails (self, data):  
		self.movData = data

		threading.Thread(target = self.__getDetails).start()

	def __getDetails (self) :
		if self.movData['url'] != '' :
			if self.movData['source'] == 'zmz' :
				result = self.mainSearcher.getLink(self.movData['url'])
			else :
				result = self.subSearcher.getLink(self.movData['url'])

			threading.Thread(target = lambda rst = result : self.ResWindow.showRes(rst)).start()