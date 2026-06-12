
from tkinter import *
from tkinter import ttk
import tkinter.font as f
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql
from employee import connect_database

Tree= None


def fetch_supplier_category(category_combobox, supplier_combobox):
    category_option= []
    supplier_option=[]
    connection,cursor= connect_database()
    if not cursor or not connection:
          return
    cursor.execute("use inventory_system")
    cursor.execute("SELECT name from category_data")
    names= cursor.fetchall()
    if len(names)>0 :
        category_combobox.set("Select")
        for name in names :
          category_option.append(name[0])
        category_combobox.config(values= category_option)

    
    cursor.execute("SELECT name from  supplier_data")
    names= cursor.fetchall()
    if len(names)>0 :
        supplier_combobox.set("Select")
        for name in names :
          supplier_option.append(name[0])
        supplier_combobox.config(values= supplier_option)
        
def treeview_data():
  global Tree
  connection, cursor = connect_database()
  if not cursor or not connection:
    return
  try:
      cursor.execute("USE inventory_system")
      cursor.execute("SELECT * from product_data")
      product_records= cursor.fetchall()
      Tree.delete(*Tree.get_children())
      for record in product_records:
          Tree.insert("", END, values= record)
          
  except Exception as e :
      messagebox.showerror('Error', f'Error Due to {e}')
  finally:
      cursor.close()
      connection.close()

        
def add_product(category, supplier, name, price, quantity, status):
    if category== "Empty" :
        messagebox.showerror("Error", "Please Add Category.")
    elif supplier== "Empty":
        messagebox.showerror("Error", "Please Add Supplier.")
    elif category== "Select" or supplier==  "Select" or name== ""or price==""or quantity=="" or status== "Select Status":
        messagebox.showerror("Error", "All Fields Are Required.")
    else:
        connection, cursor= connect_database()
        if not cursor or not connection:
          return
        try:
         cursor.execute("use inventory_system")
         cursor.execute("CREATE TABLE IF NOT EXISTS product_data(Id INT AUTO_INCREMENT Primary key,category VARCHAR(100), supplier VARCHAR(100), name VARCHAR(100),price DECIMAL(10,2), quantity INT, status VARCHAR(100))")
         cursor.execute("INSERT INTO product_data (category, supplier,name, price, quantity, status)Values(%s,%s,%s,%s,%s,%s)",(category, supplier,name, price, quantity, status))
         connection.commit()
         messagebox.showinfo("Success", "Data Is Inserted Successfully")
         treeview_data()
        except Exception as e:
          messagebox.showerror("Error", str(e))
        finally:
          cursor.close()
          connection.close()
def clear_fields(category_combobox, supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox):
   name_entry.delete(0, END)
   price_entry.delete(0, END)
   quantity_entry.delete(0, END)
   supplier_combobox.set("Select")
   category_combobox.set("Select")
   status_combobox.set("Select")

def delete_product():
  global Tree
  selected= Tree.selection()
  if not selected :
   messagebox.showerror("Error", "Row not selected")
  else:
    result= messagebox.askyesno("Confirm", "Do You Really Want To Delete The Record?")
    if result:
     connection, cursor = connect_database()
     if not connection or not cursor:
      return
  try:
     content = Tree.item(selected)
     row = content['values']
     product_id = row[0]
     cursor.execute("USE inventory_system")
     cursor.execute('DELETE FROM product_data where Id= %s', (product_id,))
     connection.commit()
     treeview_data()
     messagebox.showinfo("success", "data deleted")
  except Exception as e:
    messagebox.showerror("error", f'error due to {e}')
  finally:
    connection.close()
    cursor.close()
   

def select_data(event,category_combobox, supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox):
  global Tree
  index= Tree.selection()
  content= Tree.item(index)
  row= content['values']
  
  clear_fields(category_combobox, supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox)
  
  category_combobox.set(row[1])
  supplier_combobox.set(row[2])
  name_entry.insert(0,row[3])
  price_entry.insert(0,row[4])
  quantity_entry.insert(0, row[5])
  status_combobox.set(row[6])

