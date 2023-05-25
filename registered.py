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


class start:

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = uic.loadUi('UI/registered.ui')
        self.ui.registered.clicked.connect(self.registered)
        self.ui.account.returnPressed.connect(self.registered)
        self.ui.password.returnPressed.connect(self.registered)
        self.ui.confirm.returnPressed.connect(self.registered)
        self.ui.user_name.returnPressed.connect(self.registered)


    def registered(self):
        acc = self.ui.account.text()
        pwd = self.ui.password.text()
        cof = self.ui.confirm.text()
        name = self.ui.user_name.text()
        if acc and pwd and cof:
            db = pymysql.connect(host='localhost', user='root', password='164820', charset='utf8mb4',database='mydatabase')
            cur = db.cursor()
        else:
            QMessageBox.warning(self.ui, '警告', '输入内容不完整，请检查输入')
            return
        cur.execute(f"select account from user where account = '{acc}'")
        r = cur.fetchall()
        if r:
            QMessageBox.warning(self.ui, '警告', '用户已存在')
            return
        else:
            cur.execute("select max(id) from user")
            max_id = cur.fetchall()
            id_temp = int(max_id[0][0])
            if id_temp:
                start_id = id_temp+1
            else:
                start_id = 0
            if pwd == cof:
                sql = "insert into user values (%s,%s,%s,%s)"
                param = (start_id,acc,pwd,name)
                cur.execute(sql, param)
                db.commit()
                QMessageBox.information(self.ui, '恭喜', '注册成功')
            else:
                QMessageBox.critical(self.ui, '错误', '两次密码输入不正确')
                return

        cur.close()
        db.close()




if __name__ == "__main__":
    App = QApplication(sys.argv)  # 创建QApplication对象，作为GUI主程序入口
    l = start()
    l.ui.show()    # 显示主窗体
    sys.exit(App.exec_())  # 循环中等待退出程序