# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 21:58:26 2021

@author: User
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import os
import qrcode_test as qr
import palette
import cutter

class mode3(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.grab_set()
        self.wm_title('點陣填色疊圖')
        self.resizable(width=False, height=False)
        self.lift(aboveThis=None)
        
        self.frame_left=tk.Frame(self,pady=10,padx=10)
        self.frame_left.pack(side='left')
        
        self.canvas=tk.Canvas(self.frame_left,width=570,heigh=570,bg='gray')
        self.canvas.pack()
        
        self.frame=tk.Frame(self)
        self.frame.pack(side='right')
        self.frontground=None
        self.background=None
        self.locate_c=None
        self.nothing=True
        self.filename=None
        
        self.frame4=tk.Frame(self.frame,padx=10,pady=10)
        self.frame4.pack()
        self.label4=tk.Label(self.frame4,text='url')
        self.label4.pack(side='left')
        self.entry4=tk.Entry(self.frame4,width=35)
        self.entry4.pack(side='right')
        
        self.frame3=tk.Frame(self.frame,padx=10,pady=10)
        self.frame3.pack()
        self.label3=tk.Label(self.frame3,text='點陣樣式')
        self.label3.pack(side='left')
        self.combo=ttk.Combobox(self.frame3,values=["●", "★", "•", "♬", "▲", "☀", "♣", "♦", "♥",
                                                    "♠", "☯", "◆", "◉", "◒","◎","◐", "◑", "◓", 
                                                    "Ⅹ", "※", "▼", "♫", "▶"],state="readonly",width=5)
        self.combo.current(0)
        self.combo.pack(side='right')
        
        self.frame1=tk.Frame(self.frame,padx=10,pady=10)
        self.frame1.pack()
        
        
        self.loc_c = tk.Button(self.frame1,text="定位顏色",command=self.loc)
        self.loc_c.pack(side='left',padx = 10,pady = 10,ipadx = 5,ipady = 5)
        
        self.front_c = tk.Button(self.frame1,text="點陣顏色",command=self.front)
        self.front_c.pack(side='left',padx = 10,pady = 10,ipadx = 5,ipady = 5)
        
        self.back_c = tk.Button(self.frame1,text="背景顏色",command=self.back)
        self.back_c.pack(side='left',padx = 10,pady = 10,ipadx = 5,ipady = 5)
        
        
        self.frame2=tk.Frame(self.frame,padx=10,pady=10)
        self.frame2.pack()
        
        
        
        self.bg_file = tk.Button(self.frame2,text="背景圖",command=self.crop)
        self.bg_file.pack(side='left',padx = 10,pady = 10,ipadx = 5,ipady = 5)
        self.remove_bg_file = tk.Button(self.frame2,text="去除背景圖",state='disable',command=self.remove)
        self.remove_bg_file.pack(side='left',padx = 10,pady = 10,ipadx = 5,ipady = 5)
        self.mode3 = tk.Button(self.frame2,text="產生",command=self.first_step)
        self.mode3.pack(side='left',padx = 10,pady = 10,ipadx = 5,ipady = 5)
        
        self.save_but = tk.Button(self.frame2,text="儲存檔案",state='disable',command=self.save_file)
        self.save_but.pack(side='left',padx = 10,pady = 10,ipadx = 5,ipady = 5)
        
        
    def first_step(self):
        if not self.entry4.get():
            tk.messagebox.showwarning('請輸入url','請輸入url')
            return
        if self.frontground is None or self.background is None or self.locate_c is None:
            tk.messagebox.showwarning('請選擇顏色','請選擇顏色')
            return
        if not os.path.exists('data'):
            os.makedirs('data')
        qr.first_3([self.entry4.get(),self.frontground,self.background,self.locate_c,self.combo.get()])
        if self.nothing:
            self.img=ImageTk.PhotoImage(Image.open('data/dot.png').resize((570,570)))
            self.name='dot.png'
        else:
            qr.second_3(self.frontground,self.background)
            self.img=ImageTk.PhotoImage(Image.open('data/dot_pic.png').resize((570,570)))
        self.canvas.create_image(0,0, anchor=tk.NW,image = self.img)
        self.save_but.config(state='normal')
        self.grab_set()
        
        
    
        
    def crop(self):
        cut=cutter.cutter(self.filename)
        self.wait_window(cut)
        self.grab_set()
        if cut.error:
            return
        self.filename=cut.filename
        self.img=ImageTk.PhotoImage(Image.open('data/input.png'))
        self.canvas.create_image(0,0, anchor=tk.NW,image = self.img)
        self.nothing=False
        self.lift(aboveThis=None)
        self.remove_bg_file.config(state='normal')
        
        
    def remove(self):
        if self.nothing:
            return
        self.nothing=True
        if os.path.isfile('data/dot.png'):
            self.img=ImageTk.PhotoImage(Image.open('data/dot.png').resize((570,570)))
            self.canvas.create_image(0,0, anchor=tk.NW,image = self.img)
        else:
            self.canvas.delete(self.canvas.create_image(0,0, anchor=tk.NW,image = self.img))
        self.remove_bg_file.config(state='disable')
        
        
    def save_file(self):
        MsgBox = tk.messagebox.askquestion('儲存檔案','請先確認是否能掃描出內容')
        if MsgBox == 'no':
            return
        tk.messagebox.showinfo('儲存成功',cutter.save_file(self.name)+'儲存成功')
        self.save_but.config(state='disable')
        self.nothing=True
        
    def loc(self):
        self.locate_c=self.color()
        self.grab_set()
        if self.locate_c==None:
            return
        color="#%02x%02x%02x"%self.locate_c
        self.loc_c.config(bg=color)
        
        
    def back(self):
        self.background=self.color()
        self.grab_set()
        if self.background==None:
            return
        color="#%02x%02x%02x"%self.background
        self.back_c.config(bg=color)
    
    def front(self):
        self.frontground=self.color()
        self.grab_set()
        if self.frontground==None:
            return
        color="#%02x%02x%02x"%self.frontground
        self.front_c.config(bg=color)
        
        
    def color(self):
        color = palette.palette()
        self.wait_window(color)
        return color.color
            
if __name__ == '__main__':
    app=tk.Tk()
    app.wait_window(mode3())
    app.destroy()
    app.mainloop()  