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
        self.ui = uic.loadUi('UI/change_password.ui')
        self.ui.confirm.clicked.connect(self.changepass)
        self.ui.confirm_password.returnPressed.connect(self.changepass)
        self.ui.account.returnPressed.connect(self.changepass)
        self.ui.old_password.returnPressed.connect(self.changepass)
        self.ui.new_password.returnPressed.connect(self.changepass)

    def changepass(self):
        acc = str(self.ui.account.text())
        old = str(self.ui.old_password.text())
        new = str(self.ui.new_password.text())
        cfm = str(self.ui.confirm_password.text())
        if acc and old and new and cfm:
            db = pymysql.connect(host='localhost', user='root', password='164820', charset='utf8mb4', database='mydatabase')
            cur = db.cursor()
        else:
            QMessageBox.critical(self.ui, '错误', '输入内容不完整，请检查输入')
            return
        cur.execute(f"select account,password,uer_name from user where account = '{acc}'")
        acc_list = cur.fetchall()
        try:
            account = acc_list[0][0]
            password = acc_list[0][1]
            uer_name = acc_list[0][2]
        except:
            QMessageBox.critical(self.ui,'错误','未找到该用户，请检查输入')
            return
        if password == old:
            if new == cfm:
                cur.execute(f"update user set password = '{new}' where account = '{acc}'")
                db.commit()
                cur.close()
                db.close()
                QMessageBox.information(self.ui, '恭喜', '密码修改成功')
            else:
                QMessageBox.warning(self.ui,'警告','两次新密码输入不正确')
                return
        else:
            QMessageBox.warning(self.ui, '警告', '原密码输入错误')
            return










if __name__ == "__main__":
    App = QApplication(sys.argv)  # 创建QApplication对象，作为GUI主程序入口
    l = start()
    l.ui.show()    # 显示主窗体
    sys.exit(App.exec_())  # 循环中等待退出程序