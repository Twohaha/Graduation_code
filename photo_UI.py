# -*- coding: utf-8 -*-
import os
import sys
import shutil
import pymysql
import datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui,QtCore,QtWidgets,uic


class photo:

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = uic.loadUi('UI/photos.ui')
        # 添加槽函数
        self.ui.images.clicked.connect(self.tupian)
        self.ui.open_2.clicked.connect(self.baocun)
        self.ui.start.clicked.connect(self.kaishi)
        self.show_daytime()
        self.ui.Identify_results.setText('欢迎使用YOLOv7+CRNN车牌识别系统。')
        self.ui.Original.setPixmap(QtGui.QPixmap('UI/CQJTU.png'))
        # 显示时间
        self.statusShowTime()
        # 表格自适应显示
        self.ui.results.resizeColumnsToContents()



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

    # 导入图片
    def tupian(self):
        images_file, images_type = QtWidgets.QFileDialog.getOpenFileNames(None, "选择你要上传的图片",'../test',filter="图片类型 (*.jpg);;图片类型(*.png)")
        # print(images_file, images_type)
        # print(type(images_file))
        # print(images_path,'   ',images_name)
        if images_file:
            images_path, images_name = os.path.split(images_file[0])
            if len(images_file) > 1:
                # 显示文件名
                self.ui.name.setText(f"选择了“{images_name}”等{len(images_file)}个图片")
                # 显示文件路径
                self.ui.location.setText(images_path)
                # 显示图片
                self.ui.Original.setPixmap(QtGui.QPixmap(images_file[0]))
                self.ui.Original.setScaledContents(True)

                # 清理缓存文件夹并创建缓存文件夹
                shutil.rmtree('../test/temp')
                os.mkdir('../test/temp')
                for file in images_file:
                    shutil.copy(file, '../test/temp')
                    self.ui.Identify_results.setText('图片导入成功！\n点击“开始识别”启动系统。')
                print(f'导入{images_name}等{len(images_file)}个文件')
            else:
                # 显示文件名
                self.ui.name.setText(images_name)
                # 显示文件路径
                self.ui.location.setText(images_path)
                # 显示原始图片
                self.ui.Original.setPixmap(QtGui.QPixmap(images_file[0]))
                self.ui.Original.setScaledContents(True)
                # 清理缓存文件夹并创建缓存文件夹
                shutil.rmtree('../test/temp')
                os.mkdir('../test/temp')
                # 复制图片到缓存文件夹中
                shutil.copy(images_file[0], '../test/temp')
                self.ui.Identify_results.setText('图片导入成功！\n点击“开始识别”启动系统。')
                print('导入图片', '  ', images_file)
        else:
            self.ui.Identify_results.setText('取消识别')
            print('取消导入图片')


    # 开始识别图片
    def kaishi(self):
        print('开始识别')
        self.ui.Identify_results.setText('识别中，请等待...')
        cmd = 'python detect_rec_plate.py --source ../test/temp'
        # run(cmd, shell=True)
        self.show_table()
        # 显示结果图片
        img = os.listdir('../test/temp')
        file_location = '../test/runout/' + img[0]
        self.ui.Original.setPixmap(QtGui.QPixmap(file_location))
        self.ui.Original.setScaledContents(True)
        self.ui.Identify_results.setText('识别完成,久等了!!!')
        print("识别完成~")

    # 打开识别完成的路径
    def baocun(self):
        folder = '../test/runout'
        os.startfile(folder)

    # 显示当前日期（拟改为运行时间）
    def show_daytime(self):
        daytime = datetime.datetime.now().strftime(' %Y年 %m月 %d日')
        # self.daydate.setStyleSheet('{text-align:center}')
        self.ui.daydate.setText(daytime)

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
    def statusShowTime(self):
        self.timer = QtCore.QTimer()
        self.ui.timeLabel = QLabel()
        self.ui.statusBar.addPermanentWidget(self.ui.timeLabel, 0)
        self.timer.timeout.connect(lambda: self.showCurrentTime(self.ui.timeLabel))  # 这个通过调用槽函数来刷新时间
        self.timer.start(1000)  # 每隔一秒刷新一次，这里设置为1000ms  即1s


if __name__ == "__main__":
    App = QApplication(sys.argv)  # 创建QApplication对象，作为GUI主程序入口
    photo = photo().ui
    photo.show()  # 显示主窗体
    sys.exit(App.exec_())  # 循环中等待退出程序


