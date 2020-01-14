#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import tkinter

sys.path.append("..")
from View import MainView
from Bl import Update

class App :

	def __init__ (self) :
		self.Update = Update.Update()

	def run (self) :
		mainWindow = MainView.GUI()
		self.Update.chkUpdate()
		mainWindow.run()

App = App()
App.run()