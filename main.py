# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 22:02:07 2021

@author: User
"""
import tkinter as tk
import tkinter.font as tkFont
from PIL import Image
from PIL import ImageTk
import shutil
import mode1
import mode2
import mode3


class window:
    def __init__(self):
        self.root = tk.Tk()
        #self.setwin()
        self.root.title('QReative')
        self.setbackground()
        self.root.resizable(width=False, height=False)
        self.root.mainloop()
        
    
        
    
    
    
    
    
    def setbackground(self):
        self.root.geometry('1200x700')
        self.bg_pic = ImageTk.PhotoImage(Image.open('image/default_bg.png'))
        self.canvas=tk.Canvas(self.root, width=1200,height=720,bd=0)
        self.canvas.create_image(0, 0,anchor=tk.NW, image=self.bg_pic)
        self.canvas.pack()
    
        
        
        
        
        fontExample = tkFont.Font(family='Arial', size=16)

        self.fun1=tk.Button(bg='#4e7d7d',text="色彩疊合渲染", width=15,height=1,font=fontExample,command=mode1.mode1)
        self.fun1.pack(ipadx = 5,ipady = 5)
        self.fun1.bind("<Enter>",self.act1)
        self.fun1.bind("<Leave>",self.default)
        
        self.fun2=tk.Button(bg='#4e7d7d',text="格點分布遮色", width=15,height=1,font=fontExample,command=mode2.mode2)
        self.fun2.pack(ipadx = 5,ipady = 5)
        self.fun2.bind("<Enter>",self.act2)
        self.fun2.bind("<Leave>",self.default)
        
        self.fun3=tk.Button(bg='#4e7d7d',text="點陣填色疊圖", width=15,height=1,font=fontExample,command=mode3.mode3)
        self.fun3.pack(ipadx = 5,ipady = 5)
        self.fun3.bind("<Enter>",self.act3)
        self.fun3.bind("<Leave>",self.default)
        
        
        
        self.canvas.create_window(20, 550, anchor='nw', window=self.fun1)
        self.canvas.create_window(20, 600, anchor='nw', window=self.fun2)
        self.canvas.create_window(20, 650, anchor='nw', window=self.fun3)
        self.textwin = None
    
    
    
    
    
    
    
    
    
    def act1(self,event):
        self.fun1.config(bg='white',text='>>色彩疊合渲染', width=17)
        self.change('1')
        self.warn('彩色完整圖片\n適合風景、人物等全圖',[event.x_root,event.y_root])
    
    
    def act2(self,event):
        self.fun2.config(bg='white',text='>>格點分布遮色', width=17)
        self.change('2')
        self.warn('商標，貼圖或表情符號，各式Logo圖',[event.x_root,event.y_root])
    
    
    def act3(self,event):
        self.fun3.config(bg='white',text='>>點陣填色疊圖', width=17)
        self.change('3')
        self.warn('彩色完整圖片\n適合風景、人物等全圖',[event.x_root,event.y_root])
    
    
    def change(self,mode):
        path='image/method0'+mode+'_bg.png'
        self.bg_pic = ImageTk.PhotoImage(Image.open(path))
        self.canvas.create_image(0, 0,anchor=tk.NW, image=self.bg_pic)
        
    

    
        
    def default(self,event):
        self.win.destroy()
        self.fun1.config(bg='#4e7d7d',text='色彩疊合渲染', width=15)
        self.fun2.config(bg='#4e7d7d',text='格點分布遮色', width=15)
        self.fun3.config(bg='#4e7d7d',text='點陣填色疊圖', width=15)
        self.bg_pic = ImageTk.PhotoImage(Image.open('image/default_bg.png'))
        self.canvas.create_image(0, 0,anchor=tk.NW, image=self.bg_pic)
        
        
    def warn(self,txt,event):
        self.win=tk.Toplevel()
        x,y=event
        string='+'+str(x)+'+'+str(y)
        #print(string)
        self.win.geometry(string)
        self.win.overrideredirect(True)
        #root.attributes("-alpha", 0.3)窗口透明度70 %
        self.win.attributes("-alpha", 0.9)#窗口透明度60 %
        label = tk.Label(self.win,text=txt,bg='yellow',justify='left')
        label.pack()
        
        
def delete():
    try:
        shutil.rmtree('data')
    except:
        pass       
if __name__ == '__main__':
    window()
    delete()