# -*- coding: utf-8 -*-
import os
import sys
import shutil
import pymysql
import datetime
from PyQt5.QtCore import *
from subprocess import run
from PyQt5.QtWidgets import *
from PyQt5 import QtGui,QtCore,QtWidgets,uic



class choose_mode:

    def __init__(self):
        self.ui = uic.loadUi('UI/choose.ui')
        self.ui.photos.clicked.connect(self.photo)
        self.ui.video.clicked.connect(self.video)
        self.ui.select.clicked.connect(self.select)
        self.ui.open.clicked.connect(self.open)

    def photo(self):
        import photo_UI
        p = photo_UI.photo().ui
        p.show()

    def video(self):
        os.system('python video_UI.py')

    def select(self):
        import select_UI
        s = select_UI.select().ui
        s.show()

    def open(self):
        folder = 'G:/Graduation/code/test/runout'
        os.startfile(folder)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    choose = choose_mode()
    choose.ui.show()
    sys.exit(App.exec_())