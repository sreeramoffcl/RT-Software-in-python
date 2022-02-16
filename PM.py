from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import sqlite3


# Create an entry with placeholder
class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', *args, **kwargs):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


def run_pm():
    root = Tk()
    root.title('Product master')
    root.geometry("1300x500")

    # Functions for functionalities

    # Enter data from db into treeview
    def query_db():
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        cursor.execute("SELECT rowid,* FROM prod_master")
        records = cursor.fetchall()
        # Add our data to the screen
        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2], record[3], record[4], record[5]),
                               tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2], record[3], record[4], record[5]),
                               tags=('oddrow',))
            # increment counter
            count += 1

        conn.commit()
        conn.close()

    # Clear entries
    def clear_entries():
        # Clear entry boxes
        pc_entry.delete(0, END)
        ic_entry.delete(0, END)
        dn_entry.delete(0, END)
        desc_entry.delete(0, END)
        weight_entry.delete(0, END)

    # Select records
    def select_records(e):
        # Clear entry boxes
        pc_entry.delete(0, END)
        ic_entry.delete(0, END)
        dn_entry.delete(0, END)
        desc_entry.delete(0, END)
        weight_entry.delete(0, END)
        try:
            # Grab record Number
            selected = my_tree.focus()
            # Grab record values
            values = my_tree.item(selected, 'values')

            pc_entry.insert(0, values[1])
            ic_entry.insert(0, values[2])
            dn_entry.insert(0, values[3])
            desc_entry.insert(0, values[4])
            weight_entry.insert(0, values[5])
        except IndexError:
            pass

    # Update record
    def update_records():
        # Grab the record number
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        try:
            weight = float(weight_entry.get())
            cursor.execute("""
                UPDATE prod_master SET 
                prod_code = :prod_code,
                item_code = :item_code,
                draw_no = :draw_no,
                desc = :desc,
                weight = :weight
                WHERE oid = :oid
            """, {
                "prod_code": pc_entry.get(),
                "item_code": ic_entry.get(),
                "draw_no": dn_entry.get(),
                "desc": desc_entry.get(),
                "weight": weight,
                "oid": values[0]
            })
            # Update record
            my_tree.item(selected, text="",
                         values=(
                             values[0], pc_entry.get(), ic_entry.get(), dn_entry.get(), desc_entry.get(),
                             weight_entry.get(),))
        except ValueError:
            messagebox.showerror("Error", "Enter number in Weight box!")

        conn.commit()
        conn.close()

        # Clear entry boxes
        pc_entry.delete(0, END)
        ic_entry.delete(0, END)
        dn_entry.delete(0, END)
        desc_entry.delete(0, END)
        weight_entry.delete(0, END)

    # Add record
    def add_record():
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM prod_master WHERE prod_code = :prod_code", {"prod_code": pc_entry.get()})
        pc = cursor.fetchall()

        cursor.execute("SELECT * FROM prod_master WHERE item_code = :item_code", {"item_code": ic_entry.get()})
        ic = cursor.fetchall()
        # Check whether data entered is a float for weight
        try:
            weight = float(weight_entry.get())
            if not pc and not ic:
                cursor.execute("INSERT INTO prod_master VALUES (:prod_code, :item_code, :draw_no, :desc, :weight)", {
                    "prod_code": pc_entry.get(),
                    "item_code": ic_entry.get(),
                    "draw_no": dn_entry.get(),
                    "desc": desc_entry.get(),
                    "weight": weight
                })

            else:
                messagebox.showerror("Error", "Record exists")
        except ValueError:
            messagebox.showerror("Error", "Enter number in Weight box!")

        conn.commit()
        conn.close()

        # Clear entry boxes
        pc_entry.delete(0, END)
        ic_entry.delete(0, END)
        dn_entry.delete(0, END)
        desc_entry.delete(0, END)
        weight_entry.delete(0, END)

        # Clear The Treeview Table
        my_tree.delete(*my_tree.get_children())

        # Run to pull data from database on start
        query_db()

    # Delete record
    def delete_record():
        # Confirm deletion
        yes_no = messagebox.askyesno("Warning", "Delete the record?")
        if yes_no:
            # Deletion from Database
            conn = sqlite3.connect("data.db")
            cursor = conn.cursor()

            # Grab the record number
            selected = my_tree.focus()
            values = my_tree.item(selected, 'values')
            # print(values[0])
            cursor.execute("DELETE from prod_master WHERE oid=" + values[0])

            conn.commit()
            conn.close()

            # Deletion from tree
            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_db()
        clear_entries()

    # Add entry boxes
    entry_frame = LabelFrame(root, text="Record")
    entry_frame.pack(fill="x", padx=20)

    pc_label = Label(entry_frame, text="Product Code")
    pc_label.grid(row=0, column=0, padx=10, pady=10)
    pc_entry = Entry(entry_frame, borderwidth=3)
    pc_entry.grid(row=0, column=1, padx=10, pady=10)

    ic_label = Label(entry_frame, text="Item Code")
    ic_label.grid(row=0, column=2, padx=10, pady=10)
    ic_entry = Entry(entry_frame, borderwidth=3)
    ic_entry.grid(row=0, column=3, padx=10, pady=10)

    dn_label = Label(entry_frame, text="Drawing Number")
    dn_label.grid(row=0, column=4, padx=10, pady=10)
    dn_entry = Entry(entry_frame, borderwidth=3)
    dn_entry.grid(row=0, column=5, padx=10, pady=10)

    desc_label = Label(entry_frame, text="Description")
    desc_label.grid(row=1, column=0, padx=10, pady=10)
    desc_entry = Entry(entry_frame, borderwidth=3)
    desc_entry.grid(row=1, column=1, padx=10, pady=10)

    weight_label = Label(entry_frame, text="Weight")
    weight_label.grid(row=1, column=2, padx=10, pady=10)
    weight_entry = Entry(entry_frame, borderwidth=3)
    weight_entry.grid(row=1, column=3, padx=10, pady=10)

    # Add Buttons
    button_frame = LabelFrame(root, text="Commands")
    button_frame.pack(fill="x", padx=20)

    add_button = Button(button_frame, text="Add Record", command=add_record)
    add_button.grid(row=0, column=0, padx=10, pady=10)

    update_button = Button(button_frame, text="Update Record", command=update_records)
    update_button.grid(row=0, column=1, padx=10, pady=10)

    delete_button = Button(button_frame, text="Delete Record", command=delete_record)
    delete_button.grid(row=0, column=2, padx=10, pady=10)

    clear_button = Button(button_frame, text="Clear Entries", command=clear_entries)
    clear_button.grid(row=0, column=3, padx=10, pady=10)

    # Search entry
    search_entry = EntryWithPlaceholder(root, "Search...", borderwidth=5)

    def searched(e):
        # Clear The Treeview Table
        my_tree.delete(*my_tree.get_children())
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        # Filter by value entered in search entry
        search_val = "%" + search_entry.get() + "%"

        cursor.execute("""SELECT rowid,* FROM prod_master WHERE
            prod_code LIKE :search OR
            item_code LIKE :search OR
            draw_no LIKE :search OR
            desc LIKE :search OR
            weight LIKE :search
        """, {
            "search": search_val
        })
        records = cursor.fetchall()

        # Add our data to the screen
        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2], record[3], record[4], record[5]),
                               tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2], record[3], record[4], record[5]),
                               tags=('oddrow',))
            # increment counter
            count += 1

        conn.commit()
        conn.close()

    search_entry.pack(fill="x", padx=20, pady=20, ipady=5)

    # Add treeview

    # Add Some Style
    style = ttk.Style()

    # Pick A Theme
    style.theme_use('default')

    # Configure the Treeview Colors
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")

    # Change Selected Color
    style.map('Treeview',
              background=[('selected', "#347083")])

    # Create a Treeview Frame
    tree_frame = Frame(root)
    tree_frame.pack()

    # Create a Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse")
    my_tree.pack()

    # Configure the Scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Define Our Columns
    my_tree['columns'] = ("ID", "Product Code", "Item Code", "Drawing Number", "Description", "Weight")

    # Format Our Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID", anchor=W, width=75)
    my_tree.column("Product Code", anchor=W, width=200)
    my_tree.column("Item Code", anchor=W, width=200)
    my_tree.column("Drawing Number", anchor=CENTER, width=300)
    my_tree.column("Description", anchor=CENTER, width=300)
    my_tree.column("Weight", anchor=CENTER, width=150)

    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ID", text="ID", anchor=W)
    my_tree.heading("Product Code", text="Product Code", anchor=W)
    my_tree.heading("Item Code", text="Item Code", anchor=W)
    my_tree.heading("Drawing Number", text="Drawing Number", anchor=CENTER)
    my_tree.heading("Description", text="Description", anchor=CENTER)
    my_tree.heading("Weight", text="Weight", anchor=CENTER)

    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    my_tree.bind("<ButtonRelease-1>", select_records)

    search_entry.bind("<KeyRelease>", searched)

    # Run to pull data from database on start
    query_db()

    root.mainloop()
