# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 14:13:44 2021

@author: User
"""
import tkinter as tk
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import os

class cutter(tk.Toplevel):
    def __init__(self,path):
        super().__init__()
        self.grab_set()
        w,h = self.maxsize()
        self.geometry("{}x{}".format(w,h))
        self.wm_title("裁切圖片")
        self.nothing = True
        self.filename=path
        self.error=True
        self.sole_rectangle = None
        self.frame = tk.Frame(self) 
        self.frame.pack(pady = 10)
        self.but_frame = tk.Frame(self) 
        self.yscrollbar = tk.Scrollbar(self.frame)
        self.yscrollbar.pack(side="right", fill="y")
        self.xscrollbar = tk.Scrollbar(self.frame,orient=tk.HORIZONTAL)
        self.xscrollbar.pack(side="bottom", fill="x")

        
        self.canvas = tk.Canvas(self.frame,width=w*0.8,heigh=h*0.8,xscrollcommand=self.xscrollbar.set,yscrollcommand=self.yscrollbar.set)
        
        
        self.canvas.pack()
        self.but_frame.pack()
        self.openf = tk.Button(self.but_frame,text="選擇檔案") 
        self.savef = tk.Button(self.but_frame,text="裁切完成") 
        
        self.yscrollbar.config(command=self.canvas.yview)
        self.xscrollbar.config(command=self.canvas.xview)

        self.canvas.bind("<Button-1>",self.left_mouse_down)
        self.canvas.bind("<B1-Motion>",self.moving_mouse)
        self.canvas.bind("<ButtonRelease-1>",self.left_mouse_up)
        
        
        self.openf.bind("<Button-1>",self.openpicture)
        self.savef.bind("<Button-1>",self.Export_File)
        self.openf.pack(side = 'left',padx = 10,pady = 10,ipadx = 5,ipady = 5)
        self.savef.pack(side = 'right',padx = 10,pady = 10,ipadx = 5,ipady = 5)
        
        if path:
            self.show_pic()
 
    
    def openpicture(self, event):
        self.lift(aboveThis=None)
        temp = tk.Toplevel()
        temp.grab_set()
        temp.withdraw()
        self.filename=filedialog.askopenfilename(title='Select File',filetypes = (("png files","*.png"),("jpeg files","*.jpg"),("all files","*.*")))     #獲取文件全路徑
        temp.destroy()
        if not self.filename:
            self.lift(aboveThis=None)
            self.grab_set()
            return
        self.show_pic()
        
    def show_pic(self,):
        self.nothing = False
        self.image = Image.open(self.filename)
        self.img=ImageTk.PhotoImage(self.image)
        self.x,self.y = self.image.size
        self.left_mouse_down_x = 0
        self.left_mouse_down_y = 0
        self.left_mouse_up_x = self.x
        self.left_mouse_up_y = self.y
        scrw,scrh= self.maxsize()
        self.canvas.config(width=min(scrw*0.8,self.x),height=min(scrh*0.8,self.y),scrollregion=(0,0,self.x,self.y))
        self.canvas.create_image(0,0, anchor=tk.NW,image = self.img)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.lift(aboveThis=None)
        self.openf.config(relief='raised') 
        self.grab_set()
        
        
        
    def Export_File(self,event):
        if self.nothing:
            self.lift(aboveThis=None)
            tk.messagebox.showwarning(message='請先選擇檔案')
            return
        if not os.path.exists('data'):
            os.makedirs('data')
        filename='data\input.png'
        if self.left_mouse_down_x < self.left_mouse_up_x:
            min_x = self.left_mouse_down_x
            max_x = self.left_mouse_up_x
        else:
            min_x = self.left_mouse_up_x
            max_x = self.left_mouse_down_x
        if self.left_mouse_down_y < self.left_mouse_up_y:
            min_y = self.left_mouse_down_y
            max_y = self.left_mouse_up_y
        else:
            min_y = self.left_mouse_up_y
            max_y = self.left_mouse_down_y
        save_img = self.image.crop((min_x, min_y, max_x, max_y))
        x,y = save_img.size
        if x>570:
            y=y*570/x
            x=570
            save_img=save_img.resize((int(x),int(y)))
        if y>570:
            x=x*570/y
            y=570
            save_img=save_img.resize((int(x),int(y)))
        save_img=save_img.resize((570,570))
        save_img.save(filename)
        self.lift(aboveThis=None)
        self.error=False
        self.destroy()
        
        
        
    def left_mouse_down(self,event):
        if self.nothing:
            return
        self.b,i=self.yscrollbar.get()
        self.a,i=self.xscrollbar.get()
        
        self.left_mouse_down_x = event.x + int(self.a*self.x)
        self.left_mouse_down_y = event.y + int(self.b*self.y)
        
    def left_mouse_up(self,event):
        if self.nothing:
            return
        self.left_mouse_up_x = event.x + int(self.a*self.x)
        self.left_mouse_up_y = event.y + int(self.b*self.y)


    def moving_mouse(self,event):
        if self.nothing:
            return
        self.b,i=self.yscrollbar.get()
        self.a,i=self.xscrollbar.get()
        self.moving_mouse_x = event.x + int(self.a*self.x)
        self.moving_mouse_y = event.y + int(self.b*self.y)
        if self.sole_rectangle is not None:
            self.canvas.delete(self.sole_rectangle) # 刪除前一個矩形
        self.sole_rectangle = self.canvas.create_rectangle(self.left_mouse_down_x,self.left_mouse_down_y,self.moving_mouse_x,self.moving_mouse_y,outline='black',width=2)
        
 
    def _on_mousewheel(self, event): 
        self.canvas.yview_scroll(int(-1*event.delta/120), "units")
        
def save_file(name):
    filename = filedialog.asksaveasfile(title='Save File',filetypes = (("png files","*.png"),("jpeg files","*.jpg"),("all files","*.*")),defaultextension='.jpg')
    if not filename:
        return
    save_img = Image.open('data/'+name)
    save_img.save(filename.name)
    return filename.name[filename.name.rfind('/')+1:]
 