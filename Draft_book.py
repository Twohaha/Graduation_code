# -*- coding: utf-8 -*-
import os
import sys
import datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore,QtWidgets,uic


class Stats:

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = uic.loadUi('UI/choose.ui')
        # self.ui.photos.clicked.connect(self.photo)
        # self.ui.video.clicked.connect(self.video)
        # self.ui.select.clicked.connect(self.select)
        # self.ui.open.clicked.connect(self.open)


    def photo(self):
        import photo_UI
        p = photo_UI.photo().ui
        p.show()

    def video(self):
        import video_UI
        v = video_UI.video().ui
        v.show()

    def select(self):
        import select_UI
        s = select_UI.select().ui
        s.show()

    def open(self):
        folder ='G:/Graduation/code/test/runout'
        os.startfile(folder)


if __name__ == "__main__":
    App = QApplication(sys.argv)  # 创建QApplication对象，作为GUI主程序入口
    stats = Stats()
    stats.ui.show()  # 显示主窗体
    sys.exit(App.exec_())  # 循环中等待退出程序