# -*- coding: utf-8 -*-
import os
import sys
import time
import shutil
import datetime
import detect_rec_plate
from subprocess import run
from PIL import Image, ImageTk
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMessageBox,QTextBrowser,QFileDialog


class Ui_recognition(object):

    # 初始化
    def setupUi(self, recognition):
        recognition.setObjectName("recognition")
        recognition.resize(1250, 800)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        recognition.setPalette(palette)
        recognition.setLayoutDirection(QtCore.Qt.LeftToRight)
        recognition.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.centralwidget = QtWidgets.QWidget(recognition)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.title = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.horizontalLayout_9.addWidget(self.title)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_3.addWidget(self.line_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 0, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 0, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.groupBox.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(15)
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.Original = QtWidgets.QLabel(self.groupBox)
        self.Original.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Original.sizePolicy().hasHeightForWidth())
        self.Original.setSizePolicy(sizePolicy)
        self.Original.setMaximumSize(QtCore.QSize(600, 560))
        self.Original.setText("")
        self.Original.setAlignment(QtCore.Qt.AlignCenter)
        self.Original.setObjectName("Original")
        self.horizontalLayout_4.addWidget(self.Original)
        self.horizontalLayout_6.addWidget(self.groupBox)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_6.addWidget(self.line_2)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.groupBox_2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(15)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.results = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.results.sizePolicy().hasHeightForWidth())
        self.results.setSizePolicy(sizePolicy)
        self.results.setMaximumSize(QtCore.QSize(600, 400))
        self.results.setText("")
        self.results.setAlignment(QtCore.Qt.AlignCenter)
        self.results.setObjectName("results")
        self.horizontalLayout_5.addWidget(self.results)
        self.horizontalLayout_6.addWidget(self.groupBox_2)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 1)
        self.horizontalLayout_6.setStretch(2, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(20)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.Identify_results = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Identify_results.sizePolicy().hasHeightForWidth())
        self.Identify_results.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(15)
        self.Identify_results.setFont(font)
        self.Identify_results.setObjectName("Identify_results")
        self.horizontalLayout_2.addWidget(self.Identify_results)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.daydate = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.daydate.sizePolicy().hasHeightForWidth())
        self.daydate.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(15)
        self.daydate.setFont(font)
        self.daydate.setObjectName("daydate")
        self.horizontalLayout.addWidget(self.daydate)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.name = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(15)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.horizontalLayout_3.addWidget(self.name)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_7.addWidget(self.label_4)
        self.location = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.location.sizePolicy().hasHeightForWidth())
        self.location.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(9)
        self.location.setFont(font)
        self.location.setObjectName("location")
        self.horizontalLayout_7.addWidget(self.location)
        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.images = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.images.sizePolicy().hasHeightForWidth())
        self.images.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.images.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(15)
        self.images.setFont(font)
        self.images.setObjectName("images")
        self.verticalLayout.addWidget(self.images)
        self.video = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video.sizePolicy().hasHeightForWidth())
        self.video.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.video.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(15)
        self.video.setFont(font)
        self.video.setObjectName("video")
        self.verticalLayout.addWidget(self.video)
        self.start = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start.sizePolicy().hasHeightForWidth())
        self.start.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.start.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(15)
        self.start.setFont(font)
        self.start.setObjectName("start")
        self.verticalLayout.addWidget(self.start)
        self.open_2 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_2.sizePolicy().hasHeightForWidth())
        self.open_2.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.open_2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(15)
        self.open_2.setFont(font)
        self.open_2.setObjectName("open_2")
        self.verticalLayout.addWidget(self.open_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 4)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 3)
        self.horizontalLayout_2.setStretch(4, 2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_3.addWidget(self.line_4)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(2, 7)
        self.verticalLayout_3.setStretch(4, 3)
        recognition.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(recognition)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1041, 26))
        self.menubar.setObjectName("menubar")
        recognition.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(recognition)
        self.statusBar.setObjectName("statusBar")
        recognition.setStatusBar(self.statusBar)
        self.file = QtWidgets.QAction(recognition)
        self.file.setObjectName("file")
        self.open = QtWidgets.QAction(recognition)
        self.open.setObjectName("open")
        self.save = QtWidgets.QAction(recognition)
        self.save.setObjectName("save")

        # 添加槽函数
        self.images.clicked.connect(self.tupian)
        self.video.clicked.connect(self.shipin)
        self.start.clicked.connect(self.kaishi)
        self.open_2.clicked.connect(self.baocun)
        self.daydate.setText(self.show_daytime())
        self.Identify_results.setText('欢迎使用YOLOv7+CRNN车牌识别系统。')
        self.Original.setPixmap(QtGui.QPixmap('../CQJTU.png'))
        self.results.setPixmap(QtGui.QPixmap('../CQJTU.png'))
        self.statusShowTime()

        self.retranslateUi(recognition)
        QtCore.QMetaObject.connectSlotsByName(recognition)

    # 重新翻译用户界面
    def retranslateUi(self, recognition):
        _translate = QtCore.QCoreApplication.translate
        recognition.setWindowTitle(_translate("recognition", "MainWindow"))
        self.title.setText(_translate("recognition", "基于机器视觉的车牌识别"))
        self.groupBox.setTitle(_translate("recognition", "图像"))
        self.groupBox_2.setTitle(_translate("recognition", "识别结果"))
        self.label_5.setText(_translate("recognition", "运行\n结果"))
        self.label_2.setText(_translate("recognition", "日期"))
        self.label_3.setText(_translate("recognition", "项目\n名称"))
        self.label_4.setText(_translate("recognition", "项目\n路径"))
        self.images.setText(_translate("recognition", "选择图片"))
        self.video.setText(_translate("recognition", "选择视频"))
        self.start.setText(_translate("recognition", "开始识别"))
        self.open_2.setText(_translate("recognition", "打开识别路径"))


    # 导入图片
    def tupian(self):
        images_file,images_type = QFileDialog.getOpenFileName(self.centralwidget,"选择你要上传的图片",'../test',filter="图片类型 (*.jpg);;图片类型(*.png)")
        # print(images_file,images_type)
        # print(type(images_file))
        if images_file:
            # 显示框清屏
            self.Original.clear()
            self.results.clear()
            file_name = images_file.split('/')[-1]
            # 显示文件名
            self.name.setText(file_name)
            # 显示文件路径
            self.location.setText(images_file)
            # 显示原始图片
            self.Original.setPixmap(QtGui.QPixmap(images_file))
            self.Original.setScaledContents(True)
            # 清理缓存文件夹并创建缓存文件夹
            shutil.rmtree('../../../test/temp')
            os.mkdir('../../../test/temp')
            # 复制图片到缓存文件夹中
            shutil.copy(images_file, '../../../test/temp')
            self.Identify_results.setText('图片导入成功！\n点击“开始识别”启动系统。')
            print('导入图片','  ',images_file)
        else:
            self.Identify_results.setText('取消识别')
            print('取消导入图片')


    # 导入视频并开始识别
    def shipin(self):
        print('选择视频')
        # 显示框清屏
        self.Original.clear()
        self.results.clear()
        self.Identify_results.setText('视频识别启动中，请等待...')
        video_file,video_type = QFileDialog.getOpenFileNames(self.centralwidget,"选择你要上传的视频",'../test',filter="视频类型 (*.MP4);;视频类型(*.mkv)")
        # print(video_file,video_type)
        self.Identify_results.clear()
        if video_file:
            file_name = video_file[0].split('/')[-1]
            # 显示文件名
            self.name.setText(file_name)
            # 显示文件路径
            self.location.setText(video_file[0])

            print('开始识别视频')
            cmd = 'python E:\\Graduation\\code\\graduation_code\\detect_rec_plate.py --video {}'
            run(cmd.format(video_file[0]), shell=True)
            self.Identify_results.setText('视频识别完成，请点击“打开识别路径”查看识别结果。')
            print("识别完成~")
        else:
            self.Identify_results.setText('取消识别')
            print('取消视频识别')


    # 开始识别图片
    def kaishi(self):
        print('开始识别')
        self.Identify_results.setText('识别中，请等待...')
        cmd = 'python ../graduation_code/detect_rec_plate.py --source E:/Graduation/code/test/temp'
        run(cmd,shell=True)
        # 显示结果图片
        img = os.listdir('../../../test/temp')
        file_location = 'E:/Graduation/code/test/runout/'+img[0]
        self.Original.setPixmap(QtGui.QPixmap(file_location))
        self.Original.setScaledContents(True)
        # 调用判断车辆类型的方法
        self.combination('../../Temp.txt')
        print("识别完成~")


    # 打开识别完成的路径
    def baocun(self):
        folder ='E:\\Graduation\\code\\test\\runout'
        os.startfile(folder)


    # 显示当前日期（拟改为运行时间）
    def show_daytime(self):
        daytime = datetime.datetime.now().strftime('%Y-%m-%d')
        return str(daytime)


    # 判断车辆类型
    def judge(self,ple_color,ple_license):
        if ple_color == '蓝色':
            p_type = '小汽车'
        elif ple_color == '绿色':
            p_type = '新能源汽车'
        elif ple_color == '黄色':
            if ple_license[-1] == '学':
                p_type = '教练车'
            else:
                p_type = '工程车'
        elif ple_color == '黑色':
            if ple_license[-1] == '港':
                p_type = '香港车辆'
            elif ple_license[-1] == '澳':
                p_type = '澳门车辆'
            elif ple_license[0] == "使":
                p_type = '使馆车辆'
            else:
                p_tupe = '领馆车辆'
        elif ple_color == '白色':
            if ple_license[0] == 'W':
                p_type = '武警车辆'
            else:
                p_type = '警车'
        else:
            p_type = '其他车辆'
        return p_type

    def place(self,license):
        t = license[0]
        if t == "W":
            t = license[2]
        car_dict = {'京': '北京', '津': '天津', '沪': '上海', '渝': '重庆',
                    '蒙': '内蒙古', '新': '新疆', '藏': '西藏', '宁': '宁夏',
                    '桂': '广西', '港': '香港', '澳': '澳门', '黑': '黑龙江',
                    '吉': '吉林', '辽': '辽宁', '晋': '山西', '冀': '河北',
                    '青': '青海', '鲁': '山东', '豫': '河南', '苏': '江苏',
                    '皖': '安徽', '浙': '浙江', '闽': '福建', '赣': '江西',
                    '湘': '湖南', '鄂': '湖北', '粤': '广东', '琼': '海南',
                    '甘': '甘肃', '陕': '陕西', '贵': '贵林', '云': '云南',
                    '川': '四川', '危': '危险品运输车', '航': '机场专用车辆'}
        return car_dict[t]

    def combination(self,file_path):
        with open(file=str(file_path), mode='r', encoding='utf-8') as j:
            imfo = j.read().split()
            a = int(len(imfo) / 2)
            show = ''
            for i in range(a):
                ple_color = imfo[(2 * i + 1)]
                ple_license = imfo[(2 * i)]
                temp = f'车型：{self.judge(ple_color,ple_license)}\n车牌：{ple_license}\n车辆归属地为：{self.place(ple_license)}\n添加数据库完成\n'
                show += temp
            self.results.setText(f'识别完成！\n{show}')

    # 获取当前时间
    def showCurrentTime(self,timeLabel):
        # 获取系统当前时间
        time = QDateTime.currentDateTime()
        # 设置系统时间的显示格式
        timeDisplay = time.toString('yyyy-MM-dd    hh:mm:ss   dddd')
        # print(timeDisplay)
        # 状态栏显示
        timeLabel.setText(timeDisplay)


    # 状态栏显示时间
    def statusShowTime(self):
        self.timer =QtCore.QTimer()
        self.timeLabel = QLabel()
        self.statusBar.addPermanentWidget(self.timeLabel, 0)
        self.timer.timeout.connect(lambda: self.showCurrentTime(self.timeLabel))  # 这个通过调用槽函数来刷新时间
        self.timer.start(1000)  # 每隔一秒刷新一次，这里设置为1000ms  即1s


if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=Ui_recognition()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())