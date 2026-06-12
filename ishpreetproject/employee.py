from tkinter import *
from tkinter import ttk
import tkinter.font as f
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql
from datetime import datetime


def connect_database():
  
  try:
   connection= pymysql.connect(host= "localhost", user= "root",password= "tiger", port= 3306)

   global cursor
   cursor=connection.cursor()

   cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
   cursor.execute("USE inventory_system")
   cursor.execute("CREATE TABLE IF NOT EXISTS employee_data(empid INT Primary key,name VARCHAR(100),email VARCHAR(100), gender VARCHAR(50),dob VARCHAR(50),contacts VARCHAR(15) ,employmenttype VARCHAR(20),education VARCHAR(80),workshift VARCHAR(20),address VARCHAR(100),doj VARCHAR(50),salary INT(20),usertype VARCHAR(30), password INT(10))")

   return connection, cursor

  except Exception as e:
      messagebox.showerror("ERROR",f"Database Error: {e}")
      return None, None
  else:
   print("database is connected")
connect_database()

def treeview_data():
  connection, cursor = connect_database()
  if not cursor or not connection:
    return
  try:
      cursor.execute("USE inventory_system")
      cursor.execute("SELECT * from employee_data")
      employee_records= cursor.fetchall()
      employee_treeview.delete(*employee_treeview.get_children())
      for record in employee_records:
          employee_treeview.insert("", END, values= record)
          
  except Exception as e :
      messagebox.showerror('Error', f'Error Due to {e}')
  finally:
      cursor.close()
      connection.close()
    

def clear_fields(empid_entry,name_entry,email_entry,gender_combobox, dob_date_entry, contact_entry, emptype_combobox, Education_combobox,Work_Shift_combobox, Address_text,Doj_date,salary_entry,usertype_combobox,Pass_entry):
   empid_entry.delete(0, END)
   name_entry.delete(0, END)
   email_entry.delete(0, END)
   gender_combobox.set("Select Gender")
   from datetime import date
   
   dob_date_entry.set_date(date.today())
   contact_entry.delete(0, END)
   emptype_combobox.set("Select Type")
   Education_combobox.set("Select Education")
   Work_Shift_combobox.set("Select Work Shift")
   Address_text.delete(1.0, END)
   Doj_date.set_date(date.today())
   salary_entry.delete(0, END)
   usertype_combobox.set("Select Usertype")
   Pass_entry.delete(0, END)


def delete_employee(empid):
  selected= employee_treeview.selection()
  if not selected :
   messagebox.showerror("Error", "Row not selected")
  else:
    result= messagebox.askyesno("Confirm", "Do You Really Want To Delete The Record?")
    if result:
     connection, cursor = connect_database()
     if not connection or not cursor:
      return
  try:
     cursor.execute("USE inventory_system")
     cursor.execute('DELETE FROM employee_data where empid= %s', (empid,))
     connection.commit()
     treeview_data()
     messagebox.showinfo("success", "data deleted")
  except Exception as e:
    messagebox.showerror("error", f'error due to {e}')
  finally:
    connection.close()
    cursor.close()
    
def select_data(event, empid_entry, name_entry, email_entry, gender_combobox, dob_date_entry, contact_entry, emptype_combobox, Education_combobox, Work_Shift_combobox, Address_text, Doj_date, salary_entry, usertype_combobox, Pass_entry):
  index= employee_treeview.selection()
  content= employee_treeview.item(index)
  row= content['values']
  
  clear_fields(empid_entry, name_entry, email_entry, gender_combobox, dob_date_entry, contact_entry, emptype_combobox, Education_combobox, Work_Shift_combobox, Address_text, Doj_date, salary_entry, usertype_combobox, Pass_entry)

  empid_entry.insert(0, row[0])
  name_entry.insert(0, row[1])
  email_entry.insert(0, row[2])
  gender_combobox.set(row[3])
  dob_date_entry.set_date(row[4])
  contact_entry.insert(0, row[5])
  emptype_combobox.set(row[6])
  Education_combobox.set(row[7])
  Work_Shift_combobox.set(row[8])
  Address_text.insert(1.0, row[9])
  Doj_date.set_date(row[10])
  salary_entry.insert(0, row[11])
  usertype_combobox.set(row[12])
  Pass_entry.insert(0, row[13])

