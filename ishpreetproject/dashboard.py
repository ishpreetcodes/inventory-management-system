from tkinter import *
from tkinter import ttk
import tkinter.font as f
from tkinter import messagebox
from tkcalendar import DateEntry
import employee
import supplier
import category
import product
import sales
import pymysql


      

def dashboard():
    global frame2
    dashboardd= Toplevel()
    connection = pymysql.connect(host="localhost", user="root", password="tiger", port=3306)
    cursor = connection.cursor()
    
    cursor.execute("USE inventory_system")
    
    frame2= Frame(dashboardd, height=1000, width=2000, bd=10, background="white")
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
    empl_button= Button(left_frame, image= empl_icon, compound= LEFT, text= "Employee", font= ("Segou UI", 18), bg= "white", fg= "#111827", anchor= "w", padx=10,command=lambda :employee.employee_frame(frame2))
    empl_button.image=empl_icon
    empl_button.pack(fill= X)

    sup_icon= PhotoImage(file="supplier.png")
    sup_button= Button(left_frame, image= sup_icon, compound= LEFT, text= "Supplier", font= ("Segou UI", 18), bg= "white", fg= "#111827", anchor= "w", padx=10, command=lambda :supplier.supplier_form(frame2))
    sup_button.image=sup_icon
    sup_button.pack(fill= X)
    
    cat_icon= PhotoImage(file="categorization.png")
    cat_button= Button(left_frame, image= cat_icon, compound= LEFT, text= "Category", font= ("Segou UI", 18), bg= "white", fg= "#111827", anchor= "w", padx=10,command=lambda :category.category_form(frame2))
    cat_button.image=cat_icon
    cat_button.pack(fill= X)
    
    prod_icon= PhotoImage(file="product.png")
    prod_button= Button(left_frame, image= prod_icon, compound= LEFT, text= "Product", font= ("Segou UI", 18), bg= "white", fg= "#111827", anchor= "w", padx=10,command=lambda : product.product_form(frame2))
    prod_button.image=prod_icon
    prod_button.pack(fill= X)

    sale_icon= PhotoImage(file="sales.png")
    sale_button= Button(left_frame, image= sale_icon, compound= LEFT, text= "Dashboard", font= ("Segou UI", 18), bg= "white", fg= "#111827", anchor= "w", padx=10, command= lambda : sales.sales_form(frame2))
    sale_button.image=sale_icon
    sale_button.pack(fill= X)


    exit_icon= PhotoImage(file="exit.png")
    exit_button= Button( left_frame, image= exit_icon, compound= LEFT, text= "Exit", font= ("Segou UI", 18), bg= "white", fg= "#111827", anchor= "w", padx=10, command= dashboardd.destroy)
    exit_button.image=exit_icon
    exit_button.pack(fill= X)

    cursor.execute("SELECT COUNT(*) from employee_data")
    noofemployees= cursor.fetchone()[0]

    empframe= Frame(frame2, bg="white", bd=3, relief= RIDGE)
    empframe.place(x=300, y=200, height= 170, width= 280)
    empicon=PhotoImage(file="employeeframe.png")
    empiconn=Label(empframe,image=empicon)
    empiconn.pack()
    emplabel= Label(empframe, text= "Total Employees", bg= "white", fg="#1f2937", font=("Segou UI", 20, "bold"))
    emplabel.pack()
    emp_count= Label(empframe, text= noofemployees, bg= "white", fg="#1f2937", font=("Segou UI", 17, "bold"))
    emp_count.pack()
    empiconn.image=empicon

    cursor.execute("SELECT COUNT(*) from supplier_data")
    noofsuppliers= cursor.fetchone()[0]

    supframe= Frame(frame2, bg="white", bd=3, relief= RIDGE)
    supframe.place(x=600, y=200, height= 170, width= 280)
    supicon=PhotoImage(file="supplierframe.png")
    supiconn=Label(supframe,image=supicon)
    supiconn.pack()
    suplabel= Label(supframe, text= "Total Suppliers", bg= "white", fg="#1f2937", font=("Segou UI", 20, "bold"))
    suplabel.pack()
    sup_count= Label(supframe, text= noofsuppliers , bg= "white", fg="#1f2937", font=("Segou UI", 17, "bold"))
    sup_count.pack()
    supiconn.image=supicon

    cursor.execute("SELECT COUNT(*) from category_data")
    noofcategories= cursor.fetchone()[0]

    catframe= Frame(frame2, bg="white", bd=3, relief= RIDGE)
    catframe.place(x=900, y=200, height= 170, width= 280)
    caticon=PhotoImage(file="categorizationframe.png")
    caticonn=Label(catframe,image=caticon)
    caticonn.pack()
    catlabel= Label(catframe, text= "Total Categories", bg= "white", fg="#1f2937", font=("Segou UI", 20, "bold"))
    catlabel.pack()
    cat_count= Label(catframe, text= noofcategories, bg= "white", fg="#1f2937", font=("Segou UI", 17, "bold"))
    cat_count.pack()
    caticonn.image=caticon
    
    cursor.execute("SELECT COUNT(*) from product_data")
    noofproducts= cursor.fetchone()[0]

    prodframe= Frame(frame2, bg="white", bd=3, relief= RIDGE)
    prodframe.place(x=400, y=400, height= 170, width= 280)
    prodicon=PhotoImage(file="productframe.png")
    prodiconn=Label(prodframe,image=prodicon)
    prodiconn.pack()
    prodlabel= Label(prodframe, text= "Total Products", bg= "white", fg="#1f2937", font=("Segou UI", 20, "bold"))
    prodlabel.pack()
    prod_count= Label(prodframe, text= noofproducts , bg= "white", fg="#1f2937", font=("Segou UI", 17, "bold"))
    prod_count.pack()
    prodiconn.image=prodicon



    saleframe= Frame(frame2, bg="white", bd=3, relief= RIDGE)
    saleframe.place(x=700, y=400, height= 170, width= 280)
    saleicon=PhotoImage(file="salesframe.png")
    saleiconn=Label(saleframe,image=saleicon)
    saleiconn.pack()
    salelabel= Label(saleframe, text= "Dashboard", bg= "white", fg="#1f2937", font=("Segou UI", 20, "bold"))
    salelabel.pack()
    saleiconn.image=saleicon
    dashboardd.mainloop()
