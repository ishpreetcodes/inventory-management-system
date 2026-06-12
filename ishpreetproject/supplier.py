from tkinter import *
from tkinter import ttk
import tkinter.font as f
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql

#connection

def connect_database():
  try:
   connection= pymysql.connect(host= "localhost", user= "root",password= "tiger", port= 3306)

   cursor=connection.cursor()

   cursor.execute("USE inventory_system")
   cursor.execute('''CREATE TABLE IF NOT EXISTS supplier_data
                     (invoice_no INT Primary key,
                      name VARCHAR(50), contact VARCHAR(60),
                      description VARCHAR(100))''')
   return connection, cursor
  except Exception as e:
      messagebox.showerror("ERROR",f"Database Error: {e}")
      return None, None
  else:
   print("database is connected")
connect_database()


#add button functionality
def add_supplier(invoice_no, name, contact, description):
        if (invoice_no==""or name== "" or contact== "" or description =="/n"):
          messagebox.showerror("ERROR", "All Fields Are Required")
          return
        connection, cursor = connect_database()
        if not cursor or not connection:
          return
        
        try:
          cursor.execute("use inventory_system")
          cursor.execute("SELECT invoice_no from supplier_data WHERE invoice_no= %s",(invoice_no,))
          if cursor.fetchone():
           messagebox.showerror("Error", "Invoice Number Already Exists.")
           return
          cursor.execute("INSERT INTO supplier_data Values(%s,%s,%s,%s)",(invoice_no,name,contact,description))
          connection.commit()
          treeview_data()
          messagebox.showinfo("Success", "Data Is Inserted Successfully")
        except Exception as e:
          messagebox.showerror("Error", str(e))
        finally:
          cursor.close()
          connection.close()

#treeviewadd

def treeview_data():
  connection, cursor = connect_database()
  if not cursor or not connection:
    return
  try:
      cursor.execute("USE inventory_system")
      cursor.execute("SELECT * from supplier_data")
      supplier_records= cursor.fetchall()
      treevieww.delete(*treevieww.get_children())
      for record in supplier_records:
          treevieww.insert("", END, values= record)
          
  except Exception as e :
      messagebox.showerror('Error', f'Error Due to {e}')
  finally:
      cursor.close()
      connection.close()

#clearbutton_functionality

def clear_fields(Invoice_entry, Name_entry, Contact_entry, Description_entry):
   Invoice_entry.delete(0, END)
   Name_entry.delete(0, END)
   Contact_entry.delete(0, END)
   Description_entry.delete(1.0, END)

#deletebutton_functionalty

def delete_supplier(invoice_no):
  selected= treevieww.selection()
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
     cursor.execute('DELETE FROM supplier_data where invoice_no= %s', (invoice_no))
     connection.commit()
     treeview_data()
     messagebox.showinfo("success", "data deleted")
  except Exception as e:
     messagebox.showerror("error", f'error due to {e}')
  finally:
     connection.close()
     cursor.close()

#Update Button Functionality

def select_data(event,Invoice_entry, Name_entry, Contact_entry, Description_entry):
  
  index= treevieww.selection()
  content= treevieww.item(index)
  row= content['values']
  
  clear_fields(Invoice_entry, Name_entry, Contact_entry, Description_entry)

  Invoice_entry.insert(0, row[0])
  Name_entry.insert(0, row[1])
  Contact_entry.insert(0, row[2])
  Description_entry.insert(1.0, row[3])
  

def update(invoice_no, name, contact, description):
  selected= treevieww.selection()
  if not selected :
   messagebox.showerror("Error", "Row not selected")
   return
  connection, cursor = connect_database()
  if not connection or not cursor:
     return
  try:
     cursor.execute("USE inventory_system")
     cursor.execute("UPDATE supplier_data SET name= %s,contact= %s, description=%s WHERE invoice_no=%s", (name,contact,description,invoice_no))
     connection.commit()
     treeview_data()
     messagebox.showinfo("Success", "Data is updated succesfully")
  except Exception as e:
    messagebox.showerror("error", f"Update failed: {e}")
  finally:
    connection.close()

def search_supplier(search_value,treevieww):
  if search_value== "" :
    messagebox.showerror("Error", "Please Enter Invoice Number")
  else:
    connection, cursor = connect_database()
    if not cursor or not connection :
      return
    try:
       cursor.execute("USE inventory_system")
       cursor.execute("SELECT * from supplier_data WHERE invoice_no= %s", search_value)
       
    
       records= cursor.fetchall()
       treevieww.delete(*treevieww.get_children())
       for record in records:
        treevieww.insert('', END, values= record)
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
def auto_save(event, inv_ent, name_ent, cnt_ent, desc_txt):
    add_supplier(Invoice_entry.get(), Name_entry.get(), Contact_entry.get(), Description_entry.get(1.0, "end-1c"))
    return "break"
  
   
