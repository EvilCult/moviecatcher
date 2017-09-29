#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sqlite3
import platform
import time

from View import ConfigView
from Da import AppBase

class Config :

	def __init__(self):
		self.appTitle = AppBase.info['title']
		self.__getConfigPath()

		self.table = 'config'
		if self.__connect() == False:
			self.connStat = False
		else :
			self.connStat = True
			self.__chkTable()

	def __del__ (self) :
		if self.connStat == True :
			try:
				self.__disConn()
			except Exception as e:
				pass

	def show (self) :
		CfgView = ConfigView.GUI()
		data = self.get()
		CfgView.save = lambda data = data : self.save(data)
		CfgView.show(data)

	def get (self) :
		result = {'stat' : 1, 'msg' : ''}

		if self.connStat != False : 
			sql = "SELECT * FROM " + self.table + " ORDER BY id DESC LIMIT 1"
			self.cur.execute(sql)
			values = self.cur.fetchone()

			if values :
				result['stat'] = 0
				result['bdc'] = values[1]
				result['path'] = values[2]
				result['ariarpc'] = values[3]
				result['ariapath'] = values[4]
				result['udrate'] = values[5]
				result['udtime'] = values[6]
		
		return result

	def save (self, data) :
		result = {'stat' : 1, 'msg' : ''}

		param = ''
		for k, v in data.iteritems() :
		   param +=  ", " + k + " = '" + str(v) + "'"
		param = param[1:]

		if self.connStat != False : 
			sql = "UPDATE " + self.table + " SET " + param
			self.cur.execute(sql)
			self.conn.commit()
			result['msg'] = '更新成功！'

		return result

	def lastUd (self, timeStr) :
		if self.connStat != False : 
			sql = "UPDATE " + self.table + " SET udtime = " + str(timeStr)
			self.cur.execute(sql)
			self.conn.commit()

	def __connect (self) :
		try:
			if not os.path.exists(self.configPath) :
				os.makedirs(self.configPath)
			self.configPath = os.path.join(self.configPath, 'Config')

			self.conn = sqlite3.connect(self.configPath, check_same_thread = False)
			self.cur = self.conn.cursor()
			return True
		except:
			return False

	def __chkTable (self) :
		if self.connStat == False : return False

		sql = "SELECT tbl_name FROM sqlite_master WHERE type='table'"
		tableStat = False

		self.cur.execute(sql)
		values = self.cur.fetchall()

		for x in values:
			if self.table in x :
				tableStat = True

		if tableStat == False :
			self.__create()

	def __create (self) :
		if self.connStat == False : return False

		sql = 'create table ' + self.table + ' (id integer PRIMARY KEY autoincrement, bdc text, path varchar(500), ariarpc varchar(500), ariapath varchar(500), udrate int(1), udtime varchar(100))'
		self.cur.execute(sql);

		bdc = ''
		path = 'MovieCatcherFiles'
		ariarpc = ''
		ariapath = ''
		udrate = '2'
		udtime = str(int(time.time()))

		sql = "insert into " + self.table + " (bdc, path, ariarpc, ariapath, udrate, udtime) values ('" + bdc + "', '" + path + "', '" + ariarpc + "', '" + ariapath + "', " + udrate + ", '" + udtime + "')"

		self.cur.execute(sql)
		self.conn.commit()

	def __disConn (self) :
		if self.connStat == False : return False

		self.cur.close()
		self.conn.close()

	def __getConfigPath (self) :
		osType = platform.system()
		homeDir = os.path.expanduser('~')

		if osType == 'Darwin' :
			self.configPath = os.path.join(homeDir, 'Library', 'Application Support', self.appTitle)
		elif osType == 'Windows' :
			sysDrive = os.getenv("SystemDrive")
			self.configPath = os.path.join(homeDir, 'Documents', self.appTitle)