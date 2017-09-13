## Movie Catcher

「我想看个美剧不知道哪里有？」

「这个资源怎么没速度？」

「为什么非得用客户端？」

这些个问题都将不是问题。。。。

### 简介

整合资源站点及网盘离线功能，通过标题搜索电影/美剧的下载资源，通过网盘在线播放，或获取网盘离线的真实下载地址，脱离客户端，实现离线下载功能。

后期初步仅支持【搜索】，【离线下载】，【在线播放】，后期会逐渐加入新功能，以及扩展资源搜索范围。

Mac版App下载：[下载地址](https://github.com/EvilCult/moviecatcher/releases/tag/Beta0.9.5(29BA0)).

Windows版exe暂不提供，带后期开发.

### 使用说明

[传送门](https://github.com/EvilCult/moviecatcher/wiki/Application-Guide).

### 系统要求

App ： MacOs 10.12 及以上

Python ： 2.7.10

依赖包 : Pillow, selenium


### 系统要求

离线下载请搭配[Aria2Gui](https://github.com/yangshun1029/aria2gui/releases), 强烈推荐.

### 附注

源代码已开放[GitHub](https://github.com/EvilCult/moviecatcher).如对登陆不放心，可详查源代码，并且，.spec文件已上传，可食用Pyinstaller自行打包使用。

Mac需要注意，系统的Tcl/Tk版本存在bug，Entry无法输入中文，请更新至8.5.18可解决此问题。（新系统有rootless，先关闭后，再替换'/system/library/frameworks'目录下的文件（目前感觉最完美的解决方案，如有更好请告诉我））

本软件其实就是个自动操作流，如果还是不放心填密码，来来来，我教你如何人工手动来实现。。。


