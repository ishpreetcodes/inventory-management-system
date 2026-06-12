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
   cursor.execute('''CREATE TABLE IF NOT EXISTS category_data
                     (Id INT Primary key,
                      name VARCHAR(50),
                      description VARCHAR(100))''')
   return connection, cursor
  except Exception as e:
      messagebox.showerror("ERROR",f"Database Error: {e}")
      return None, None
  else:
   print("database is connected")
connect_database()


#add button functionality
def add_category(Id, name,description):
        if (Id==""or name== "" or description =="/n"):
          messagebox.showerror("ERROR", "All Fields Are Required")
          return
        connection, cursor = connect_database()
        if not cursor or not connection:
          return
        
        try:
          cursor.execute("use inventory_system")
          cursor.execute("SELECT Id from category_data WHERE Id= %s",(Id,))
          if cursor.fetchone():
           messagebox.showerror("Error", "Id Already Exists.")
           return
          cursor.execute("INSERT INTO category_data Values(%s,%s,%s)",(Id,name,description))
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
      cursor.execute("SELECT * from category_data")
      category_records= cursor.fetchall()
      Tree.delete(*Tree.get_children())
      for record in category_records:
          Tree.insert("", END, values= record)
          
  except Exception as e :
      messagebox.showerror('Error', f'Error Due to {e}')
  finally:
      cursor.close()
      connection.close()

 #clearbutton_functionality

def clear_fields(ID_entry,catname_entry,descrip_entry):
   ID_entry.delete(0, END)
   catname_entry.delete(0, END)
   descrip_entry.delete(1.0, END)

#deletebutton_functionalty

def delete_category(Id):
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
     cursor.execute("USE inventory_system")
     cursor.execute('DELETE FROM category_data where Id= %s', (Id))
     connection.commit()
     treeview_data()
     messagebox.showinfo("success", "data deleted")
  except Exception as e:
     messagebox.showerror("error", f'error due to {e}')
  finally:
     connection.close()
     cursor.close()
     #Update button functionality
def select_data(event,ID_entry,catname_entry,descrip_entry):
  
  index= Tree.selection()
  content= Tree.item(index)
  row= content['values']
  
  clear_fields(ID_entry,catname_entry,descrip_entry)

  ID_entry.insert(0, row[0])
  catname_entry.insert(0, row[1])
  descrip_entry.insert(1.0, row[2])

def move_next(event):
    event.widget.tk_focusNext().focus()
    return "break"
def auto_save(event, ID_entry,catname_entry,descrip_entry):
    add_category(ID_entry.get(),catname_entry.get(),descrip_entry.get("1.0", END))          
    return "break"
  


def category_form(frame2):
        global backimage
        global font3
        global font1
        global categorylogo
        global Tree

        categoryframe= Frame(frame2,height= 660, width= 1200)
        categoryframe.place(x=200, y=165)
        headinglabel= Label(categoryframe,text= "Managing Product Category", fg="white", font=("Times new roman", 20), bg="#01082d")
        headinglabel.place(x=0,y=0,relwidth=1)
        backimage= PhotoImage(file="backimage.png")
        back_button=Button(categoryframe, image=backimage,bg="#f2f4f7", bd=0, cursor="hand2", command= lambda:categoryframe.place_forget())
        back_button.place(x=0,y=0)

        logo= PhotoImage(file="categorylogoo.png")
        label=Label(categoryframe, image= logo)
        label.place(x=100, y=100)
        label.image = logo 

        details_frame=Frame(categoryframe)
        details_frame.place(x=500, y=60)

        IDlabel= Label(details_frame, text= "ID",font=("Times new roman", 14))
        IDlabel.grid(row=0, column=0,padx=10,pady=10, sticky= "w")
        ID_entry= Entry(details_frame,bg= "light yellow", font=("Times new roman",14))
        ID_entry.grid(row=0, column=1,padx=10,pady=10, sticky= "w")
        ID_entry.bind("<Return>", move_next)

        catnamelabel= Label(details_frame, text= "Category Name",font=("Times new roman", 14))
        catnamelabel.grid(row=1, column=0,padx=10,pady=10, sticky= "w")
        catname_entry= Entry(details_frame,bg= "light yellow", font=("Times new roman",14))
        catname_entry.grid(row=1, column=1,padx=10,pady=10, sticky= "w")
        catname_entry.bind("<Return>", move_next)

        descriplabel= Label(details_frame, text= "Description",font=("Times new roman", 14))
        descriplabel.grid(row=2, column=0,padx=10,pady=10, sticky= "w")
        descrip_entry= Text(details_frame,bg= "light yellow", font=("Times new roman",14),width=20, height=4)
        descrip_entry.grid(row=2, column=1,padx=10,pady=10, sticky= "w")
        descrip_entry.bind("<Return>", move_next)
        
        button_frame=Frame(categoryframe)
        button_frame.place(x=480, y=270)

        Add_button= Button(button_frame, text= "ADD", font=("segou UI", 11),width=15, cursor= "hand2",fg="white", bg="#01082d", command= lambda : add_category(ID_entry.get(),catname_entry.get(),descrip_entry.get("1.0", END)))
        Add_button.grid(row=0, column=0, padx=30)

        Delete_button= Button(button_frame, text= "DELETE", font=("segou UI", 11),width=15, cursor= "hand2",fg="white", bg="#01082d", command= lambda : delete_category(ID_entry.get()))
        Delete_button.grid(row=0, column=1, padx=30)
        
        Clear_button= Button(button_frame, text= "CLEAR", font=("segou UI", 11),width=15, cursor= "hand2",fg="white", bg="#01082d", command= lambda : clear_fields(ID_entry, catname_entry,descrip_entry))
        Clear_button.grid(row=0, column=2, padx=30)

        T_frame=Frame(categoryframe)
        T_frame.place(x=500, y=320,height=200, width=600)


        scroll_y= Scrollbar(T_frame, orient= VERTICAL)
        scroll_x= Scrollbar(T_frame, orient= HORIZONTAL)
        

        Tree= ttk.Treeview(T_frame, columns=( "ID","Category_Name","Description"), show= "headings", yscrollcommand= scroll_y.set, xscrollcommand= scroll_x.set)
        scroll_y.pack(side= RIGHT, fill=Y)
        scroll_x.pack(side= BOTTOM, fill=X)
        scroll_x.config(command= Tree.xview)
        scroll_y.config(command= Tree.yview)
        
        
        Tree.heading("ID", text= "ID")
        Tree.heading("Category_Name",text="Category Name")
        Tree.heading("Description",text="Description")

        Tree.column("ID", width=100)
        Tree.column("Category_Name", width=280)
        Tree.column("Description", width=390)
        Tree.pack(fill= BOTH, expand=1)
        treeview_data()
        Tree.bind('<ButtonRelease-1>', lambda event: select_data(event, ID_entry,  catname_entry, descrip_entry))
        ID_entry.focus_set()
        

        


        

        

        

        

        

        

        
