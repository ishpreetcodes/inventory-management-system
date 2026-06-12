from tkinter import *
from tkinter import ttk
import tkinter.font as f
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql
import customtkinter as ctk
import product
from employee import connect_database
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
global tp_button
global tp_button, ls_button, os_button, s_button
global valuelabel, reclabel, unflabel, backimage


def kpi_values():
      global ls_button, os_button, s_button, reclabel, unflabel
      try:  
        connection= pymysql.connect(host= "localhost", user= "root",password= "tiger", port= 3306)
        global cursor
        cursor=connection.cursor()
    
        cursor.execute("USE inventory_system")
        cursor.execute(" SELECT COUNT(*) from product_data")
        total_products= cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) from product_data WHERE quantity>0 and quantity<15")
        
        low_stock=cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) from product_data WHERE quantity=0")
        
        outof_stock= cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) from supplier_data")
        total_supplier= cursor.fetchone()[0]

        cursor.execute("SELECT SUM(quantity * price) from product_data")
        stock_value_raw = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(quantity * price) from product_data WHERE status = 'Active'")
        received_raw = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(quantity * price) from product_data WHERE status = 'Inactive'")
        unfulfilled_raw = cursor.fetchone()[0]

        in_stock = total_products - outof_stock
        if in_stock < 0: in_stock = 0

        

        if stock_value_raw is None:
            stock_value_raw = 0.0

        if received_raw is None:
            received_raw = 0.0

        if unfulfilled_raw  is None:
            unfulfilled_raw  = 0.0

        formatted_value = f"${stock_value_raw:,.2f}"
        formattedd_value = f"${received_raw:,.2f}"
        formatteddd_value = f"${unfulfilled_raw:,.2f}"
        global tp_button
        tp_button.config(text=f"Total Products\n[ {total_products}]")
        ls_button.config(text=f"Low Stock\n[{low_stock}]")
        os_button.config(text=f"Out Of Stock\n[ {outof_stock}]")
        s_button.config(text=f"Total Suppliers\n[ {total_supplier}]")
        valuelabel.config(text=formatted_value)
        reclabel.config(text=f"Active Stock\n[ {formattedd_value}]")
        unflabel.config(text=f"Inactive Stock\n[ {formatteddd_value}]")

      
        

      except Exception as e :
        print(f"Dashboard query error : {e}")
    
      finally :
        return (outof_stock,low_stock, in_stock)
        cursor.close()
        connection.close()
def show_metric_details(title, detail_text):
    messagebox.showinfo(title, detail_text)
