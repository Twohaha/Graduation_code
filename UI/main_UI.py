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


class Stats:

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = uic.loadUi('my_UI.ui')

        # 添加槽函数
        self.ui.images.clicked.connect(self.tupian)
        self.ui.video.clicked.connect(self.shipin)
        self.ui.open_2.clicked.connect(self.baocun)
        self.ui.start.clicked.connect(self.kaishi)
        self.ui.sqlselect.clicked.connect(self.select_sql)
        self.ui.sqlresults.returnPressed.connect(self.select_sql)
        self.ui.comboBox.currentIndexChanged.connect(self.mode)
        self.show_daytime()
        self.ui.Identify_results.setText('欢迎使用YOLOv7+CRNN车牌识别系统。')
        self.ui.Original.setPixmap(QtGui.QPixmap('CQJTU.png'))
        # 显示时间
        self.statusShowTime()
        # 文本框提示输入内容
        self.ui.sqlresults.setPlaceholderText('请输入')
        # 表格自适应显示
        # self.ui.results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)



    # 判断查询类型
    def mode(self, imfo):
        # global table
        self.img = '1'
        if imfo == 0:
            self.ui.Identify_results.setText('请先在下方选择您要查询的类型')
        elif imfo == 1:
            self.ty = '车牌号码'
            self.img = 'license'
            self.ui.Identify_results.setText('您选择了使用“车牌号码”进行查询，请在下方输入栏中输入车牌号码')
        elif imfo == 2:
            self.ty = '车辆类型'
            self.img = 'car_type'
            self.ui.Identify_results.setText('您选择了使用“车辆类型”进行查询，请在下方输入栏中输入车辆类型，例如：小汽车、新能源汽车（具体类型详见论文）')
        elif imfo == 3:
            self.ty = '车牌颜色'
            self.img = 'car_color'
            self.ui.Identify_results.setText('您选择了使用“车牌颜色”进行查询，请在下方输入栏中输入车牌颜色，例如：X色')
        elif imfo == 4:
            self.ty = '车牌归属地'
            self.img= 'car_place'
            self.ui.Identify_results.setText('您选择了使用“车牌归属地”进行查询，请在下方输入栏中输入车牌归属地，例如：重庆、北京、安徽')
        else:
            self.ty = '识别记录时间'
            self.img = 'time'
            self.ui.Identify_results.setText('您选择了使用“识别记录时间”进行查询，日期与时间之间用空格分隔，日期之间用“ - ”分隔，时间之间用“ ：”分隔')

    # sql数据库
    def select_sql(self):
        try:
            mag = self.ui.sqlresults.text()
            db = pymysql.connect(host='localhost', user='root', password='164820', charset='utf8mb4',database='mydatabase')
            cur = db.cursor()
            if mag != "all":
                cur.execute(f"select license , car_type , car_place ,car_color ,time from data where {self.img} like '%{mag}%'")
                self.ui.Identify_results.setText(f'您查询的类型为“{self.ty}”，查询的内容为“{mag}”')
            else:
                cur.execute("select license , car_type , car_color , car_place ,time from data")
                self.ui.Identify_results.setText(f'您查询了数据库的所有内容')
        except:
            self.ui.Identify_results.setText("请您先选择要查询的类型，完成选择以后在按下Enter或“查找车牌”按钮进行查询")
            self.ui.sqlresults.clear()
            return
        resu = cur.fetchall()

        if not resu:
            self.ui.Identify_results.setText("输入数据有误，请检查输入数据")
        else:
            row = cur.rowcount
            vol = len(resu[0])
            # print(resu)
            self.write_table(resu, row, vol)
            self.ui.sqlresults.clear()
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
                shutil.rmtree('../../test/temp')
                os.mkdir('../../test/temp')
                for file in images_file:
                    shutil.copy(file, '../../test/temp')
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
                shutil.rmtree('../../test/temp')
                os.mkdir('../../test/temp')
                # 复制图片到缓存文件夹中
                shutil.copy(images_file[0], '../../test/temp')
                self.ui.Identify_results.setText('图片导入成功！\n点击“开始识别”启动系统。')
                print('导入图片', '  ', images_file)
        else:
            self.ui.Identify_results.setText('取消识别')
            print('取消导入图片')

    # 导入视频并开始识别
    def shipin(self):
        print('选择视频')
        # 显示框清屏
        self.ui.Original.setPixmap(QtGui.QPixmap('CQJTU.png'))
        self.ui.Identify_results.setText('视频识别启动中，请等待...')
        video_file, video_type = QFileDialog.getOpenFileNames(None, "选择你要上传的视频", '../test',filter="视频类型 (*.MP4);;视频类型(*.mkv)")
        # print(video_file,video_type)
        # self.Identify_results.clear()
        if video_file:
            video_path, video_name = os.path.split(video_file[0])
            # 显示文件名
            self.ui.name.setText(video_name)
            # 显示文件路径
            self.ui.location.setText(video_path)
            print('开始识别视频')
            cmd = 'python detect_rec_plate.py --video {}'
            run(cmd.format(video_file[0]), shell=True)
            self.show_table()
            self.ui.Identify_results.setText('视频识别完成，请点击“打开识别路径”查看识别结果。')
            print("识别完成~")
        else:
            self.ui.Identify_results.setText('取消识别')
            print('取消视频识别')

    # 开始识别图片
    def kaishi(self):
        print('开始识别')
        self.ui.Identify_results.setText('识别中，请等待...')
        cmd = 'python detect_rec_plate.py --source ../test/temp'
        run(cmd, shell=True)
        self.show_table()
        # 显示结果图片
        img = os.listdir('../../test/temp')
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
    stats = Stats()
    stats.ui.show()  # 显示主窗体
    sys.exit(App.exec_())  # 循环中等待退出程序


