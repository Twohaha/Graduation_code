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


class select:

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = uic.loadUi('UI/select.ui')

        # 添加槽函数
        self.showtime()
        self.ui.select.clicked.connect(self.select_sql)
        self.ui.input.returnPressed.connect(self.select_sql)
        self.ui.mode.currentIndexChanged.connect(self.mode)
        self.ui.remind.setText('欢迎使用YOLOv7+CRNN车牌识别系统。')
        # 文本框提示输入内容
        self.ui.input.setPlaceholderText('请输入')
        # 表格自适应显示
        self.ui.results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # 判断查询类型
    def mode(self, imfo):
        if imfo == 0:
            self.ui.remind.setText('请先在下方选择您要查询的类型')
        elif imfo == 1:
            self.ty = '车牌号码'
            self.img = 'license'
            self.ui.remind.setText('您选择了使用“车牌号码”进行查询，请在下方输入栏中输入车牌号码')
        elif imfo == 2:
            self.ty = '车辆类型'
            self.img = 'car_type'
            self.ui.remind.setText('您选择了使用“车辆类型”进行查询，请在下方输入栏中输入车辆类型，例如：小汽车、新能源汽车（具体类型详见论文）')
        elif imfo == 3:
            self.ty = '车牌颜色'
            self.img = 'car_color'
            self.ui.remind.setText('您选择了使用“车牌颜色”进行查询，请在下方输入栏中输入车牌颜色，例如：X色')
        elif imfo == 4:
            self.ty = '车牌归属地'
            self.img= 'car_place'
            self.ui.remind.setText('您选择了使用“车牌归属地”进行查询，请在下方输入栏中输入车牌归属地，例如：重庆、北京、安徽')
        else:
            self.ty = '识别记录时间'
            self.img = 'time'
            self.ui.remind.setText('您选择了使用“识别记录时间”进行查询，日期与时间之间用空格分隔，日期之间用“ - ”分隔，时间之间用“ ：”分隔')

    # sql数据库
    def select_sql(self):
        try:
            mag = self.ui.input.text()
            db = pymysql.connect(host='localhost', user='root', password='164820', charset='utf8mb4',database='mydatabase')
            cur = db.cursor()
            if mag != "all":
                cur.execute(f"select license , car_type , car_place ,car_color ,time from data where {self.img} like '%{mag}%'")
                self.ui.remind.setText(f'您查询的类型为“{self.ty}”，查询的内容为“{mag}”')
            else:
                cur.execute("select license , car_type , car_color , car_place ,time from data")
                self.ui.remind.setText(f'您查询了数据库的所有内容')
        except:
            self.ui.remind.setText("请您先选择要查询的类型，完成选择以后在按下Enter或“查找车牌”按钮进行查询")
            self.ui.input.clear()
            return
        resu = cur.fetchall()
        if not resu:
            self.ui.remind.setText("输入数据有误，请检查输入数据")
        else:
            row = cur.rowcount
            vol = len(resu[0])
            # print(resu)
            self.write_table(resu, row, vol)
            self.ui.input.clear()
        cur.close()
        db.close()

    # 表格显示内容
    def show_table(self):
        db = pymysql.connect(host='localhost', user='root', password='164820', charset='utf8mb4',database='mydatabase')
        cur = db.cursor()
        cur.execute(f"select * from temp")
        table_text = cur.fetchall()
        row = cur.rowcount
        vol = len(table_text[0]) - 1
        cur.close()
        db.close()
        self.write_table(table_text, row, vol)

    # 向表格写入数据
    def write_table(self, table_text, row, vol):
        self.ui.results.setRowCount(row)
        for i in range(row):
            for j in range(vol):
                data = QtWidgets.QTableWidgetItem(str(table_text[i][j]))
                self.ui.results.setItem(i, j, data)  # 转换后可插入表格
        # self.ui.results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)    #让表格自适应窗口
        self.ui.results.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)       # 让窗口自适应文字宽度
        self.ui.results.setAlternatingRowColors(True)  # 使表格颜色交错显示

    # 获取当前时间
    def showCurrentTime(self, timeLabel):
        # 获取系统当前时间
        time = QDateTime.currentDateTime()
        # 设置系统时间的显示格式
        timeDisplay = time.toString('yyyy-MM-dd    hh:mm:ss   dddd')
        # print(timeDisplay)
        # 状态栏显示
        timeLabel.setText(timeDisplay)

    # 状态栏显示时间
    def showtime(self):
        self.timer = QtCore.QTimer()
        self.ui.timeLabel = QLabel()
        self.ui.statusBar.addPermanentWidget(self.ui.timeLabel, 0)
        self.timer.timeout.connect(lambda: self.showCurrentTime(self.ui.timeLabel))  # 这个通过调用槽函数来刷新时间
        self.timer.start(1000)  # 每隔一秒刷新一次，这里设置为1000ms  即1s


if __name__ == "__main__":
    App = QApplication(sys.argv)  # 创建QApplication对象，作为GUI主程序入口
    select = select().ui
    select.show()  # 显示主窗体
    sys.exit(App.exec_())  # 循环中等待退出程序