def sales_form(frame2):
    
    global backimage
    global valuelabel
    global reclabel, unflabel
    global kpi_values
    (outof_stock,low_stock, in_stock)=kpi_values()

    in_stock= total_products- outof_stock
    

    salesframe= Frame(frame2,height= 660, width= 1200, bg="white")
    salesframe.place(x=200, y=165)
    backimage= PhotoImage(file="backimage.png")
    back_button=Button(salesframe, image=backimage,bg="#f2f4f7", bd=0, cursor="hand2", command= lambda:salesframe.place_forget())
    back_button.place(x=10,y=10)


    headingglabel= Label(salesframe,text= "Dashboard", fg="white", font=("Times new roman", 20), bg="#01082d")
    headingglabel.place(x=0,y=0, relwidth=1)

    topframe=Frame(salesframe, height=200, width=1200, bg="#010c48")
    topframe.place(x=5,y=40)
                                               
    leftframe=Frame(salesframe, height=600, width=200, bg="#010c48")
    leftframe.place(x=5,y=245)

    rightframe= Frame(salesframe, height=600, width=1200, bg="#010c48")
    rightframe.place(x=210, y=245)

    fig, ax = plt.subplots(figsize=(4,3))
    categories=["Out of Stock","Low Stock","In Stock"]
    pie=[out_of_stock,low_stock,in_stock]
    ax.pie(pie, labels=categories, autopct='%1.1f%%', startangle=90, colors=['#2ecc71', '#e74c3c', '#f1c40f'])

    canvas = FigureCanvasTkAgg(fig, master=rightframe)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=BOTH, expand=True)

    # Render chart
    canvas.draw()
    

    text= "Inventory"
    spaced_text = " ".join(text)
    headinggglabel= Label(topframe,text=spaced_text, fg="white", font=("Montserrat", 30, "bold"), bg="#010c48")
    headinggglabel.place(x=12,y=0)

    headingzlabel= Label(topframe,text="Dashboard", fg="white", font=("Times new roman", 15), bg="#010c48")
    headingzlabel.place(x=40,y=40)

    tp_icon= PhotoImage(file="tp_icon.png")
    global tp_button
    tp_button= Button(topframe, image= tp_icon, compound= LEFT, text="Total Products",font= ("Times New Roman", 23, "bold"), bg= "white", fg= "#010c48", anchor= "nw", padx=10, height=100, width=240, command= lambda: show_metric_details("Total Products", "This shows the total variety of items registered in your inventory system database"))
    tp_button.image=tp_icon
    tp_button.place(x=16,y=72)

    ls_icon= PhotoImage(file="tp_icon.png")
    global ls_button
    ls_button= Button(topframe, image= tp_icon, compound= LEFT, text= "Low Stock", font= ("Times New Roman", 23, "bold"), bg= "white", fg= "#010c48", anchor= "nw", padx=10, height=100, width=240, command= lambda: show_metric_details("Low Stock Warning!", "Attention! These items have a remaining stock quantity between 1 and 14 items. Please restock soon." ))
    ls_button.image=tp_icon
    ls_button.place(x=300,y=72)

    os_icon= PhotoImage(file="tp_icon.png")
    global os_button
    os_button= Button(topframe, image= tp_icon, compound= LEFT, text= "Out Of Stock", font= ("Times New Roman", 23, "bold"), bg= "white", fg= "#010c48", anchor= "nw", padx=10, height=100, width=240,command= lambda: show_metric_details( "Critical: Out of Stock", "Warning! These items have exactly 0 stock count available. Customers cannot buy these items until updated." ))
    os_button.image=tp_icon
    os_button.place(x=584,y=72)

    s_icon= PhotoImage(file="tp_icon.png")
    global s_button
    s_button= Button(topframe, image= tp_icon, compound= LEFT, text= "Suppliers", font= ("Times New Roman", 23, "bold"), bg= "white", fg= "#010c48", anchor= "nw", padx=10, height=100, width=240, command= lambda: show_metric_details("Active Suppliers", "This counts all individual supply companies and distributors connected to your enterprise ledger."))
    s_button.image=tp_icon
    s_button.place(x=868,y=72)

    headinggzlabel= Label(leftframe,text="Value Of Stock", fg="white", font=("Times new roman", 18, "bold"),bg="#010c48")
    headinggzlabel.place(x=25,y=30)

    valuelabel= Label(leftframe,text="", fg="white", font=("Segoe UI", 20),bg="#010c48")
    valuelabel.place(x=35,y=70)

    div_line = Frame(leftframe, height=2, width=180, bg="white", bd=0, highlightthickness=0)
    div_line.place(x=10, y=140)

    stocklabel= Label(leftframe,text="Stock Purchases", fg="white", font=("Segoe UI", 18, "bold"),bg="#010c48")
    stocklabel.place(x=10,y=160)

    reclabel= Label(leftframe,text="Received", fg="white", font=("Times new roman", 15),bg="#010c48", anchor= "nw")
    reclabel.place(x=45,y=200)

    unflabel= Label(leftframe,text="Unfulfilled", fg="white", font=("Times new roman", 15),bg="#010c48", anchor= "nw")
    unflabel.place(x=45,y=250)

    kpi_values()












    

  from tkinter import *
