import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Establish MySQL Connection
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    mycursor = mydb.cursor()

    # Create Database
    mycursor.execute("CREATE DATABASE IF NOT EXISTS SchoolStationeryDB;")
    mycursor.execute("USE SchoolStationeryDB;")

    # Create Items Table
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Items (
        item_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) UNIQUE,
        category VARCHAR(100),
        price DECIMAL(10,2),
        stock INT
    );
    """)

except mysql.connector.Error as err:
    print(f"Database Error: {err}")

# Tkinter GUI Setup
root = Tk()
root.title("School Stationery Inventory")
root.geometry("850x650")
root.configure(bg="#ADD8E6")

Label(root, text="School Stationery Inventory", font=("Arial", 16, "bold"), bg="#ADD8E6").grid(row=0, column=0, columnspan=2, pady=10)

# Function to Add Item
def add_item():
    name = name_entry.get()
    category = category_entry.get()
    price = price_entry.get()
    stock = stock_entry.get()

    if name and category and price and stock:
        sql = "INSERT INTO Items (name, category, price, stock) VALUES (%s, %s, %s, %s)"
        values = (name, category, float(price), int(stock))
        try:
            mycursor.execute(sql, values)
            mydb.commit()
            messagebox.showinfo("Success", "Item Added Successfully!")
            name_entry.delete(0, END)
            category_entry.delete(0, END)
            price_entry.delete(0, END)
            stock_entry.delete(0, END)
            display_all_items()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Item already exists!")
    else:
        messagebox.showerror("Error", "All fields are required!")

# Function to Update Item
def update_item():
    item_id = update_item_id_entry.get()
    name = update_name_entry.get()
    category = update_category_entry.get()
    price = update_price_entry.get()
    stock = update_stock_entry.get()

    if item_id and name and category and price and stock:
        sql = "UPDATE Items SET name=%s, category=%s, price=%s, stock=%s WHERE item_id=%s"
        values = (name, category, float(price), int(stock), item_id)
        try:
            mycursor.execute(sql, values)
            mydb.commit()
            if mycursor.rowcount > 0:
                messagebox.showinfo("Success", "Item Updated Successfully!")
                update_item_id_entry.delete(0, END)
                update_name_entry.delete(0, END)
                update_category_entry.delete(0, END)
                update_price_entry.delete(0, END)
                update_stock_entry.delete(0, END)
                display_all_items()
            else:
                messagebox.showerror("Error", "Item ID not found!")
        except mysql.connector.Error:
            messagebox.showerror("Error", "Update Failed!")
    else:
        messagebox.showerror("Error", "All fields are required!")

# Function to Delete Item
def delete_item():
    item_id = delete_item_id_entry.get()

    if item_id:
        sql = "DELETE FROM Items WHERE item_id = %s"
        values = (item_id,)
        try:
            mycursor.execute(sql, values)
            mydb.commit()
            if mycursor.rowcount > 0:
                messagebox.showinfo("Success", "Item Deleted Successfully!")
                delete_item_id_entry.delete(0, END)
                display_all_items()
            else:
                messagebox.showerror("Error", "Item ID not found!")
        except mysql.connector.Error:
            messagebox.showerror("Error", "Delete Failed!")
    else:
        messagebox.showerror("Error", "Item ID is required!")

# Function to Display All Items
def display_all_items():
    sql = "SELECT * FROM Items"
    mycursor.execute(sql)
    results = mycursor.fetchall()

    for row in item_tree.get_children():
        item_tree.delete(row)

    if results:
        for row in results:
            item_tree.insert("", "end", values=row)
    else:
        messagebox.showinfo("Info", "No items found.")

# UI Elements
Label(root, text="Item Name", bg="#ADD8E6").grid(row=1, column=0, padx=10, pady=5, sticky=E)
name_entry = Entry(root)
name_entry.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Category", bg="#ADD8E6").grid(row=2, column=0, padx=10, pady=5, sticky=E)
category_entry = Entry(root)
category_entry.grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Price", bg="#ADD8E6").grid(row=3, column=0, padx=10, pady=5, sticky=E)
price_entry = Entry(root)
price_entry.grid(row=3, column=1, padx=10, pady=5)

Label(root, text="Stock", bg="#ADD8E6").grid(row=4, column=0, padx=10, pady=5, sticky=E)
stock_entry = Entry(root)
stock_entry.grid(row=4, column=1, padx=10, pady=5)

Button(root, text="Add Item", command=add_item, bg="lightgreen").grid(row=5, column=1, pady=5)

# Update Item
Label(root, text="Item ID (for Update)", bg="#ADD8E6").grid(row=6, column=0, padx=10, pady=5, sticky=E)
update_item_id_entry = Entry(root)
update_item_id_entry.grid(row=6, column=1, padx=10, pady=5)

Label(root, text="New Name", bg="#ADD8E6").grid(row=7, column=0, padx=10, pady=5, sticky=E)
update_name_entry = Entry(root)
update_name_entry.grid(row=7, column=1, padx=10, pady=5)

Label(root, text="New Category", bg="#ADD8E6").grid(row=8, column=0, padx=10, pady=5, sticky=E)
update_category_entry = Entry(root)
update_category_entry.grid(row=8, column=1, padx=10, pady=5)

Label(root, text="New Price", bg="#ADD8E6").grid(row=9, column=0, padx=10, pady=5, sticky=E)
update_price_entry = Entry(root)
update_price_entry.grid(row=9, column=1, padx=10, pady=5)

Label(root, text="New Stock", bg="#ADD8E6").grid(row=10, column=0, padx=10, pady=5, sticky=E)
update_stock_entry = Entry(root)
update_stock_entry.grid(row=10, column=1, padx=10, pady=5)

Button(root, text="Update Item", command=update_item, bg="lightpink").grid(row=11, column=1, pady=5)

# Delete Item
Label(root, text="Item ID (for Delete)", bg="#ADD8E6").grid(row=12, column=0, padx=10, pady=5, sticky=E)
delete_item_id_entry = Entry(root)
delete_item_id_entry.grid(row=12, column=1, padx=10, pady=5)

Button(root, text="Delete Item", command=delete_item, bg="red").grid(row=13, column=1, pady=5)

# Button to Display All Items
Button(root, text="Display All Items", command=display_all_items, bg="grey").grid(row=14, column=1, pady=5)

# Treeview to Display Items
item_tree = ttk.Treeview(root, columns=("ID", "Name", "Category", "Price", "Stock"), show="headings", height=10)
item_tree.grid(row=15, column=0, columnspan=2, pady=10)

item_tree.heading("ID", text="ID")
item_tree.heading("Name", text="Name")
item_tree.heading("Category", text="Category")
item_tree.heading("Price", text="Price")
item_tree.heading("Stock", text="Stock")

display_all_items()
root.mainloop()

