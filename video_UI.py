# -*- coding: utf-8 -*-
import os
import sys
import pymysql
import datetime
from subprocess import run
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore,QtWidgets,uic


class video:

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = uic.loadUi('UI/video.ui')
        self.ui.openfile.clicked.connect(self.openfiles)
        self.ui.start.clicked.connect(self.start)
        self.ui.openvideo.clicked.connect(self.openvideo)

        self.show_daytime()
        self.showtime()
        self.ui.results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)



    # 导入视频
    def openvideo(self):
        print('选择视频')
        self.ui.outtext.setText('视频识别启动中，请等待...')
        video_file, video_type = QFileDialog.getOpenFileNames(None, "选择你要上传的视频", '../test',filter="视频类型 (*.MP4);;视频类型(*.mkv)")
        if video_file:
            video_path, video_name = os.path.split(video_file[0])
            self.path = video_file[0]
            # 显示文件名
            self.ui.name.setText(video_name)
            # 显示文件路径
            self.ui.location.setText(video_path)
            print('开始识别视频')

        else:
            self.ui.outtext.setText('取消识别')
            print('取消视频识别')

    # 开始识别
    def start(self):
        try:
            self.ui.outtext.setText('开始识别')
            cmd = 'python detect_rec_plate.py --video {}'
            run(cmd.format(self.path), shell=True)
            self.show_table()
            self.ui.outtext.setText('视频识别完成，请点击“打开识别路径”查看识别结果。')
            print("识别完成~")
        except:
            # self.ui.outtext.setText('请选择需要识别的视频')
            QMessageBox.critical(self.ui,'错误','请选择需要识别的视频')

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
        self.ui.results.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)    #让表格自适应窗口
        # self.ui.results.resizeColumnsToContents()  # 让窗口自适应文字宽度
        self.ui.results.setAlternatingRowColors(True)  # 使表格颜色交错显示


    # 打开识别完成的路径
    def openfiles(self):
        folder = 'G:/Graduation/code/test/runout'
        os.startfile(folder)

    # 显示当前日期（拟改为运行时间）
    def show_daytime(self):
        daytime = datetime.datetime.now().strftime(' %Y年 %m月 %d日')
        # self.daydate.setStyleSheet('{text-align:center}')
        self.ui.day.setText(daytime)

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
    video = video()
    video.ui.show()  # 显示主窗体
    sys.exit(App.exec_())  # 循环中等待退出程序


