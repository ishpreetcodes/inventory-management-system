from tkinter import *
from tkinter import ttk
import tkinter.font as f
from tkinter import messagebox
from tkcalendar import DateEntry
from dashboard import frame2


def left_frame():
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
    empl_button= Button(left_frame, image= empl_icon, compound= LEFT, text= "Employee", font= ("Segou UI", 18), bg= "white", fg= "#111827", anchor= "w", padx=10, command= employee.employee_frame)
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


left_frame()
