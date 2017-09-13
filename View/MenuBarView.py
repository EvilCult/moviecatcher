#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter
import webbrowser

import AppInfoView
from Da import Config
from Da import BdApi
import PlayerView
from Bl import Update


class GUI :

	def __init__ (self, master) :
		self.master = master

	def show (self) :
		menubar = Tkinter.Menu(self.master)

		fileMenu = Tkinter.Menu(menubar, tearoff = 0)
		appInfo = AppInfoView.GUI()
		fileMenu.add_command(label = "About Movie Catcher", command = appInfo.show)
		# url = 'https://github.com/EvilCult'
		# fileMenu.add_command(label = "Website", command = lambda url = url : webbrowser.open_new(url))
		url = 'https://github.com/EvilCult/moviecatcher/wiki'
		fileMenu.add_command(label = "Guide", command = lambda url = url : webbrowser.open_new(url))
		Ud = Update.Update()
		fileMenu.add_command(label = "Check Update", command = lambda force = True : Ud.chkUpdate(force))
		fileMenu.add_separator()
		url = 'https://evilcult.github.io/moviecatcher/donate.html'
		fileMenu.add_command(label = "Donate", command = lambda url = url : webbrowser.open_new(url))
		fileMenu.add_separator()
		fileMenu.add_command(label = "Quit", command = self.master.quit)
		menubar.add_cascade(label = "File", menu = fileMenu)

		editMenu = Tkinter.Menu(menubar, tearoff = 0)
		Cfg = Config.Config()
		editMenu.add_command(label = "Config", command = Cfg.show)
		editMenu.add_separator()
		editMenu.add_command(label = "Baidu Login", command = lambda cb = BdApi.BdApi().saveLogin : PlayerView.GUI().showLoginWindow(cb))
		menubar.add_cascade(label = "Edit", menu = editMenu)

		winMenu = Tkinter.Menu(menubar, tearoff = 0)
		url = 'https://pan.baidu.com'
		winMenu.add_command(label = "BaiduYun", command = lambda url = url : webbrowser.open_new(url))
		menubar.add_cascade(label = "Window", menu = winMenu)
	
		helpMenu = Tkinter.Menu(menubar, tearoff = 0)
		url = 'https://github.com/EvilCult/moviecatcher'
		helpMenu.add_command(label = "GitHub", command = lambda target = url : webbrowser.open_new(target))
		url = 'https://github.com/EvilCult/moviecatcher/releases'
		helpMenu.add_command(label = "Release Notes", command = lambda target = url : webbrowser.open_new(target))
		url = 'https://github.com/EvilCult/moviecatcher/issues'
		helpMenu.add_command(label = "Send Feedback", command = lambda target = url : webbrowser.open_new(target))
		menubar.add_cascade(label = "Help", menu = helpMenu)

		self.master.config(menu = menubar)