def update(empid,name,email, gender,dob,contacts,employmenttype,education,workshift, address,doj,salary, usertype, password):
  selected= employee_treeview.selection()
  if not selected :
   messagebox.showerror("Error", "Row not selected")
   return
  connection, cursor = connect_database()
  if not connection or not cursor:
     return
  try:
     cursor.execute("USE inventory_system")
     query= """
       UPDATE employee_data SET name= %s,email= %s, gender=%s,dob=%s,contacts=%s,
       employmenttype=%s,education=%s,workshift=%s, address=%s,
       doj=%s,salary=%s, usertype=%s, password=%s
       WHERE empid=%s
       """
     cursor.execute(query,(name,email, gender,dob,contacts,employmenttype,education,workshift, address,doj,salary, usertype, password, empid))
     
     connection.commit()
     treeview_data()
     messagebox.showinfo("Success", "Data is updated succesfully")
  except Exception as e:
    messagebox.showerror("error", f"Update failed: {e}")
  finally:
    connection.close()

def search_employee(search_option,value):
  if search_option== "Search by" :
    messagebox.showerror("Error", "No Option is Selected.")
  elif value== "" :
    messagebox.showerror("Error", "Select the value to search.")
  else:
    connection, cursor = connect_database()
    if not cursor or not connection :
      return
    try:
       cursor.execute("USE inventory_system")
       query= f"SELECT * from employee_data WHERE {search_option} LIKE %s"
       cursor.execute(query, (f"%{value}%",))
    
       records= cursor.fetchall()
       employee_treeview.delete(*employee_treeview.get_children())
       for record in records:
        employee_treeview.insert('', END, values= record)
    except Exception as e:
       messagebox.showerror("error", f"Search failed: {e}")
    finally:
       cursor.close()
       connection.close()


def show_all():
  treeview_data()

def move_next(event):
    event.widget.tk_focusNext().focus()
    return "break"
def auto_save(event,empid,name,email, gender,dob,contacts,employmenttype,education,workshift, address,doj,salary, usertype, password):
    add_employee(empid_entry.get(),name_entry.get(),email_entry.get(),gender_combobox.get(), dob_date_entry.get(), contact_entry.get(), emptype_combobox.get(), Education_combobox.get(),Work_Shift_combobox.get(), Address_text.get(1.0, END),Doj_date.get(),salary_entry.get(),usertype_combobox.get(),Pass_entry.get())
    return "break"
  
    
  
def add_employee(empid,name,email, gender,dob,contacts,employmenttype,education,workshift, address,doj,salary, usertype, password):
        if ( empid==""or name== "" or email== "" or gender== "Select Gender" or contacts== "" or employmenttype== "Employement Type" or education== "Select Education" or workshift== "Select Work Shift" or address== "\n" or salary== ""or usertype== "Select Usertype"or password== ""):
          messagebox.showerror("ERROR", "All Fields Are Required")
          return
        connection, cursor = connect_database()
        if not cursor or not connection:
          return
        
        try:
          
          cursor.execute("use inventory_system")
          cursor.execute("SELECT empid from employee_data WHERE empid= %s",(empid,))
          if cursor.fetchone():
           messagebox.showerror("Error", "Id already exists.")
           return
          
          query="""
          INSERT INTO employee_data Values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)     
          """
          cursor.execute(query,(empid, name, email, gender, dob, contacts, employmenttype, education, workshift, address, doj, salary, usertype, password))
          connection.commit()
          treeview_data()
          messagebox.showinfo("Success", "Data Is Inserted Successfully")
        except Exception as e:
          messagebox.showerror("Error", str(e))
        finally:
          cursor.close()
          connection.close()  

