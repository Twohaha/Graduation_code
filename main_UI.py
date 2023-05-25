# -*- coding: utf-8 -*-
import os
import sys
import pymysql
from PyQt5.QtWidgets import *
from PyQt5 import uic


class start:

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = uic.loadUi('UI/loginpage.ui')
        self.ui.login.clicked.connect(self.choose)
        self.ui.password.returnPressed.connect(self.choose)
        self.ui.account.returnPressed.connect(self.choose)
        self.ui.change.clicked.connect(self.change)
        self.ui.registered.clicked.connect(self.registered)
        self.ui.account.setPlaceholderText('请输入账号')
        self.ui.password.setPlaceholderText('请输入密码')

    def choose(self):
        acc = str(self.ui.account.text())
        pwd = str(self.ui.password.text())
        if acc:
            if pwd:
                db = pymysql.connect(host='localhost', user='root', password='164820', charset='utf8mb4',database='mydatabase')
                cur = db.cursor()
                cur.execute(f"select account,password,uer_name from user where account = '{acc}'")
                acc_list = cur.fetchall()
                # print(acc_list)
                try:
                    account = acc_list[0][0]
                    password = acc_list[0][1]
                    uer_name = acc_list[0][2]
                    # print(account, password, uer_name)
                except:
                    QMessageBox.critical(self.ui, '错误', '用户名不存在，请检查用户输入')
                    return
                cur.close()
                db.close()
                if acc == account and pwd == password:
                    login.ui.close()
                    os.system('python choose_mode.py')
                else:
                    QMessageBox.critical(self.ui, '错误', '账号或密码错误')
                    return
            else:
                QMessageBox.warning(self.ui, '警告', '请输入密码')
                return
        else:
            QMessageBox.warning(self.ui, '警告', '请输入账号')
            return

    def change(self):
        os.system('python change.py')

    def registered(self):
        os.system('python registered.py')



if __name__ == "__main__":
    App = QApplication(sys.argv)  # 创建QApplication对象，作为GUI主程序入口
    login = start()
    login.ui.show()    # 显示主窗体
    sys.exit(App.exec_())  # 循环中等待退出程序