def update_product(category, supplier, name, price, quantity, status):
  global Tree
  selected= Tree.selection()
  if not selected :
   messagebox.showerror("Error", "Row not selected")
   return
  connection, cursor = connect_database()
  if not connection or not cursor:
     return
  try:
     content = Tree.item(selected)
     row = content['values']
     product_id = row[0]
     cursor.execute("USE inventory_system")
     cursor.execute("UPDATE product_data SET category= %s, supplier= %s, name= %s,price= %s, quantity=%s,status=%s WHERE Id=%s", (category, supplier, name,price, quantity,status, product_id))
     connection.commit()
     treeview_data()
     messagebox.showinfo("Success", "Data is updated succesfully")
  except Exception as e:
    messagebox.showerror("error", f"Update failed: {e}")
  finally:
    connection.close()

def search_employee(search_option,value):
  if search_option== "Search By" :
    messagebox.showerror("Error", "No Option is Selected.")
  elif value== "" :
    messagebox.showerror("Error", "Select the value to search.")
  else:
    connection, cursor = connect_database()
    if not cursor or not connection :
      return
    try:
       cursor.execute("USE inventory_system")
       query= f"SELECT * from product_data WHERE {search_option} LIKE %s"
       cursor.execute(query, (f"%{value}%",))
    
       records= cursor.fetchall()
       Tree.delete(*Tree.get_children())
       for record in records:
        Tree.insert('', END, values= record)
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
def auto_save(event, category, supplier, name, price, quantity, status):
    add_product(category_combobox.get(), supplier_combobox.get(), name_entry.get(), price_entry.get(), quantity_entry.get(), status_combobox.get())
    return "break"
        