from tkinter import ttk
import tkinter.font as f
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql
import customtkinter as ctk
import product
from employee import connect_database
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
global tp_button
global tp_button, ls_button, os_button, s_button
global valuelabel, reclabel, unflabel, backimage


def kpi_values():
      global ls_button, os_button, s_button, reclabel, unflabel
      try:  
        connection= pymysql.connect(host= "localhost", user= "root",password= "tiger", port= 3306)
        global cursor
        cursor=connection.cursor()
    
        cursor.execute("USE inventory_system")
        cursor.execute(" SELECT COUNT(*) from product_data")
        total_products= cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) from product_data WHERE quantity>0 and quantity<15")
        
        low_stock=cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) from product_data WHERE quantity=0")
        
        outof_stock= cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) from supplier_data")
        total_supplier= cursor.fetchone()[0]

        cursor.execute("SELECT SUM(quantity * price) from product_data")
        stock_value_raw = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(quantity * price) from product_data WHERE status = 'Active'")
        received_raw = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(quantity * price) from product_data WHERE status = 'Inactive'")
        unfulfilled_raw = cursor.fetchone()[0]

        in_stock = total_products - outof_stock
        if in_stock < 0: in_stock = 0

        

        if stock_value_raw is None:
            stock_value_raw = 0.0

        if received_raw is None:
            received_raw = 0.0

        if unfulfilled_raw  is None:
            unfulfilled_raw  = 0.0

        formatted_value = f"${stock_value_raw:,.2f}"
        formattedd_value = f"${received_raw:,.2f}"
        formatteddd_value = f"${unfulfilled_raw:,.2f}"
        global tp_button
        tp_button.config(text=f"Total Products\n[ {total_products}]")
        ls_button.config(text=f"Low Stock\n[{low_stock}]")
        os_button.config(text=f"Out Of Stock\n[ {outof_stock}]")
        s_button.config(text=f"Total Suppliers\n[ {total_supplier}]")
        valuelabel.config(text=formatted_value)
        reclabel.config(text=f"Active Stock\n[ {formattedd_value}]")
        unflabel.config(text=f"Inactive Stock\n[ {formatteddd_value}]")

      
        

      except Exception as e :
        print(f"Dashboard query error : {e}")
    
      finally :
        return (outof_stock,low_stock, in_stock)
        cursor.close()
        connection.close()
def show_metric_details(title, detail_text):
    messagebox.showinfo(title, detail_text)