def employee_frame(frame2):
        global backimage
        global font3
        global font1
        global employee_treeview
        employeeframe= Frame(frame2,height= 900, width= 1200)
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
        searchframe= ttk.Combobox(search_frame, values=("empid", "name", "email"), font=("helvetica",12), state="readonly")
        searchframe.set("Search By")
        searchframe.grid(row=0, column=0, padx=20)
        search_entry= Entry(search_frame, font=("helvetica",12), bg="lightblue")
        search_entry.grid(row=0, column=1)
        searchbutton= Button(search_frame, text= "SEARCH", font=("segou UI", 12),width=10, cursor= "hand2",fg="white", bg="#01082d", command= lambda: search_employee(searchframe.get(),search_entry.get()))
        searchbutton.grid(row=0, column=2, padx=20)
        showallbutton= Button(search_frame, text= "Show All", font=("segou UI", 12), width=10, cursor= "hand2",fg="white", bg="#01082d", command= show_all)
        showallbutton.grid(row=0, column=3, padx=20)

        hscroll= Scrollbar(top_frame, orient=HORIZONTAL)
        vscroll= Scrollbar(top_frame, orient=VERTICAL)

        employee_treeview= ttk.Treeview(top_frame, columns= ("empid", "name", "email", "gender", "dob", "contacts", "employmenttype","education", "workshift", "address", "doj","salary", "usertype", "password"), show= "headings", yscrollcommand= vscroll.set, xscrollcommand= hscroll.set )
        
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
        employee_treeview.heading("education", text= "Education")
        employee_treeview.heading("workshift", text= "Work Shift")
        employee_treeview.heading("address", text= "Address")
        employee_treeview.heading("doj", text= "DOJ")
        employee_treeview.heading("salary", text= "Salary")
        employee_treeview.heading("usertype", text= "User Type")
        employee_treeview.heading("password", text= "Password")
        
        
        

        font4= f.Font(family="helvetica",size=10)

        treeview_data()

        detail_frame= Frame(employeeframe, height=1800, width=1000,bg= "white")
        detail_frame.place(x=100, y=300)

        
        empid_label=Label(detail_frame, text= "EmpId",font=font4)
        empid_label.grid(row=0, column=0, padx=20, pady=10)
        empid_entry= Entry(detail_frame, font=font4, bg="lightblue")
        empid_entry.grid(row=0, column=1,padx=10, pady=10)
        empid_entry.bind("<Return>", move_next)

        name_label=Label(detail_frame, text= "Name",font=font4)
        name_label.grid(row=0, column=2,padx=20, pady=10)
        name_entry= Entry(detail_frame, font=font4, bg= "lightblue")
        name_entry.grid(row=0, column=3, padx=10, pady=10)
        name_entry.bind("<Return>", move_next)
        

    
        email_label=Label(detail_frame, text= "E-Mail",font=font4)
        email_label.grid(row=0, column=4, pady=10, padx=10)
        email_entry= Entry(detail_frame, font=font4, bg= "lightblue")
        email_entry.grid(row=0, column=5, pady=10, padx=10)
        email_entry.bind("<Return>", move_next)

        gender_label=Label(detail_frame, text= "Gender",font=font4)
        gender_label.grid(row=1, column=0, pady=10, padx=10)

        gender_combobox= ttk.Combobox(detail_frame, values=("male", "female"), font= font4, width=18, state= "readonly")
        gender_combobox.set("Select Gender")
        gender_combobox.grid(row=1, column=1,pady=10, padx=10)
        gender_combobox.bind("<Return>", move_next)

        Doj_label=Label(detail_frame, text= "Date of Joining",font=font4)
        Doj_label.grid(row=1, column=2, pady=10, padx=10)

        Doj_date= DateEntry(detail_frame, width=18, state= "readonly", date_pattern="dd/MM/yyyy", showmonthyears=True, showweeknumbers=False, selectmode='day')
        
        Doj_date.grid(row=1, column=3, pady=10, padx=10,sticky= 'w')
        Doj_date.bind("<Return>", move_next)
        
        

        dob_label=Label(detail_frame, text= "Date Of Birth",font=font4)
        dob_label.grid(row=1, column=4, pady=10, padx=10)
        dob_date_entry= DateEntry(detail_frame, width=18, font=font4, state= "readonly", date_pattern="dd/MM/yyyy", showmonthyears=True, showweeknumbers=False, selectmode='day')
        dob_date_entry.grid(row=1, column=5, pady=10, padx=10, sticky='w')
        dob_date_entry.bind("<Return>", move_next)

        emptype_label=Label(detail_frame, text= "Employement Type",font=font4)
        emptype_label.grid(row=2, column=0, pady=10, padx=10)
        emptype_combobox= ttk.Combobox(detail_frame, values=("Full Time", "Part Time", "Intern"), font= font4, width=18, state= "readonly")
        emptype_combobox.set("Employement Type")
        emptype_combobox.grid(row=2, column=1, pady=10, padx=10)
        emptype_combobox.bind("<Return>", move_next)

        Education_label=Label(detail_frame, text= "Education",font=font4)
        Education_label.grid(row=2, column=2, pady=10, padx=10)
        Education_combobox= ttk.Combobox(detail_frame, values=("M.Com", "B.Com", "Bba", "Mba", "B.a", "M.a","Other"), font= font4, width=18, state= "readonly")
        Education_combobox.set("Select Education")
        Education_combobox.grid(row=2, column=3, pady=10, padx=10)
        Education_combobox.bind("<Return>", move_next)

        Work_Shift_label=Label(detail_frame, text= "Work Shift",font=font4)
        Work_Shift_label.grid(row=2, column=4, pady=10, padx=10)
        Work_Shift_combobox= ttk.Combobox(detail_frame, values=("Morning", "Evening", "Night"), font= font4, width=18, state= "readonly")
        Work_Shift_combobox.set("Select Work Shift")
        Work_Shift_combobox.grid(row=2, column=5, pady=10, padx=10)
        Work_Shift_combobox.bind("<Return>", move_next)

        Address_label=Label(detail_frame, text= "Address",font=font4)
        Address_label.grid(row=3, column=0, pady=10, padx=20)
        Address_text= Text(detail_frame,width=20, height=3, font= font4)
        Address_text.grid(row=3, column=1, pady=10, padx=10, rowspan=2)
        Address_text.bind("<Return>", move_next)

        contact_label=Label(detail_frame, text= "Contact",font=font4)
        contact_label.grid(row=3, column=2, pady=10, padx=10)
        contact_entry= Entry(detail_frame, font=font4, bg= "lightblue")
        contact_entry.grid(row=3, column=3, pady=10, padx=10)
        contact_entry.bind("<Return>", move_next)

        salary_label=Label(detail_frame, text= "Salary",font=font4)
        salary_label.grid(row=3, column=4, padx=10, pady=10)
        salary_entry= Entry(detail_frame, font=font4, bg="lightblue")
        salary_entry.grid(row=3, column=5,padx=10, pady=10)
        salary_entry.bind("<Return>", move_next)

        usertype_label=Label(detail_frame, text= "User Type",font=font4)
        usertype_label.grid(row=4, column=2, pady=10, padx=10)
        usertype_combobox= ttk.Combobox(detail_frame, values=("Employee", "Admin", "Member", "Guest"), font= font4, width=18, state= "readonly")
        usertype_combobox.set("Select User Type")
        usertype_combobox.grid(row=4, column=3, padx=10, pady=10)
        usertype_combobox.bind("<Return>", move_next)

        Pass_label=Label(detail_frame, text= "Password",font=font4)
        Pass_label.grid(row=4, column=4, padx=10, pady=10)
        Pass_entry= Entry(detail_frame, font=font4, bg="lightblue")
        Pass_entry.grid(row=4, column=5)
        Pass_entry.bind("<Return>", move_next)

        button_framee=Frame(frame2, height=50, width=1270, bg="white")
        button_framee.place(x=320, y=668)
        
        add_button= Button(button_framee, text= "ADD", font=("segou UI", 11),width=15, cursor= "hand2",fg="white", bg="#01082d", command= lambda: add_employee(empid_entry.get(),name_entry.get(),email_entry.get(),gender_combobox.get(), dob_date_entry.get(), contact_entry.get(), emptype_combobox.get(), Education_combobox.get(),Work_Shift_combobox.get(), Address_text.get(1.0, END),Doj_date.get(),salary_entry.get(),usertype_combobox.get(),Pass_entry.get()))
        add_button.grid(row=0, column=0, padx=30)

        update_button= Button(button_framee, text= "UPDATE", font=("segou UI", 11),width=15, cursor= "hand2",fg="white", bg="#01082d", command= lambda: update(empid_entry.get(),name_entry.get(),email_entry.get(),gender_combobox.get(), dob_date_entry.get(), contact_entry.get(), emptype_combobox.get(), Education_combobox.get(),Work_Shift_combobox.get(), Address_text.get(1.0, END),Doj_date.get(),salary_entry.get(),usertype_combobox.get(),Pass_entry.get()))
        update_button.grid(row=0, column=1, padx=30)
        
        delete_button= Button(button_framee, text= "DELETE", font=("segou UI", 11),width=15, cursor= "hand2",fg="white", bg="#01082d",command= lambda: delete_employee(empid_entry.get()))
        delete_button.grid(row=0, column=2, padx=30)

        clear_button= Button(button_framee, text= "CLEAR", font=("segou UI", 11),width=15, cursor= "hand2",fg="white", bg="#01082d", command=lambda: clear_fields(empid_entry,name_entry,email_entry,gender_combobox, dob_date_entry, contact_entry, emptype_combobox, Education_combobox,Work_Shift_combobox, Address_text,Doj_date,salary_entry,usertype_combobox,Pass_entry))
        clear_button.grid(row=0, column=3, padx=30)
        employee_treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, empid_entry,name_entry,email_entry,gender_combobox, dob_date_entry, contact_entry, emptype_combobox, Education_combobox,Work_Shift_combobox, Address_text,Doj_date,salary_entry,usertype_combobox,Pass_entry))
        empid_entry.focus_set()







        
