# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 21:58:11 2021

@author: User
"""
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import qrcode_test as qr
import cutter


class mode2(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.grab_set()
        self.wm_title('格點分布遮色')
        self.resizable(width=False, height=False)
        self.frame_left=tk.Frame(self,pady=10,padx=10)
        self.frame_left.pack(side='left')
        
        self.canvas=tk.Canvas(self.frame_left,width=570,heigh=570,bg='gray')
        self.canvas.pack()
        self.nothing=True
        self.filename=None
        
        self.frame_right=tk.Frame(self)
        self.frame_right.pack(side='right',fill='x')
        
        
        self.frame=tk.Frame(self.frame_right,padx=10,pady=10)
        self.frame.pack(fill='x')
        self.label=tk.Label(self.frame,text='QRcode_version')
        self.label.pack(side='left')
        self.version=tk.StringVar()
        self.version.set('10')
        self.entry=tk.Entry(self.frame,textvariable=self.version)
        self.entry.pack(side='right')
        
        
        self.frame1=tk.Frame(self.frame_right,padx=10,pady=10)
        self.frame1.pack(fill='x')
        self.var1=tk.StringVar()
        self.var1.set('200')
        self.label1=tk.Label(self.frame1,text='臨界值域值')
        self.label1.pack(side='left')
        self.entry1=tk.Entry(self.frame1,textvariable=self.var1)
        self.entry1.pack(side='right')
        
        self.frame2=tk.Frame(self.frame_right,padx=10,pady=10)
        self.frame2.pack(fill='x')
        self.var2=tk.StringVar()
        self.var2.set('4')
        self.label2=tk.Label(self.frame2,text='調整強度')
        self.label2.pack(side='left')
        self.entry2=tk.Entry(self.frame2,textvariable=self.var2)
        self.entry2.pack(side='right')
        
        
        self.frame4=tk.Frame(self.frame_right,padx=10,pady=10)
        self.frame4.pack(fill='x')
        self.label4=tk.Label(self.frame4,text='url')
        self.label4.pack(side='left')
        self.entry4=tk.Entry(self.frame4,width=35)
        self.entry4.pack(side='right')
        
        self.frame5=tk.Frame(self.frame_right,padx=10,pady=10)
        self.frame5.pack()
        
        
        self.cut_but = tk.Button(self.frame5,text="選擇檔案",command=self.crop)
        self.cut_but.pack(side='left',padx = 10,pady = 10,ipadx = 5,ipady = 5)
        self.mode2 = tk.Button(self.frame5,text="確定",command=self.go)
        self.mode2.pack(side='left',padx = 10,pady = 10,ipadx = 5,ipady = 5)
        self.save_but = tk.Button(self.frame5,text="儲存檔案",state='disable',command=self.save_file)
        self.save_but.pack(side='left',padx = 10,pady = 10,ipadx = 5,ipady = 5)
        
        
    def go(self):
        self.grab_set()
        if self.check_error():
            return
        wait=tk.Toplevel()
        wait.grab_set()
        qr.init_2([int(self.version.get()),self.entry4.get(),int(self.var1.get()),int(self.var2.get())])
        wait.destroy()
        self.save_but.config(state='normal')
        self.lift(aboveThis=None)
        self.img=ImageTk.PhotoImage(Image.open('data/2_cube_dot_final.png').resize((570,570)))
        self.canvas.create_image(0,0, anchor=tk.NW,image = self.img)
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
        self.cut_but.config(relief='raised')
        self.lift(aboveThis=None)
        
    def save_file(self):
        MsgBox = tk.messagebox.askquestion('save file','請先確認是否能掃描出內容')
        if MsgBox == 'no':
            return
        
        tk.messagebox.showinfo('儲存成功',cutter.save_file('2_cube_dot_final.png')+'儲存成功')
        self.save_but.config(state='disable')
        self.nothing=True
        
        
    def check_error(self):
        if self.nothing:
            tk.messagebox.showwarning(message='請選擇檔案')
            return True
        try :
            int(self.version.get())
        except:
            tk.messagebox.showwarning(message='請輸入整數')
            return True
        
        if int(self.version.get()) <= 0 or int(self.version.get()) > 10:
            tk.messagebox.showwarning(message='請輸入0~10整數')
            return True;
        try :
            int(self.var1.get())
            int(self.var2.get())
        except:
            tk.messagebox.showwarning(message='請輸入整數')
            return True
        
        if int(self.var1.get()) < 0 or int(self.var1.get()) > 255:
            tk.messagebox.showwarning(message='請輸入0~255')
            return True;
        
        if int(self.var2.get()) < 0.5 or int(self.var2.get()) > 10:
            tk.messagebox.showwarning(message='請輸入0~10')
            return True;
        if not self.entry4.get():
            tk.messagebox.showwarning(message='請輸入url')
            return True
        
        return False
    
    
if __name__ == '__main__':
    app=tk.Tk()
    app.wait_window(mode2())
    app.destroy()
    app.mainloop()