def supplier_form(frame2):
        global back_image
        global font3
        global font1
        global treevieww
        supplier_frame= Frame(frame2,height= 700, width= 1200)
        supplier_frame.place(x=200, y=165)
        headinglabel= Label(supplier_frame,text= "Manage Supplier Details", fg="white", font=("Times new roman", 20), bg="#01082d")
        headinglabel.place(x=0,y=0,relwidth=1)
        back_image= PhotoImage(file="backimage.png")
        back_button=Button(supplier_frame, image=back_image,bg="#f2f4f7", bd=0, cursor="hand2", command= lambda:supplier_frame.place_forget())
        back_button.place(x=0,y=0)
        
        left_frame=Frame(supplier_frame)
        left_frame.place(x=0, y=100)
        
        Invoicelabel= Label(left_frame, text= "Invoice No.",font=("Times new roman", 14))
        Invoicelabel.grid(row=0, column=0,padx=10,pady=10, sticky= "w")
        Invoice_entry= Entry(left_frame,bg= "light yellow", font=("Times new roman",14))
        Invoice_entry.grid(row=0, column=1,padx=10,pady=10, sticky= "w")
        Invoice_entry.bind("<Return>", move_next)

        Namelabel= Label(left_frame, text= "Supplier Name",font=("Times new roman", 14))
        Namelabel.grid(row=1, column=0, padx=10,pady=10, sticky= "w")
        Name_entry= Entry(left_frame,bg= "light yellow", font=("Times new roman",14))
        Name_entry.grid(row=1, column=1,padx=10,pady=10, sticky= "w")
        Name_entry.bind("<Return>", move_next)

        Contactlabel= Label(left_frame, text= "Supplier Contact",font=("Times new roman", 14))
        Contactlabel.grid(row=2, column=0,padx=10,pady=10, sticky= "w")
        Contact_entry= Entry(left_frame,bg= "light yellow", font=("Times new roman",14))
        Contact_entry.grid(row=2, column=1,padx=10,pady=10, sticky= "w")
        Contact_entry.bind("<Return>", move_next)

        Descriptionlabel= Label(left_frame, text= "Description",font=("Times new roman", 14))
        Descriptionlabel.grid(row=3, column=0, padx=10,pady=20, sticky= "nw")
        Description_entry= Text(left_frame,bg= "light yellow", font=("Times new roman",14), width=25, height=6)
        Description_entry.grid(row=3, column=1,padx=10,pady=10, sticky= "w")
        Description_entry.bind("<Return>", lambda event: auto_save(event, Invoice_entry, Name_entry, Contact_entry, Description_entry))

        button_frame=Frame(left_frame)
        button_frame.grid(row=4, column=0, columnspan=4, pady=50, sticky="w")

        Save_button= Button(button_frame, text= "Save", font=("segou UI", 11),width=15, cursor= "hand2",fg="white", bg="#01082d", command= lambda : add_supplier(Invoice_entry.get(), Name_entry.get(), Contact_entry.get(), Description_entry.get(1.0, END)))
        Save_button.grid(row=0, column=0, padx=30)

        update_button= Button(button_frame, text= "UPDATE", font=("segou UI", 11),width=15, cursor= "hand2",fg="white", bg="#01082d", command= lambda: update(Invoice_entry.get(), Name_entry.get(), Contact_entry.get(), Description_entry.get(1.0, END)))
        update_button.grid(row=0, column=1, padx=30)
        
        delete_button= Button(button_frame, text= "DELETE", font=("segou UI", 11),width=15, cursor= "hand2",fg="white", bg="#01082d", command= lambda: delete_supplier(Invoice_entry.get()))
        delete_button.grid(row=0, column=2, padx=30)

        clear_button= Button(button_frame, text= "CLEAR", font=("segou UI", 11),width=15, cursor= "hand2",fg="white", bg="#01082d", command= lambda : clear_fields(Invoice_entry,  Name_entry, Contact_entry, Description_entry))
        clear_button.grid(row=0, column=3, padx=30)

        
        right_frame= Frame(supplier_frame)
        right_frame.place(x=565, y=90, width=500, height=340)
        search_frame=Frame(right_frame)
        search_frame.pack()

        Invoicelabell= Label(search_frame, text= "Invoice No.",font=("Times new roman", 11))
        Invoicelabell.grid(row=0, column=0,padx=5,pady=5, sticky= "w")
        Invoice_entryy= Entry(search_frame,bg= "light yellow", font=("Times new roman",11))
        Invoice_entryy.grid(row=0, column=1,padx=5,pady=5, sticky= "w")

        show_button= Button(search_frame, text= "Search", font=("segou UI", 10),width=10, cursor= "hand2",fg="white", bg="#01082d", command= lambda: search_supplier(Invoice_entryy.get(),treevieww))
        show_button.grid(row=0, column=2, padx=15)
        showall_button= Button(search_frame, text= "Show All", font=("segou UI", 10),width=10, cursor= "hand2",fg="white", bg="#01082d", command= show_all)
        showall_button.grid(row=0, column=3, padx=15)

        scroll_y= Scrollbar(right_frame, orient= VERTICAL)
        scroll_x= Scrollbar(right_frame, orient= HORIZONTAL)
        

        treevieww= ttk.Treeview(right_frame, columns=( "Invoice Number","Name","Contact","Description"), show= "headings", yscrollcommand= scroll_y.set, xscrollcommand= scroll_x.set)
        scroll_y.pack(side= RIGHT, fill=Y)
        scroll_x.pack(side= BOTTOM, fill=X)
        scroll_x.config(command= treevieww.xview)
        scroll_y.config(command= treevieww.yview)
        
        
        treevieww.heading("Invoice Number", text= "Invoice Number")
        treevieww.heading("Name",text="Name")
        treevieww.heading("Contact",text="Contact")
        treevieww.heading("Description",text="Description")

        treevieww.column("Invoice Number", width=100)
        treevieww.column("Name", width=180)
        treevieww.column("Contact", width=150)
        treevieww.column("Description", width=290)
        treevieww.pack(fill= BOTH, expand=1)

        treeview_data()
        treevieww.bind('<ButtonRelease-1>', lambda event: select_data(event, Invoice_entry,  Name_entry, Contact_entry, Description_entry))
        Invoice_entry.focus_set()

        
            

        

        

        

        
        










        









                             

