from tkinter import *
from tkinter import ttk
import tkinter.font as f
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql



'''
try:
 con= ms.connect(host="localhost", user="root", database="inventory_management", port= 3307, password= "")
except:
    print("Error : connection unsuccessful")
else:
    print("Connection successful")'''


win= Tk()
win.state("zoomed")

def connect_database():
  try:
   connection= pymysql.connect(host= "localhost", user= "root",password= "", port= 3307)
   cursor=connection.cursor()
   cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
   cursor.execute("USE inventory_system")
   cursor.execute("""
   CREATE TABLE IF NOT EXISTS employee_data(
   empid INT Primary key,name VARCHAR(100),
   email VARCHAR(100), gender VARCHAR(50),
   dob VARCHAR(50),contacts INT(10) ,
   employmenttype VARCHAR(20), address VARCHAR(100),
   doj VARCHAR(100),education VARCHAR(20),
   workshift VARCHAR(20),salary INT(20),
   usertype VARCHAR(30), password INT(10))""")
  except:
      messagebox.showerror("ERROR", "Database Connectivity Issue, try again.")
  else:
      messagebox.showinfo("Message", "Connection successful",parent= win)
      
      

def employee_frame():
        global frame2
        global backimage
        global font3
        global font1
        employeeframe= Frame(frame2,height= 500, width= 1070)
        employeeframe.place(x=200, y=165)
        headinglabel= Label(employeeframe,text= "Managing Employee Details", fg="white", font=("Times new roman", 20), bg="#01082d")
        headinglabel.place(x=0,y=0,relwidth=1)
        backimage= PhotoImage(file="backimage.png")
        back_button=Button(employeeframe, image=backimage,bg="#f2f4f7", bd=0, cursor="hand2", command= lambda:employeeframe.place_forget())
        back_button.place(x=0,y=0)
        top_frame= Frame(employeeframe, bg="white")
        top_frame.place(x=0, y=60, relwidth=1, height=230)
        search_frame= Frame(top_frame)
        search_frame.pack()
        searchframe= ttk.Combobox(search_frame, values=("Id", "Name", "Email"), font=("helvetica",12), state="readonly")
        searchframe.set("Search By")
        searchframe.grid(row=0, column=0, padx=20)
        search_entry= Entry(search_frame, font=("helvetica",12), bg="lightblue")
        search_entry.grid(row=0, column=1)
        searchbutton= Button(search_frame, text= "SEARCH", font=("segou UI", 12),width=10, cursor= "hand2",fg="white", bg="#01082d")
        searchbutton.grid(row=0, column=2, padx=20)
        showallbutton= Button(search_frame, text= "Show All", font=("segou UI", 12), width=10, cursor= "hand2",fg="white", bg="#01082d")
        showallbutton.grid(row=0, column=3, padx=20)

        hscroll= Scrollbar(top_frame, orient=HORIZONTAL)
        vscroll= Scrollbar(top_frame, orient=VERTICAL)

        employee_treeview= ttk.Treeview(top_frame, columns= ("empid", "name", "email", "gender", "dob", "contacts", "employmenttype","address", "doj", "education", "workshift","salary", "usertype"), show= "headings", yscrollcommand="vscroll.set", xscrollcommand="hscroll.set")
        hscroll.pack(side=BOTTOM, fill= X)
        vscroll.pack(side=RIGHT, fill= Y, pady=(10,0))
        hscroll.config(command=employee_treeview.xview)
        vscroll.config(command=employee_treeview.yview)
        employee_treeview.pack(pady=(0,10))
        
        employee_treeview.heading("empid", text= "Employee Id")
        employee_treeview.heading("name", text= "Name")
        employee_treeview.heading("email", text= "E-mail")
        employee_treeview.heading("gender", text= "Gender")
        employee_treeview.heading("dob", text= "DOB")
        employee_treeview.heading("contacts", text= "Contact")
        employee_treeview.heading("employmenttype", text= "Employement Type")
        employee_treeview.heading("address", text= "Address")
        employee_treeview.heading("doj", text= "DOJ")
        employee_treeview.heading("salary", text= "Salary")
        employee_treeview.heading("usertype", text= "User Type")
        employee_treeview.heading("workshift", text= "Work Shift")
        employee_treeview.heading("education", text= "Education")

        font4= f.Font(family="helvetica",size=10)

        detail_frame= Frame(employeeframe, height=1500, width=1000,bg= "white")
        detail_frame.place(x=100, y=300)

        
        empid_label=Label(detail_frame, text= "EmpId",font=font4)
        empid_label.grid(row=0, column=0, padx=20, pady=10)
        empid_entry= Entry(detail_frame, font=font4, bg="lightblue")
        empid_entry.grid(row=0, column=1,padx=10, pady=10)

        name_label=Label(detail_frame, text= "Name",font=font4)
        name_label.grid(row=0, column=2,padx=20, pady=10)
        name_entry= Entry(detail_frame, font=font4, bg= "lightblue")
        name_entry.grid(row=0, column=3, padx=10, pady=10)

    
        email_label=Label(detail_frame, text= "E-Mail",font=font4)
        email_label.grid(row=0, column=4, pady=10, padx=10)
        email_entry= Entry(detail_frame, font=font4, bg= "lightblue")
        email_entry.grid(row=0, column=5, pady=10, padx=10)

        gender_label=Label(detail_frame, text= "Gender",font=font4)
        gender_label.grid(row=1, column=0, pady=10, padx=10)

        gender_combobox= ttk.Combobox(detail_frame, values=("male", "female"), font= font4, width=18, state= "readonly")
        gender_combobox.set("Select Gender")
        gender_combobox.grid(row=1, column=1,pady=10, padx=10)

        dob_label=Label(detail_frame, text= "Date Of Birth",font=font4)
        dob_label.grid(row=1, column=4, pady=10, padx=10)
        dob_date_entry= DateEntry(detail_frame, width=18, font=font4, state= "readonly",date_pattern="dd/mm/yyyy")
        dob_date_entry.grid(row=1, column=5, pady=10, padx=10)

        contact_label=Label(detail_frame, text= "Contact",font=font4)
        contact_label.grid(row=3, column=2, pady=10, padx=10)
        contact_entry= Entry(detail_frame, font=font4, bg= "lightblue")
        contact_entry.grid(row=3, column=3, pady=10, padx=10)

        emptype_label=Label(detail_frame, text= "Employement Type",font=font4)
        emptype_label.grid(row=2, column=0, pady=10, padx=10)
        emptype_combobox= ttk.Combobox(detail_frame, values=("Full Time", "Part Time", "Intern"), font= font4, width=18, state= "readonly")
        emptype_combobox.set("Employement Type")
        emptype_combobox.grid(row=2, column=1, pady=10, padx=10)

        Education_label=Label(detail_frame, text= "Education",font=font4)
        Education_label.grid(row=2, column=2, pady=10, padx=10)
        Education_combobox= ttk.Combobox(detail_frame, values=("M.Com", "B.Com", "Bba", "Mba", "B.a", "M.a","Other"), font= font4, width=18, state= "readonly")
        Education_combobox.set("Select Education")
        Education_combobox.grid(row=2, column=3, pady=10, padx=10)

        Work_Shift_label=Label(detail_frame, text= "Work Shift",font=font4)
        Work_Shift_label.grid(row=2, column=4, pady=10, padx=10)
        Work_Shift_combobox= ttk.Combobox(detail_frame, values=("Morning", "Evening", "Night"), font= font4, width=18, state= "readonly")
        Work_Shift_combobox.set("Select Work Shift")
        Work_Shift_combobox.grid(row=2, column=5, pady=10, padx=10)

        Address_label=Label(detail_frame, text= "Address",font=font4)
        Address_label.grid(row=3, column=0, pady=10, padx=20)
        Address_text= Text(detail_frame,width=20, height=3, font= font4)
        Address_text.grid(row=3, column=1, pady=10, padx=10, rowspan=2)

        Doj_label=Label(detail_frame, text= "Date of Joining",font=font4)
        Doj_label.grid(row=1, column=2, pady=10, padx=10)
        Doj_date= DateEntry(detail_frame, width=18, state= "readonly",date_pattern="dd/mm/yyyy")
        Doj_date.grid(row=1, column=3, pady=10, padx=10)

        salary_label=Label(detail_frame, text= "Salary",font=font4)
        salary_label.grid(row=3, column=4, padx=10, pady=10)
        salary_entry= Entry(detail_frame, font=font4, bg="lightblue")
        salary_entry.grid(row=3, column=5,padx=10, pady=10)

        usertype_label=Label(detail_frame, text= "User Type",font=font4)
        usertype_label.grid(row=4, column=2, pady=10, padx=10)
        usertype_combobox= ttk.Combobox(detail_frame, values=("Employee", "Admin", "Member", "Guest"), font= font4, width=18, state= "readonly")
        usertype_combobox.set("Select User Type")
        usertype_combobox.grid(row=4, column=3, padx=10, pady=10)

        Pass_label=Label(detail_frame, text= "Password",font=font4)
        Pass_label.grid(row=4, column=4, padx=10, pady=10)
        Pass_entry= Entry(detail_frame, font=font4, bg="lightblue")
        Pass_entry.grid(row=4, column=5)

        button_frame=Frame(frame2, height=50, width=1270, bg="white")
        button_frame.place(x=320, y=668)
        
        add_button= Button(button_frame, text= "ADD", font=("segou UI", 11),width=15, cursor= "hand2",fg="white", bg="#01082d")
        add_button.grid(row=0, column=0, padx=30)

        update_button= Button(button_frame, text= "UPDATE", font=("segou UI", 11),width=15, cursor= "hand2",fg="white", bg="#01082d")
        update_button.grid(row=0, column=1, padx=30)
        
        delete_button= Button(button_frame, text= "DELETE", font=("segou UI", 11),width=15, cursor= "hand2",fg="white", bg="#01082d")
        delete_button.grid(row=0, column=2, padx=30)

        clear_button= Button(button_frame, text= "CLEAR", font=("segou UI", 11),width=15, cursor= "hand2",fg="white", bg="#01082d")
        clear_button.grid(row=0, column=3, padx=30)

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
    empl_button= Button(left_frame, image= empl_icon, compound= LEFT, text= "Employee", font= ("Segou UI", 18), bg= "white", fg= "#111827", anchor= "w", padx=10, command= employee_frame)
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