def product_form(frame2):
    global Tree

    global backimage

    productframe= Frame(frame2,height= 660, width= 1200, bg="white")
    productframe.place(x=200, y=165)
    backimage= PhotoImage(file="backimage.png")
    back_button=Button(productframe, image=backimage,bg="#f2f4f7", bd=0, cursor="hand2", command= lambda:productframe.place_forget())
    back_button.place(x=10,y=0)

    left_frame= Frame(productframe, relief= RIDGE, bd=2)

    left_frame.place(x=20,y=30,height= 500, width= 560)
    left_frame.grid_propagate(False)
    headinglabel= Label(left_frame,text= "Managing Products", fg="white", font=("Times new roman", 20), bg="#01082d")
    headinglabel.grid(row=0,column=0,columnspan=2, sticky="we")

    categorylabel= Label(left_frame, text= "Category",font=("Times new roman", 14))
    categorylabel.grid(row=1, column=0, padx=15, sticky= "w")
    category_combobox= ttk.Combobox(left_frame, state= "readonly",font=("Times new roman", 14))
    category_combobox.grid(row=1, column=1, pady=20, sticky= "w", padx=20)
    category_combobox.set("Empty")
    category_combobox.bind("<Return>", move_next)

    supplierlabel= Label(left_frame, text= "Supplier",font=("Times new roman", 14))
    supplierlabel.grid(row=2, column=0,padx=15, sticky= "w")
    supplier_combobox= ttk.Combobox(left_frame, state= "readonly",font=("Times new roman", 14))
    supplier_combobox.grid(row=2, column=1, pady=20, sticky= "w", padx=20)
    supplier_combobox.set("Empty")
    supplier_combobox.bind("<Return>", move_next)

    namelabel= Label(left_frame, text= "Product Name",font=("Times new roman", 14))
    namelabel.grid(row=3, column=0,padx=15, sticky= "w")
    name_entry= Entry(left_frame,bg= "light yellow", font=("Times new roman",14))
    name_entry.grid(row=3, column=1,pady=20,sticky= "w", padx=20)
    name_entry.bind("<Return>", move_next)

    pricelabel= Label(left_frame, text= "Product Price",font=("Times new roman", 14))
    pricelabel.grid(row=4, column=0,padx=15, sticky= "w")
    price_entry= Entry(left_frame,bg= "light yellow", font=("Times new roman",14))
    price_entry.grid(row=4, column=1,pady=20, sticky= "w", padx=20)
    price_entry.bind("<Return>", move_next)

    quantitylabel= Label(left_frame, text= "Product Quantity",font=("Times new roman", 14))
    quantitylabel.grid(row=5, column=0,padx=15, sticky= "w")
    quantity_entry= Entry(left_frame,bg= "light yellow", font=("Times new roman",14))
    quantity_entry.grid(row=5, column=1,pady=20, sticky= "w", padx=20)
    quantity_entry.bind("<Return>", move_next)

    statuslabel= Label(left_frame, text= "Status",font=("Times new roman", 14))
    statuslabel.grid(row=6, column=0,padx=15, sticky= "w")
    status_combobox= ttk.Combobox(left_frame,values=("Active", "Inactive"),state= "readonly",font=("Times new roman", 14))
    status_combobox.grid(row=6, column=1, pady=20,sticky= "w", padx=20)
    status_combobox.set("Select Status")
    status_combobox.bind("<Return>", move_next)

    button_frame= Frame(left_frame)
    button_frame.grid(row=7, columnspan=2, pady=(20,30), padx=(10,0))

    add_button= Button(button_frame, text= "ADD", font=("segou UI", 10),width=14, cursor= "hand2",fg="white", bg="#01082d", command= lambda: add_product(category_combobox.get(), supplier_combobox.get(), name_entry.get(), price_entry.get(), quantity_entry.get(), status_combobox.get()))
    add_button.grid(row=0, column=0, padx=8)

    update_button= Button(button_frame, text= "UPDATE", font=("segou UI", 10),width=14, cursor= "hand2",fg="white", bg="#01082d", command= lambda: update_product(category_combobox.get(), supplier_combobox.get(), name_entry.get(), price_entry.get(), quantity_entry.get(), status_combobox.get()))
    update_button.grid(row=0, column=1, padx=8)
        
    delete_button= Button(button_frame, text= "DELETE", font=("segou UI", 10),width=14, cursor= "hand2",fg="white", bg="#01082d", command= lambda: delete_product())
    delete_button.grid(row=0, column=2, padx=8)

    clear_button= Button(button_frame, text= "CLEAR", font=("segou UI", 10),width=14, cursor= "hand2",fg="white", bg="#01082d", command= lambda : clear_fields(category_combobox, supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox))
    clear_button.grid(row=0, column=3, padx=8)

    #SearchFrame

    search_frame= LabelFrame(productframe, text= "Search Products",font=("Segoe UI", 14, "bold"),bg= "#DBE9F4")
    search_frame.place(x=590, y=30)
    search_combo=ttk.Combobox(search_frame, values= ("Category", "Supplier", "Name", "Status"),state= "readonly",font=("Times new roman", 12), width=14)
    search_combo.grid(row=0, column=0, padx=10)
    search_combo.set("Search By")
    
    search_entry= Entry(search_frame,bg= "light blue", font=("Times new roman",14), width=14)
    search_entry.grid(row=0, column=1)
    search_button= Button(search_frame, text= "SEARCH", font=("Segoe UI", 12),width=11, cursor= "hand2",fg="white", bg="#01082d", height=1, command= lambda: search_employee(search_combo.get(),search_entry.get()))
    search_button.grid(row=0, column=2, padx=(10,10), pady=10)
    showall_button= Button(search_frame, text= "SHOW ALL", font=("Segoe UI", 12),width=11, cursor= "hand2",fg="white", bg="#01082d", height=1, command= lambda : show_all())
    showall_button.grid(row=0, column=3, padx=(10,10), pady=10)

    tree_frame= Frame(productframe,bg= "#DBE9F4")
    tree_frame.place(x=590, y=125, height=400, width=550)

    scroll_y= Scrollbar(tree_frame, orient= VERTICAL)
    scroll_x= Scrollbar(tree_frame, orient= HORIZONTAL)
        

    Tree= ttk.Treeview(tree_frame, columns=( "Id","category","supplier","name","price","quantity", "status"), show= "headings", yscrollcommand= scroll_y.set, xscrollcommand= scroll_x.set)
    scroll_y.pack(side= RIGHT, fill=Y)
    scroll_x.pack(side= BOTTOM, fill=X)
    scroll_x.config(command= Tree.xview)
    scroll_y.config(command= Tree.yview)

    Tree.pack(fill= BOTH, expand=1)
    
    Tree.heading("Id", text= "Id")
    Tree.heading("category", text= "Category")
    Tree.heading("supplier", text= "Supplier")
    Tree.heading("name", text= "Name")
    Tree.heading("price", text= "Price")
    Tree.heading("quantity", text= "Quantity")
    Tree.heading("status", text= "Status")
    fetch_supplier_category(category_combobox, supplier_combobox)
    treeview_data()
    Tree.bind('<ButtonRelease-1>', lambda event: select_data(event,category_combobox, supplier_combobox,name_entry, price_entry, quantity_entry, status_combobox))
    category_combobox.focus_set()
    

    
    

    

    

    
    

    
    
    

    

    
    











    

    

    