def sales_form(frame2):
    
    global backimage
    global valuelabel
    global reclabel, unflabel
    global kpi_values
    (outof_stock,low_stock, in_stock)=kpi_values()

    in_stock= total_products- outof_stock
    

    salesframe= Frame(frame2,height= 660, width= 1200, bg="white")
    salesframe.place(x=200, y=165)
    backimage= PhotoImage(file="backimage.png")
    back_button=Button(salesframe, image=backimage,bg="#f2f4f7", bd=0, cursor="hand2", command= lambda:salesframe.place_forget())
    back_button.place(x=10,y=10)


    headingglabel= Label(salesframe,text= "Dashboard", fg="white", font=("Times new roman", 20), bg="#01082d")
    headingglabel.place(x=0,y=0, relwidth=1)

    topframe=Frame(salesframe, height=200, width=1200, bg="#010c48")
    topframe.place(x=5,y=40)
                                               
    leftframe=Frame(salesframe, height=600, width=200, bg="#010c48")
    leftframe.place(x=5,y=245)

    rightframe= Frame(salesframe, height=600, width=1200, bg="#010c48")
    rightframe.place(x=210, y=245)

    fig, ax = plt.subplots(figsize=(4,3))
    categories=["Out of Stock","Low Stock","In Stock"]
    pie=[out_of_stock,low_stock,in_stock]
    ax.pie(pie, labels=categories, autopct='%1.1f%%', startangle=90, colors=['#2ecc71', '#e74c3c', '#f1c40f'])

    canvas = FigureCanvasTkAgg(fig, master=rightframe)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=BOTH, expand=True)

    # Render chart
    canvas.draw()
    

    text= "Inventory"
    spaced_text = " ".join(text)
    headinggglabel= Label(topframe,text=spaced_text, fg="white", font=("Montserrat", 30, "bold"), bg="#010c48")
    headinggglabel.place(x=12,y=0)

    headingzlabel= Label(topframe,text="Dashboard", fg="white", font=("Times new roman", 15), bg="#010c48")
    headingzlabel.place(x=40,y=40)

    tp_icon= PhotoImage(file="tp_icon.png")
    global tp_button
    tp_button= Button(topframe, image= tp_icon, compound= LEFT, text="Total Products",font= ("Times New Roman", 23, "bold"), bg= "white", fg= "#010c48", anchor= "nw", padx=10, height=100, width=240, command= lambda: show_metric_details("Total Products", "This shows the total variety of items registered in your inventory system database"))
    tp_button.image=tp_icon
    tp_button.place(x=16,y=72)

    ls_icon= PhotoImage(file="tp_icon.png")
    global ls_button
    ls_button= Button(topframe, image= tp_icon, compound= LEFT, text= "Low Stock", font= ("Times New Roman", 23, "bold"), bg= "white", fg= "#010c48", anchor= "nw", padx=10, height=100, width=240, command= lambda: show_metric_details("Low Stock Warning!", "Attention! These items have a remaining stock quantity between 1 and 14 items. Please restock soon." ))
    ls_button.image=tp_icon
    ls_button.place(x=300,y=72)

    os_icon= PhotoImage(file="tp_icon.png")
    global os_button
    os_button= Button(topframe, image= tp_icon, compound= LEFT, text= "Out Of Stock", font= ("Times New Roman", 23, "bold"), bg= "white", fg= "#010c48", anchor= "nw", padx=10, height=100, width=240,command= lambda: show_metric_details( "Critical: Out of Stock", "Warning! These items have exactly 0 stock count available. Customers cannot buy these items until updated." ))
    os_button.image=tp_icon
    os_button.place(x=584,y=72)

    s_icon= PhotoImage(file="tp_icon.png")
    global s_button
    s_button= Button(topframe, image= tp_icon, compound= LEFT, text= "Suppliers", font= ("Times New Roman", 23, "bold"), bg= "white", fg= "#010c48", anchor= "nw", padx=10, height=100, width=240, command= lambda: show_metric_details("Active Suppliers", "This counts all individual supply companies and distributors connected to your enterprise ledger."))
    s_button.image=tp_icon
    s_button.place(x=868,y=72)

    headinggzlabel= Label(leftframe,text="Value Of Stock", fg="white", font=("Times new roman", 18, "bold"),bg="#010c48")
    headinggzlabel.place(x=25,y=30)

    valuelabel= Label(leftframe,text="", fg="white", font=("Segoe UI", 20),bg="#010c48")
    valuelabel.place(x=35,y=70)

    div_line = Frame(leftframe, height=2, width=180, bg="white", bd=0, highlightthickness=0)
    div_line.place(x=10, y=140)

    stocklabel= Label(leftframe,text="Stock Purchases", fg="white", font=("Segoe UI", 18, "bold"),bg="#010c48")
    stocklabel.place(x=10,y=160)

    reclabel= Label(leftframe,text="Received", fg="white", font=("Times new roman", 15),bg="#010c48", anchor= "nw")
    reclabel.place(x=45,y=200)

    unflabel= Label(leftframe,text="Unfulfilled", fg="white", font=("Times new roman", 15),bg="#010c48", anchor= "nw")
    unflabel.place(x=45,y=250)

    kpi_values()












    

    

    

    















    
    
  

    

    















    
    
