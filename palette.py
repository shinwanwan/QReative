# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 13:48:28 2021

@author: User
"""

import tkinter as tk
from tkinter import messagebox
from tkinter.colorchooser import *
class palette(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.grab_set()
        self.geometry("360x360+150+150")
        self.update()
        self.x = self.winfo_x()
        self.y = self.winfo_y()
        self.var = tk.StringVar()
        self.wm_title('調色盤')
        self.color = None
        
        self.t1 = tk.Toplevel()
        self.t1.geometry("+%d+%d" %(self.x+250,self.y+100))
        
        self.t1.withdraw()
        
        self.s1 = tk.Scale(self,from_=0,to=255,length=230,command=self.updatecolor_scale,orient='horizontal')
        self.s2 = tk.Scale(self,from_=0,to=255,length=230,command=self.updatecolor_scale,orient='horizontal')
        self.s3 = tk.Scale(self,from_=0,to=255,length=230,command=self.updatecolor_scale,orient='horizontal')
        self.s1.set(255)
        self.s2.set(255)
        self.s3.set(255)
        
        self.hexs1=hex(self.s1.get()).lstrip('0x')
        self.hexs2=hex(self.s2.get()).lstrip('0x')
        self.hexs3=hex(self.s3.get()).lstrip('0x')
        self.var.set('#'+self.hexs1+self.hexs2+self.hexs3)
        self.l=tk.Label(self,text='color(16)請輸入:')
        self.e=tk.Entry(self,width=20,textvariable=self.var)
        self.e.bind('<Return>',self.updatecolor_entry)
        self.b=tk.Button(self,text='顯示調色盤',command=self.display_palette)
        self.ok=tk.Button(self,text='確定',command=self.check)
        
        
        self.s1.grid(row=0,columnspan=2,sticky='w')
        self.s2.grid(row=1,columnspan=2,sticky='w')
        self.s3.grid(row=2,columnspan=2,sticky='w')
        self.l.grid(row=3,column=0,sticky='w')
        self.e.grid(row=3,column=1,sticky='w')
        self.b.grid(row=4,column=0,sticky='w')
        self.ok.grid(row=4,column=1,sticky='w')
    
    
    def display_palette(self):
        self.t1.grab_set()
        (rgb,hx)=askcolor(parent=self.t1)
        self.t1.grab_release()
        self.grab_set()
        if not hx:
            return
        self.config(bg=hx)
        self.var.set(hx)
        
        self.h1=hx[1:3]
        self.h2=hx[3:5]
        self.h3=hx[5:7]
        self.s1.set(int(self.h1,16))
        self.s2.set(int(self.h2,16))
        self.s3.set(int(self.h3,16))
    
    def updatecolor_scale(self,args):
        red = self.s1.get()
        green = self.s2.get()
        blue = self.s3.get()
        mycolor="#%02x%02x%02x"%(red,green,blue)
        self.config(bg=mycolor)
        self.var.set(mycolor)
    
    def updatecolor_entry(self,args):
        hexcolor = self.var.get()
        if not hexcolor.startswith('#',0,1):
            messagebox.showwarning(message='請以#開始')
        if len(hexcolor) != 7:
            messagebox.showwarning(message='輸入數值在"#000000-#FFFFFF"之間')
        try:
            h1=hexcolor[1:3]
            h2=hexcolor[3:5]
            h3=hexcolor[5:7]
            self.s1.set(int(h1,16))
            self.s2.set(int(h2,16))
            self.s3.set(int(h3,16))
            self.config(bg=hexcolor)
        except:
            self.config(bg='#FFFFFF')
            self.s1.set(255)
            self.s2.set(255)
            self.s3.set(255)
            
    def check(self):
        self.color = self.s1.get(),self.s2.get(),self.s3.get()
        self.destroy()
    
