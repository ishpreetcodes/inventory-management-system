from tkinter import *
from tkinter import ttk
import tkinter.font as f
import mysql.connector as ms
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql
from employees import employee_frame



try:
 con= ms.connect(host="localhost", user="root", database="inventory_management", port= 3307, password= "")
except:
    print("Error : connection unsuccessful")
else:
    print("Connection successful")


win= Tk()
win.state("zoomed")
frame2= None



#Frames
        
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


def clicked ():
    pass
top= None
tree= None


def clicked():
    n="i"
    p="1"
    namee= Name.get()
    passs= Pass.get()

    if(namee== n and passs== p):
        dashboard= Toplevel()
    else:
        messagebox.showerror("error", "wrong username or password /n Try Again")
    global frame2
    frame2= Frame(dashboard, height=1000, width=2000, bd=10, background="white")
    frame2.pack()
    bgimage= PhotoImage(file= "inventory-management.png")
    title= Label(frame2, image= bgimage,compound= RIGHT, text= "Inventory Management System", font= ("times new roman", 40, "bold"),bg= "#010c48", fg= "white",anchor= "w",padx=20)
    title.image = bgimage

    title.place(x=0, y=0, relwidth=1)
    logoutbutton= Button(frame2, text= "logout",font= ("Times new roman", 20, "bold"))
    logoutbutton.place(x=1100, y=25)
    subtitle= Label(frame2, text= "Welcome Admin",font=("Times new roman", 20))
    subtitle.place(x=0, y=120, relwidth=1)

    left_frame= Frame(frame2, bg="#f2f4f7")
    left_frame.place(x=0,y=165,height= 555, width=200)

    logoimage= PhotoImage(file="logo.png")
    imagelabel= Label(left_frame, image= logoimage)
    imagelabel.image=logoimage
    imagelabel.pack(fill=X)

    menu_label= Label(left_frame, text= "Menu", font=("segou UI",25, "bold" ), bg="#111827", fg= "white")
    menu_label.pack(fill=X)
    #Buttons:

    empl_icon= PhotoImage(file="employee.png")
    empl_button= Button(left_frame, image= empl_icon, compound= LEFT, text= "Employee", font= ("Segou UI", 18), bg= "white", fg= "#111827", anchor= "w", padx=10, command= lambda w=win, f2=frame2: employee_frame(w, f2))
    empl_button.image=empl_icon
    empl_button.pack(fill= X)

    sup_icon= PhotoImage(file="supplier.png")
    sup_button= Button(left_frame, image= sup_icon, compound= LEFT, text= "Supplier", font= ("Segou UI", 18), bg= "white", fg= "#111827", anchor= "w", padx=10)
    sup_button.image=sup_icon
    sup_button.pack(fill= X)
    
    cat_icon= PhotoImage(file="categorization.png")
    cat_button= Button(left_frame, image= cat_icon, compound= LEFT, text= "Category", font= ("Segou UI", 18), bg= "white", fg= "#111827", anchor= "w", padx=10)
    cat_button.image=cat_icon
    cat_button.pack(fill= X)
    
    prod_icon= PhotoImage(file="product.png")
    prod_button= Button(left_frame, image= prod_icon, compound= LEFT, text= "Product", font= ("Segou UI", 18), bg= "white", fg= "#111827", anchor= "w", padx=10)
    prod_button.image=prod_icon
    prod_button.pack(fill= X)

    sale_icon= PhotoImage(file="sales.png")
    sale_button= Button(left_frame, image= sale_icon, compound= LEFT, text= "Sales", font= ("Segou UI", 18), bg= "white", fg= "#111827", anchor= "w", padx=10)
    sale_button.image=sale_icon
    sale_button.pack(fill= X)

    exit_icon= PhotoImage(file="exit.png")
    exit_button= Button(left_frame, image= exit_icon, compound= LEFT, text= "Exit", font= ("Segou UI", 18), bg= "white", fg= "#111827", anchor= "w", padx=10)
    exit_button.image=exit_icon
    exit_button.pack(fill= X)

    empframe= Frame(frame2, bg="white", bd=3, relief= RIDGE)
    empframe.place(x=300, y=200, height= 170, width= 280)
    empicon=PhotoImage(file="employeeframe.png")
    empiconn=Label(empframe,image=empicon)
    empiconn.pack()
    emplabel= Label(empframe, text= "Total Employees", bg= "white", fg="#1f2937", font=("Segou UI", 20, "bold"))
    emplabel.pack()
    emp_count= Label(empframe, text= 0, bg= "white", fg="#1f2937", font=("Segou UI", 17, "bold"))
    emp_count.pack()
    empiconn.image=empicon

    supframe= Frame(frame2, bg="white", bd=3, relief= RIDGE)
    supframe.place(x=600, y=200, height= 170, width= 280)
    supicon=PhotoImage(file="supplierframe.png")
    supiconn=Label(supframe,image=supicon)
    supiconn.pack()
    suplabel= Label(supframe, text= "Total Suppliers", bg= "white", fg="#1f2937", font=("Segou UI", 20, "bold"))
    suplabel.pack()
    sup_count= Label(supframe, text= 0, bg= "white", fg="#1f2937", font=("Segou UI", 17, "bold"))
    sup_count.pack()
    supiconn.image=supicon

    catframe= Frame(frame2, bg="white", bd=3, relief= RIDGE)
    catframe.place(x=900, y=200, height= 170, width= 280)
    caticon=PhotoImage(file="categorizationframe.png")
    caticonn=Label(catframe,image=caticon)
    caticonn.pack()
    catlabel= Label(catframe, text= "Total Categories", bg= "white", fg="#1f2937", font=("Segou UI", 20, "bold"))
    catlabel.pack()
    cat_count= Label(catframe, text= 0, bg= "white", fg="#1f2937", font=("Segou UI", 17, "bold"))
    cat_count.pack()
    caticonn.image=caticon


    prodframe= Frame(frame2, bg="white", bd=3, relief= RIDGE)
    prodframe.place(x=400, y=400, height= 170, width= 280)
    prodicon=PhotoImage(file="productframe.png")
    prodiconn=Label(prodframe,image=prodicon)
    prodiconn.pack()
    prodlabel= Label(prodframe, text= "Total Products", bg= "white", fg="#1f2937", font=("Segou UI", 20, "bold"))
    prodlabel.pack()
    prod_count= Label(prodframe, text= 0, bg= "white", fg="#1f2937", font=("Segou UI", 17, "bold"))
    prod_count.pack()
    prodiconn.image=prodicon



    saleframe= Frame(frame2, bg="white", bd=3, relief= RIDGE)
    saleframe.place(x=700, y=400, height= 170, width= 280)
    saleicon=PhotoImage(file="salesframe.png")
    saleiconn=Label(saleframe,image=saleicon)
    saleiconn.pack()
    salelabel= Label(saleframe, text= "Total Sales", bg= "white", fg="#1f2937", font=("Segou UI", 20, "bold"))
    salelabel.pack()
    sale_count= Label(saleframe, text= 0, bg= "white", fg="#1f2937", font=("Segou UI", 17, "bold"))
    sale_count.pack()
    saleiconn.image=saleicon
    
        
bt= Button(frame1, text= "Login", width=20, command= clicked,font= font2)
bt.place(x=550, y=600)











