from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import platform
import sqlite3


# Create an entry with placeholder
class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
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


def run_crm():
    def scrolled(e):
        if platform.system() == "Windows" or platform.system() == "Linux":
            canvas.yview_scroll(-1 * (e.delta / 120), "units")
        else:
            canvas.yview_scroll(-1 * e.delta, "units")

    # Enter data from db into treeview
    def query_db():
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        cursor.execute("SELECT rowid,* FROM cust_master")
        records = cursor.fetchall()
        # Add our data to the screen
        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2], record[9], record[10]),
                               tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2], record[9], record[10]),
                               tags=('oddrow',))
            # increment counter
            count += 1

        conn.commit()
        conn.close()

    # Clear entries
    def clear_entries():
        # Clear entry boxes
        cn_entry.delete(0, END)
        cc_entry.delete(0, END)
        add_entry1.delete(0, END)
        add_entry2.delete(0, END)
        add_entry3.delete(0, END)
        district_entry.delete(0, END)
        city_entry.delete(0, END)
        pincode_entry.delete(0, END)
        gst_entry.delete(0, END)
        pan_entry.delete(0, END)
        remarks_entry.delete(0, END)

    # Select records
    def select_records(e):
        # Clear entry boxes
        cn_entry.delete(0, END)
        cc_entry.delete(0, END)
        add_entry1.delete(0, END)
        add_entry2.delete(0, END)
        add_entry3.delete(0, END)
        district_entry.delete(0, END)
        city_entry.delete(0, END)
        pincode_entry.delete(0, END)
        gst_entry.delete(0, END)
        pan_entry.delete(0, END)
        remarks_entry.delete(0, END)
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        try:
            # Grab record Number
            selected = my_tree.focus()
            # Grab record values
            id = my_tree.item(selected, 'values')[0]

            cursor.execute("SELECT rowid,* FROM cust_master WHERE rowid=:id", {"id": id})
            values = cursor.fetchall()

            cc_entry.insert(0, values[0][1])
            cn_entry.insert(0, values[0][2])
            add_entry1.insert(0, values[0][3])
            add_entry2.insert(0, values[0][4])
            add_entry3.insert(0, values[0][5])
            district_entry.insert(0, values[0][6])
            city_entry.insert(0, values[0][7])
            pincode_entry.insert(0, values[0][8])
            gst_entry.insert(0, values[0][9])
            pan_entry.insert(0, values[0][10])
            remarks_entry.insert(0, values[0][11])
        except IndexError:
            pass
        conn.commit()
        conn.close()

    # Update record
    def update_records():
        # Grab the record number
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE cust_master SET 
            cust_code=:cust_code,
            cust_name=:cust_name,
            add_1=:add_1, 
            add_2=:add_2,
            add_3=:add_3,
            city=:city, 
            district=:district, 
            pincode=:pincode, 
            gst=:gst, 
            pan=:pan, 
            remarks=:remarks 
            WHERE oid=:oid""",
                       {
                           "cust_code": cc_entry.get(),
                           "cust_name": cn_entry.get(),
                           "add_1": add_entry1.get(),
                           "add_2": add_entry2.get(),
                           "add_3": add_entry3.get(),
                           "city": city_entry.get(),
                           "district": district_entry.get(),
                           "pincode": pincode_entry.get(),
                           "gst": gst_entry.get(),
                           "pan": pan_entry.get(),
                           "remarks": remarks_entry.get(),
                           "oid": values[0]
                       })
        # Update record
        my_tree.item(selected, text="",
                     values=(
                         values[0], cc_entry.get(),
                         cn_entry.get(),
                         gst_entry.get(),
                         pan_entry.get(),
                     ))

        conn.commit()
        conn.close()

        # Clear entry boxes
        cn_entry.delete(0, END)
        cc_entry.delete(0, END)
        add_entry1.delete(0, END)
        add_entry2.delete(0, END)
        add_entry3.delete(0, END)
        district_entry.delete(0, END)
        city_entry.delete(0, END)
        pincode_entry.delete(0, END)
        gst_entry.delete(0, END)
        pan_entry.delete(0, END)
        remarks_entry.delete(0, END)

    # Add record
    def add_record():
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO cust_master VALUES (:cust_code, :cust_name, :add_1, :add_2, :add_3, :city, :district, :pincode, :gst, :pan, :remarks)",
            {
                "cust_code": cc_entry.get(),
                "cust_name": cn_entry.get(),
                "add_1": add_entry1.get(),
                "add_2": add_entry2.get(),
                "add_3": add_entry3.get(),
                "city": city_entry.get(),
                "district": district_entry.get(),
                "pincode": pincode_entry.get(),
                "gst": gst_entry.get(),
                "pan": pan_entry.get(),
                "remarks": remarks_entry.get()
            })

        conn.commit()
        conn.close()

        # Clear entry boxes
        cn_entry.delete(0, END)
        cc_entry.delete(0, END)
        add_entry1.delete(0, END)
        add_entry2.delete(0, END)
        add_entry3.delete(0, END)
        district_entry.delete(0, END)
        city_entry.delete(0, END)
        pincode_entry.delete(0, END)
        gst_entry.delete(0, END)
        pan_entry.delete(0, END)
        remarks_entry.delete(0, END)

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
            cursor.execute("DELETE from cust_master WHERE oid=" + values[0])

            conn.commit()
            conn.close()

            # Deletion from tree
            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_db()
        clear_entries()

    root = Tk()
    root.title("Customer masters")
    root.geometry("1200x500")

    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=1)
    canvas = Canvas(main_frame, bd=2, highlightthickness=0, borderwidth=0)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scroll = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scroll.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scroll.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind('<Enter>', lambda e: canvas.bind_all("<MouseWheel>", lambda ev: scrolled(ev)))
    canvas.bind('<Leave>', lambda e: canvas.unbind_all("<MouseWheel>"))
    sec_frame = Frame(canvas)
    canvas.create_window((0, 0), window=sec_frame, anchor=NW)

    # Create input fields
    inp_frame = LabelFrame(sec_frame, text="Records")
    inp_frame.pack(fill="x", padx=20)

    cc_label = Label(inp_frame, text="Customer Code")
    cc_label.grid(row=0, column=0, padx=5, pady=5)
    cc_entry = Entry(inp_frame, borderwidth=3)
    cc_entry.grid(row=0, column=1, padx=5, pady=5)

    cn_label = Label(inp_frame, text="Customer Name")
    cn_label.grid(row=0, column=2, padx=5, pady=5)
    cn_entry = Entry(inp_frame, borderwidth=3)
    cn_entry.grid(row=0, column=3, padx=5, pady=5)

    add_label = Label(inp_frame, text="Address")
    add_label.grid(row=1, column=2, padx=5, pady=5)
    add_entry1 = Entry(inp_frame, borderwidth=3)
    add_entry1.grid(row=1, column=3, padx=5, pady=5)
    add_entry2 = Entry(inp_frame, borderwidth=3)
    add_entry2.grid(row=2, column=3, padx=5, pady=5)
    add_entry3 = Entry(inp_frame, borderwidth=3)
    add_entry3.grid(row=3, column=3, padx=5, pady=5)

    district_label = Label(inp_frame, text="District")
    district_label.grid(row=4, column=2, padx=5, pady=5)
    district_entry = Entry(inp_frame, borderwidth=3)
    district_entry.grid(row=4, column=3, padx=5, pady=5)

    city_label = Label(inp_frame, text="City")
    city_label.grid(row=5, column=2, padx=5, pady=5)
    city_entry = Entry(inp_frame, borderwidth=3)
    city_entry.grid(row=5, column=3, padx=5, pady=5)

    pincode_label = Label(inp_frame, text="Pincode")
    pincode_label.grid(row=6, column=2, padx=5, pady=5)
    pincode_entry = Entry(inp_frame, borderwidth=3)
    pincode_entry.grid(row=6, column=3, padx=5, pady=5)

    gst_label = Label(inp_frame, text="GST")
    gst_label.grid(row=1, column=0, padx=5, pady=5)
    gst_entry = Entry(inp_frame, borderwidth=3)
    gst_entry.grid(row=1, column=1, padx=5, pady=5)

    pan_label = Label(inp_frame, text="PAN")
    pan_label.grid(row=2, column=0, padx=5, pady=5)
    pan_entry = Entry(inp_frame, borderwidth=3)
    pan_entry.grid(row=2, column=1, padx=5, pady=5)

    remarks_label = Label(inp_frame, text="Remarks")
    remarks_label.grid(row=3, column=0, padx=5, pady=5)
    remarks_entry = Entry(inp_frame, borderwidth=3)
    remarks_entry.grid(row=3, column=1, padx=5, pady=5)

    # Add buttons
    button_frame = LabelFrame(sec_frame, text="Commands")
    button_frame.pack(fill=X, padx=20)

    add_button = Button(button_frame, text="Add Record", command=add_record)
    add_button.grid(row=0, column=0, padx=10, pady=10)

    update_button = Button(button_frame, text="Update Record", command=update_records)
    update_button.grid(row=0, column=1, padx=10, pady=10)

    delete_button = Button(button_frame, text="Delete Record", command=delete_record)
    delete_button.grid(row=0, column=2, padx=10, pady=10)

    clear_button = Button(button_frame, text="Clear Entries", command=clear_entries)
    clear_button.grid(row=0, column=3, padx=10, pady=10)

    # Search entry
    # Search entry
    search_entry = EntryWithPlaceholder(sec_frame, "Search...")

    def searched(e):
        # Clear The Treeview Table
        my_tree.delete(*my_tree.get_children())
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        # Filter by value entered in search entry
        search_val = "%" + search_entry.get() + "%"

        cursor.execute("""SELECT rowid,* FROM cust_master WHERE
                cust_code LIKE :search OR
                cust_name LIKE :search OR
                gst LIKE :search OR
                pan LIKE :search
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
                               values=(record[0], record[1], record[2], record[9], record[10]),
                               tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2], record[9], record[10]),
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
    tree_frame = Frame(sec_frame)
    tree_frame.pack()

    # Create a Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse")
    my_tree.pack(padx=20)

    # Configure the Scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Define Our Columns
    my_tree['columns'] = ("ID", "Customer Code", "Customer Name", "GST", "PAN")

    # Format Our Columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID", anchor=W, width=75)
    my_tree.column("Customer Code", anchor=W, width=200)
    my_tree.column("Customer Name", anchor=W, width=200)
    my_tree.column("GST", anchor=CENTER, width=300)
    my_tree.column("PAN", anchor=CENTER, width=300)

    # Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("ID", text="ID", anchor=W)
    my_tree.heading("Customer Code", text="Customer Code", anchor=W)
    my_tree.heading("Customer Name", text="Customer Name", anchor=W)
    my_tree.heading("GST", text="GST", anchor=CENTER)
    my_tree.heading("PAN", text="PAN", anchor=CENTER)

    # Create Striped Row Tags
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    my_tree.bind("<ButtonRelease-1>", select_records)
    search_entry.bind("<KeyRelease>", searched)

    query_db()

    root.mainloop()
