# -*- coding:utf-8 -*-
import os
import sys
import cv2
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from tensorflow import keras
#import keras
# from core import locate_and_correct
# from Unet import unet_predict
# from CNN import cnn_predict
from subprocess import run
import tkinter.messagebox as msgbox
import shutil

class Window:
    def __init__(self, win, ww, wh):
        print('正在启动中,请稍等...')
        self.win = win
        self.ww = ww
        self.wh = wh
        self.win.geometry("%dx%d+%d+%d" % (ww, wh, 200, 50))  # 界面启动时的初始位置
        self.win.title("车牌识别软件")
        self.img_src_path = None


        self.label_src = Label(self.win, text='处理结果:', font=('微软雅黑', 13)).place(x=0, y=0)
        self.label_lic1 = Label(self.win, text='原图:', font=('微软雅黑', 13)).place(x=615, y=0)
        self.label_pred1 = Label(self.win, text='识别结果:', font=('微软雅黑', 13)).place(x=615, y=255)
        # self.label_lic2 = Label(self.win, text='车牌区域2:', font=('微软雅黑', 13)).place(x=615, y=180)
        # self.label_pred2 = Label(self.win, text='识别结果2:', font=('微软雅黑', 13)).place(x=615, y=265)
        # self.label_lic3 = Label(self.win, text='车牌区域3:', font=('微软雅黑', 13)).place(x=615, y=360)
        # self.label_pred3 = Label(self.win, text='识别结果3:', font=('微软雅黑', 13)).place(x=615, y=445)

        self.can_src = Canvas(self.win, width=512, height=512, bg='white', relief='solid', borderwidth=1)  # 原图画布
        self.can_src.place(x=85, y=0)
        self.can_lic1 = Canvas(self.win, width=245, height=205, bg='white', relief='solid', borderwidth=1)  # 车牌区域1画布
        self.can_lic1.place(x=710, y=0)
        self.can_pred1 = Canvas(self.win, width=245, height=65, bg='white', relief='solid', borderwidth=1)  # 车牌识别1画布
        self.can_pred1.place(x=710, y=255)
        # self.can_lic2 = Canvas(self.win, width=245, height=85, bg='white', relief='solid', borderwidth=1)  # 车牌区域2画布
        # self.can_lic2.place(x=710, y=175)
        # self.can_pred2 = Canvas(self.win, width=245, height=65, bg='white', relief='solid', borderwidth=1)  # 车牌识别2画布
        # self.can_pred2.place(x=710, y=265)
        # self.can_lic3 = Canvas(self.win, width=245, height=85, bg='white', relief='solid', borderwidth=1)  # 车牌区域3画布
        # self.can_lic3.place(x=710, y=350)
        # self.can_pred3 = Canvas(self.win, width=245, height=65, bg='white', relief='solid', borderwidth=1)  # 车牌识别3画布
        # self.can_pred3.place(x=710, y=440)

        self.button1 = Button(self.win, text='选择图片', width=34, height=1, command=self.load_show_img,background='#E0B788')  # 选择文件按钮
        self.button1.place(x=710, y=355)
        self.button1 = Button(self.win, text='选择视频', width=34, height=1, command=self.load_show_video,background='#E0B788')  # 选择文件按钮
        self.button1.place(x=710, y=400)
        self.button2 = Button(self.win, text='开始识别', width=34, height=1, command=self.display,background='#E0B788')  # 识别车牌按钮
        self.button2.place(x=710, y=440)
        self.button3 = Button(self.win, text='清空所有', width=34, height=1, command=self.clear,background='#E0B788')  # 清空所有按钮
        self.button3.place(x=710, y=480)
        # self.unet = keras.models.load_model('unet.h5')
        # self.cnn = keras.models.load_model('cnn.h5')

        # cnn_predict(self.cnn, [np.zeros((80, 240, 3))])
        print("已启动,开始识别吧！")

    # def resize(self,w, h, w_box, h_box, pil_image):
    #     '''
    #     resize a pil_image object so it will fit into
    #     a box of size w_box times h_box, but retain aspect ratio
    #     对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例
    #     '''
    #     f1 = 1.0 * w_box / w  # 1.0 forces float division in Python2
    #     f2 = 1.0 * h_box / h
    #     factor = min([f1, f2])
    #     # print(f1, f2, factor) # test
    #     # use best down-sizing filter
    #     width = int(w * factor)
    #     height = int(h * factor)
    #     return pil_image.resize((width, height), Image.ANTIALIAS)


    # def load_show_img(self):
    #     self.clear()
    #     sv = StringVar()
    #     sv.set(askopenfilename())
    #     self.img_src_path = Entry(self.win, state='readonly', text=sv).get()  # 获取到所打开的图片
    #     # print(self.img_src_path)
    #     img_open = Image.open(self.img_src_path)
    #     w, h = img_open.size
    #     w_box, h_box = 245, 205
    #     img_open_resized = self.resize(w,h,w_box,h_box,img_open)
    #     # tk_image = ImageTk.PhotoImage(img_open_resized)
    #     # img_open = img_open.resize((245, 205), Image.ANTIALIAS)
    #     # if img_open.size[0] * img_open.size[1] > 240 * 80:
    #     #     img_open = img_open.resize((512, 512), Image.ANTIALIAS)
    #     self.img_Tk = ImageTk.PhotoImage(img_open_resized)
    #     self.can_lic1.create_image(125, 160, image=self.img_Tk, anchor='center')

    def load_show_img(self):
        self.clear()
        sv = StringVar()
        sv.set(askopenfilename())
        self.img_src_path = Entry(self.win, state='readonly', text=sv).get()  # 获取到所打开的图片
        # text = self.img_src_path.split('.')[1]
        text = self.img_src_path.split('.')[1]
        if text == 'mp4':
            msgbox.showwarning("温馨提示","该文件不是图片")
        else:
            shutil.copy(self.img_src_path, '/test/temp')
            img_open = Image.open(self.img_src_path)
            if img_open.size[0] * img_open.size[1] > 240 * 80:
                img_open = img_open.resize((265, 210), Image.ANTIALIAS)
            self.img_Tk = ImageTk.PhotoImage(img_open)
            self.can_lic1.create_image(122.5, 102.5, image=self.img_Tk, anchor='center')

    def load_show_video(self):
        self.clear()
        sv = StringVar()
        sv.set(askopenfilename())
        self.img_src_path = Entry(self.win, state='readonly', text=sv).get()  # 获取到所打开的图片
        text = self.img_src_path.split('.')[1]
        if text != 'mp4':
            msgbox.showwarning("温馨提示","该文件不是mp4格式视频")
        else:
            cmd = 'python E:\\Graduation\\code\\graduation_code\\detect_rec_plate.py --video {}'
            run(cmd.format(self.img_src_path), shell=True)
            print("识别成功~")
        # img_open = Image.open(self.img_src_path)
        # if img_open.size[0] * img_open.size[1] > 240 * 80:
        #     img_open = img_open.resize((265, 210), Image.ANTIALIAS)
        # self.img_Tk = ImageTk.PhotoImage(img_open)
        # self.can_lic1.create_image(122.5, 102.5, image=self.img_Tk, anchor='center')

    def display(self):
        cmd = 'python E:\\Graduation\\code\yolov7_plate-master\\detect_rec_plate.py --source E:\\Graduation\\code\\test\\temp'
        # temp(cmd.format(self.img_src_path),shell=True)
        run(cmd)
        print("识别成功~")
        shutil.rmtree('/test/temp')
        os.mkdir('/test/temp')
        image_name = self.img_src_path.split('/')[-1]
        result_path = r'/test/runout'
        image_new = Image.open(result_path+image_name)
        # if image_new.size[0] * image_new.size[1] > 240 * 80:
        img_open = image_new.resize((512, 512), Image.ANTIALIAS)
        self.img_Tk_new = ImageTk.PhotoImage(img_open)
        self.can_src.create_image(258, 258, image=self.img_Tk_new, anchor='center')
        with open(file='../../Temp.txt', mode='r', encoding='utf-8') as f:
            pre_text = f.read()
        self.can_pred1.create_text(135.5,52.5,text=pre_text,anchor='center',font=('微软雅黑', 23))

    def clear(self):
        self.can_src.delete('all')
        self.can_lic1.delete('all')
        # self.can_lic2.delete('all')
        # self.can_lic3.delete('all')
        self.can_pred1.delete('all')
        # self.can_pred2.delete('all')
        # self.can_pred3.delete('all')
        self.img_src_path = None

    def closeEvent(self):  # 关闭前清除session(),防止'NoneType' object is not callable
        keras.backend.clear_session()
        self.win.destroy()

    def on_closing(self):
        win.destroy()

if __name__ == '__main__':
    win = Tk()
    win.config(background='#395065')
    ww = 1000  # 窗口宽设定1000
    wh = 600  # 窗口高设定600
    # Window(win, ww, wh)
    win.protocol("WM_DELETE_WINDOW", Window(win, ww, wh).on_closing)
    win.mainloop()

