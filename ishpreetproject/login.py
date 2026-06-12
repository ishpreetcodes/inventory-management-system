from tkinter import *
from tkinter import ttk
import tkinter.font as f
from tkinter import messagebox
from tkcalendar import DateEntry




win= Tk()
win.state("zoomed")


frame1=Frame(win, height=900, width=1400, bd=5, bg= "#f2f4f7")
frame1.pack(padx=20, pady=20)

font1=f.Font(family= "segou ui",size=30,weight= "bold")
label= Label(frame1, text= "LOGIN WINDOW", font= font1,  fg="#4b5563")
label.place(x=450,y=100)

font2= f.Font(family="segou ui", size=15, weight= "normal",slant="italic", underline=1)
label= Label(frame1, text= "Login to your Inventory System. ", font= font2,  fg="#4b5563")
label.place(x=470,y=170)

font3= f.Font(family="helvetica", size=12, weight="normal")


label1= Label(frame1, text="Username:", fg="#4b5563", font=font1)
label1.place(x=180,y=250)
name=StringVar()
Name= Entry(frame1, width=50, textvariable=name, font=font3)
Name.place(x=600, y=270)

label2= Label(frame1, text= "Password:", fg="#4b5563", font=font1)
label2.place(x=180, y=450)

password= StringVar()
Pass=Entry(frame1, width=50, textvariable= password, font=font3)
Pass.place(x=600, y=470)


def clicked():
    n="i"
    p="1"
    namee= Name.get()
    passs= Pass.get()

    if(namee== n and passs== p):
       import dashboard
       dashboard.dashboard()
    else:
        messagebox.showerror("error", "wrong username or password /n Try Again")

bt= Button(frame1, text= "Login", width=20, command= clicked,font= font2)
bt.place(x=550, y=600)


                             
