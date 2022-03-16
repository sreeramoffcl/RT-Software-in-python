from tkinter import *
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
from ttkwidgets.autocomplete import AutocompleteEntry
import tkinter as tk
import platform
import datetime
import sqlite3


def material_inward():
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

    # AutocompleteCombobox but only accepts entries from list
    class MatchOnlyAutocompleteCombobox(AutocompleteCombobox):

        def autocomplete(self, delta=0):
            """
            Autocomplete the Combobox.

            :param delta: 0, 1 or -1: how to cycle through possible hits
            :type delta: int
            """
            if delta:  # need to delete selection otherwise we would fix the current position
                self.delete(self.position, END)
            else:  # set position to end so selection starts where textentry ended
                self.position = len(self.get())
            # collect hits
            _hits = []
            for element in self._completion_list:
                if element.lower().startswith(self.get().lower()):  # Match case insensitively
                    _hits.append(element)

            if not _hits:
                # No hits with current user text input
                self.position -= 1  # delete one character
                self.delete(self.position, END)
                # Display again last matched autocomplete
                self.autocomplete(delta)
                return

            # if we have a new hit list, keep this in mind
            if _hits != self._hits:
                self._hit_index = 0
                self._hits = _hits
            # only allow cycling if we are in a known hit list
            if _hits == self._hits and self._hits:
                self._hit_index = (self._hit_index + delta) % len(self._hits)
            # now finally perform the auto completion
            if self._hits:
                self.delete(0, END)
                self.insert(0, self._hits[self._hit_index])
                self.select_range(self.position, END)

    class MatchOnlyAutocompleteEntry(AutocompleteEntry):

        def autocomplete(self, delta=0):
            """
            Autocomplete the Combobox.

            :param delta: 0, 1 or -1: how to cycle through possible hits
            :type delta: int
            """
            if delta:  # need to delete selection otherwise we would fix the current position
                self.delete(self.position, END)
            else:  # set position to end so selection starts where textentry ended
                self.position = len(self.get())
            # collect hits
            _hits = []
            for element in self._completion_list:
                if element.lower().startswith(self.get().lower()):  # Match case insensitively
                    _hits.append(element)

            if not _hits:
                # No hits with current user text input
                self.position -= 1  # delete one character
                self.delete(self.position, END)
                # Display again last matched autocomplete
                self.autocomplete(delta)
                return

            # if we have a new hit list, keep this in mind
            if _hits != self._hits:
                self._hit_index = 0
                self._hits = _hits
            # only allow cycling if we are in a known hit list
            if _hits == self._hits and self._hits:
                self._hit_index = (self._hit_index + delta) % len(self._hits)
            # now finally perform the auto completion
            if self._hits:
                self.delete(0, END)
                self.insert(0, self._hits[self._hit_index])
                self.select_range(self.position, END)

    # Initialize values
    customer = ""
    prod_code = ""
    item_code = ""
    weight = ""
    count = 0
    conn = sqlite3.connect("masters.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grade_master")
    grade = [i[0] for i in cursor.fetchall()]
    cursor.execute("SELECT * FROM coverage_master")
    coverage = [i[0] for i in cursor.fetchall()]
    conn.commit()
    conn.close()

    remarks = ['FRESH', 'RESHOOT']
    # Get customer names as list
    conn = sqlite3.connect("masters.db")
    cursor = conn.cursor()
    cursor.execute("SELECT cust_name FROM cust_master")
    cust_names = [i[0] for i in cursor.fetchall()]
    conn.commit()
    conn.close()

    root = Toplevel()
    root.title("Material Inward")
    root.geometry("1300x500")

    # Functions for functionalities

    # init state of widgets
    def init():
        sl_entry.delete(0, END)
        cust_entry.delete(0, END)
        dc_entry.delete(0, END)
        dd_entry.delete(0, END)
        sl_entry.delete(0, END)
        sl_entry.insert(0, gen_sl_no())
        clear_entries_sec()
        dd_entry.delete(0, END)
        dd_entry.insert(0, datetime.date.today().strftime("%d/%m/%Y"))
        sl2_entry.delete(0, END)
        sl2_entry.insert(0, "1")
        main_tree.delete(*main_tree.get_children())

        cust_entry.focus()

    # Check platform for scroll settings
    def scrolled(e):
        if platform.system() == "Windows" or platform.system() == "Linux":
            canvas.yview_scroll(-1 * (e.delta / 120), "units")
        else:
            canvas.yview_scroll(-1 * e.delta, "units")

    # Validate entries for macOS
    def validate(event):
        keys = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']
        for i in keys:
            if i == event.keysym:
                return 'break'

    # Generate serial number for primary entry
    def gen_sl_no():
        conn = sqlite3.connect("transactions.db")
        cursor = conn.cursor()
        cursor.execute("SELECT sl_no FROM mat_inw_prim")
        this_year = datetime.datetime.now().year
        number = ""
        not_empty = cursor.fetchone()
        if not_empty is not None:
            cursor.execute("SELECT sl_no FROM mat_inw_prim")
            temp = cursor.fetchall()[-1]
            # last sl no in db
            last = temp[0]

            last_year = last.split("/")[1]
            # Last sl no excl year
            counter = last.split("/")[0]

            if int(last_year) == int(this_year):
                no = int(counter) + 1

                number = str(no) + "/" + str(this_year)
            else:
                number = str(1) + "/" + str(this_year)
        else:
            number = "1/" + str(this_year)
        conn.commit()
        conn.close()
        return number

    # Add record to database
    def add_prim_record():
        conn = sqlite3.connect("transactions.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mat_inw_prim VALUES (:sl_no, :customer, :dc_no, :dc_date)", {
            "sl_no": sl_entry.get(),
            "customer": cust_entry.get(),
            "dc_no": dc_entry.get(),
            "dc_date": dd_entry.get()

        })
        for child in main_tree.get_children():
            values = main_tree.item(child)["values"]

            cursor.execute(
                "INSERT INTO mat_inw_sec VALUES (:uid, :sl_no, :rt_no, :prod, :ic, :weight, :grade, :hn, :qty, :coverage, :remarks)",
                {
                    "uid": sl_entry.get(),
                    "sl_no": values[0],
                    "rt_no": values[1],
                    "prod": values[2],
                    "ic": values[3],
                    "weight": values[4],
                    "grade": values[5],
                    "hn": values[6],
                    "qty": values[7],
                    "coverage": values[8],
                    "remarks": values[9]
                })
        conn.commit()
        conn.close()

        init()

    # Add secondary record to treeview
    def add_sec_record():
        sl_no = sl2_entry.get()
        rt_no = rt_no_entry.get()
        prod_code_loc = prod_entry.get()
        item_code_loc = ic_entry.get()
        weight_loc = weight_entry.get()
        grade_temp = grade_entry.get()
        hn = hn_entry.get()
        qty = qty_entry.get()
        coverage_temp = cov_entry.get()
        remarks = rem_entry.get()
        if int(sl_no) % 2 == 0:
            main_tree.insert(parent="", index="end", text="",
                             values=(
                                 sl_no, rt_no, prod_code_loc, item_code_loc, weight_loc, grade_temp, hn, qty,
                                 coverage_temp, remarks),
                             tags=("evenrow",))
        else:
            main_tree.insert(parent="", index="end", text="",
                             values=(
                                 sl_no, rt_no, prod_code_loc, item_code_loc, weight_loc, grade_temp, hn, qty,
                                 coverage_temp, remarks),
                             tags=("oddrow",))
        # Clear entry boxes
        clear_entries_sec()

        # New sl no for next record
        sl2_entry.insert(0, str(int(sl_no) + 1))
        # Focus rt no entry
        rt_no_entry.focus()

    # Select the records from treeview
    def select_record(e):
        # Clear entry boxes
        clear_entries_sec()

        try:
            selected = main_tree.focus()
            values = main_tree.item(selected, "values")
            sl2_entry.insert(0, values[0])
            rt_no_entry.insert(0, values[1])
            prod_entry.configure(state="normal")
            prod_entry.delete(0, END)
            prod_entry.insert(0, values[2])
            prod_entry.configure(state="disabled")
            ic_entry.configure(state="normal")
            ic_entry.delete(0, END)
            ic_entry.insert(0, values[3])
            ic_entry.configure(state="disabled")
            weight_entry.delete(0, END)
            weight_entry.insert(0, values[4])
            grade_entry.insert(0, values[5])
            hn_entry.insert(0, values[6])
            qty_entry.insert(0, values[7])
            cov_entry.insert(0, values[8])
            rem_entry.insert(0, values[9])

        except IndexError:
            pass

    # Clear entries of secondary entries
    def clear_entries_sec():
        # Clear entry boxes
        sl2_entry.delete(0, END)
        rt_no_entry.delete(0, END)
        prod_entry.configure(state="normal")
        prod_entry.delete(0, END)
        prod_entry.configure(state="disabled")
        ic_entry.configure(state="normal")
        ic_entry.delete(0, END)
        ic_entry.configure(state="disabled")
        weight_entry.delete(0, END)
        grade_entry.delete(0, END)
        hn_entry.delete(0, END)
        qty_entry.delete(0, END)
        cov_entry.delete(0, END)
        rem_entry.delete(0, END)

    def clear_ent_btn():
        clear_entries_sec()
        sl_no = len(main_tree.get_children()) + 1
        sl2_entry.delete(0, END)
        sl2_entry.insert(0, sl_no)

    # Update treeview
    def update_record():
        selected = main_tree.focus()
        main_tree.item(selected, text="", values=(sl2_entry.get(), rt_no_entry.get(), prod_entry.get(), ic_entry.get(),
                                                  weight_entry.get(), grade_entry.get(), qty_entry.get(),
                                                  hn_entry.get(),
                                                  cov_entry.get(),
                                                  rem_entry.get()))
        clear_entries_sec()

    # Delete entry from treeview
    def delete_entry():
        # Delete selected entry
        selected = main_tree.selection()
        main_tree.delete(selected)
        # Sort sl no for the rest of the entries
        sl_no = 1
        for child in main_tree.get_children():
            values = main_tree.item(child)["values"]
            main_tree.delete(child)
            if int(sl_no) % 2 == 0:
                main_tree.insert(parent="", index="end", text="",
                                 values=(
                                     sl_no, values[1], values[2], values[3], values[4], values[5], values[6], values[7],
                                     values[8], values[9]),
                                 tags=("evenrow",))
            else:
                main_tree.insert(parent="", index="end", text="",
                                 values=(
                                     sl_no, values[1], values[2], values[3], values[4], values[5], values[6], values[7],
                                     values[8], values[9]),
                                 tags=("oddrow",))

            sl_no += 1
        # Clear entries
        clear_entries_sec()
        # Generate sl no for nxt entry
        sl2_entry.insert(0, sl_no)

    # View and edit existing DCs
    def view_dc(e):
        if platform.system() == "Windows" or platform.system() == "Linux":
            dc_no = dc_entry.get()
        else:
            dc_no = dc_entry.get()[:-1]

        if dc_no:
            dc_entry.delete(0, END)
            dc_entry.insert(0, dc_no)

            conn = sqlite3.connect("transactions.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mat_inw_prim WHERE dc_no = :dc_no", {'dc_no': dc_no})
            prim_entry = cursor.fetchall()
            if prim_entry:
                cursor.execute("SELECT * FROM mat_inw_sec WHERE uid = :uid", {'uid': prim_entry[0][0]})
                sec_entries = cursor.fetchall()
                sl_entry.delete(0, END)
                sl_entry.insert(0, prim_entry[0][0])
                cust_entry.delete(0, END)
                cust_entry.insert(0, prim_entry[0][1])
                dc_entry.delete(0, END)
                dc_entry.insert(0, prim_entry[0][2])
                dd_entry.delete(0, END)
                dd_entry.insert(0, prim_entry[0][3])
                clear_entries_sec()
                items = main_tree.get_children()
                for item in items:
                    main_tree.delete(item)
                # Add our data to the screen
                global count
                count = 1

                for record in sec_entries:

                    if count % 2 == 0:
                        main_tree.insert(parent="", index="end", text="",
                                         values=(
                                             record[1], record[2], record[3], record[4], record[5], record[6],
                                             record[7],
                                             record[8], record[9], record[10]
                                         ),
                                         tags=("evenrow",))
                    else:
                        main_tree.insert(parent="", index="end", text="",
                                         values=(
                                             record[1], record[2], record[3], record[4], record[5], record[6],
                                             record[7],
                                             record[8], record[9], record[10]
                                         ),
                                         tags=("oddrow",))
                    # increment counter
                    count += 1
            conn.commit()
            conn.close()
        else:
            return

    # Update primary record
    def update_prim_rec():
        sl_no = sl_entry.get()
        if platform.system() == "Windows" or platform.system() == "Linux":
            dc_no = dc_entry.get()
        else:
            dc_no = dc_entry.get()[:-1]
        conn = sqlite3.connect("transactions.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE mat_inw_prim SET sl_no = :sl_no, customer = :customer, dc_no = :dc_no, dc_date = :dc_date WHERE sl_no = :sl_no",
            {
                "sl_no": sl_entry.get(),
                "customer": cust_entry.get(),
                "dc_no": dc_no,
                "dc_date": dd_entry.get()

            })
        cursor.execute("DELETE FROM mat_inw_sec WHERE uid = :sl_no", {"sl_no": sl_no})
        global count
        count = 0
        records = main_tree.get_children()
        for i in records:
            record = main_tree.item(i)['values']
            cursor.execute(
                """INSERT INTO mat_inw_sec VALUES (:uid, :sl_no, :rt_no, :prod, :ic, :weight, :grade, :heat_no, :qty, :coverage, :remarks)""",
                {
                    "uid": sl_no,
                    "sl_no": record[0],
                    "rt_no": record[1],
                    "prod": record[2],
                    "ic": record[3],
                    "weight": record[4],
                    "grade": record[5],
                    "heat_no": record[6],
                    "qty": record[7],
                    "coverage": record[8],
                    "remarks": record[9]

                })
            # increment counter
            count += 1

        conn.commit()
        conn.close()
        init()

    # Create canvas for assigning scrollbar
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=1)
    canvas = Canvas(main_frame, bd=2, highlightthickness=0, borderwidth=0)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scroll = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scroll.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scroll.set)
    sec_frame = Frame(canvas)
    frame_id = canvas.create_window((0, 0), window=sec_frame, anchor=NW)

    # Maximize width of widgets in the canvas
    def canvas_configure(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfigure(frame_id, width=e.width)

    # Create first entry frame
    top_frame = LabelFrame(sec_frame, text="Primary Entry")
    top_frame.pack(fill=X, padx=20, pady=10)
    sl_label = Label(top_frame, text="Sl No")
    sl_entry = Entry(top_frame)
    sl_entry.insert(0, gen_sl_no())
    cust_label = Label(top_frame, text="Customer")
    cust_entry = MatchOnlyAutocompleteCombobox(top_frame, completevalues=cust_names)
    cust_entry.focus()
    lst = tk.Listbox(top_frame, bd=0, bg='white')
    dc_label = Label(top_frame, text="DC No")
    dc_entry = Entry(top_frame)
    dd_label = Label(top_frame, text="DC Date")
    dd_entry = Entry(top_frame)
    dd_entry.insert(0, datetime.date.today().strftime("%d/%m/%Y"))

    sl_label.grid(row=0, column=0, padx=5, pady=5)
    sl_entry.grid(row=0, column=1, padx=5, pady=5)
    cust_label.grid(row=0, column=2, padx=5, pady=5)
    cust_entry.grid(row=0, column=3, padx=5, pady=5)
    dc_label.grid(row=0, column=5, padx=5, pady=5)
    dc_entry.grid(row=0, column=6, padx=5, pady=5)
    dd_label.grid(row=0, column=7, padx=5, pady=5)
    dd_entry.grid(row=0, column=8, padx=5, pady=5)

    # Create secondary entries
    bottom_frame = LabelFrame(sec_frame, text="Secondary Entries")
    bottom_frame.pack(fill=X, padx=20, pady=10)

    sl2_label = Label(bottom_frame, text="Sl No")
    sl2_entry = Entry(bottom_frame)
    sl2_entry.insert(0, "1")
    rt_no_label = Label(bottom_frame, text="RT No")
    rt_no_entry = Entry(bottom_frame)
    prod_label = Label(bottom_frame, text="Product")
    prod_entry = Entry(bottom_frame, state="disabled")
    ic_label = Label(bottom_frame, text="Item Code")
    ic_entry = Entry(bottom_frame, state="disabled")
    weight_label = Label(bottom_frame, text="Weight")

    # Function for selecting the customer
    def select_rt_details():
        menu = Toplevel()

        # Select Customer
        def selected(e):
            conn = sqlite3.connect("masters.db")
            cursor = conn.cursor()
            try:
                sel = prod_tree.focus()
                rowid = prod_tree.item(sel, "values")[0]
                cursor.execute("SELECT desc, item_code, weight FROM prod_master WHERE rowid=:id", {"id": rowid})
                val = cursor.fetchall()
                global prod_code, item_code, weight
                prod_code = val[0][0]
                item_code = val[0][1]
                weight = val[0][2]

            except IndexError:
                pass
            conn.commit()
            conn.close()

        # Enter data from db into treeview
        def query_db():
            conn = sqlite3.connect("masters.db")
            cursor = conn.cursor()

            cursor.execute("SELECT rowid,* FROM prod_master")
            records = cursor.fetchall()
            # Add our data to the screen
            global count
            count = 0

            for record in records:
                if count % 2 == 0:
                    prod_tree.insert(parent='', index='end', text='',
                                     values=(record[0], record[1], record[2], record[3], record[4], record[5]),
                                     tags=('evenrow',))
                else:
                    prod_tree.insert(parent='', index='end', text='',
                                     values=(record[0], record[1], record[2], record[3], record[4], record[5]),
                                     tags=('oddrow',))
                # increment counter
                count += 1

            conn.commit()
            conn.close()

        def searched(e):
            # Clear The Treeview Table
            prod_tree.delete(*prod_tree.get_children())
            conn = sqlite3.connect("masters.db")
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
                    prod_tree.insert(parent='', index='end', text='',
                                     values=(record[0], record[1], record[2], record[3], record[4], record[5]),
                                     tags=('evenrow',))
                else:
                    prod_tree.insert(parent='', index='end', text='',
                                     values=(record[0], record[1], record[2], record[3], record[4], record[5]),
                                     tags=('oddrow',))
                # increment counter
                count += 1

            conn.commit()
            conn.close()

        def submitted():
            prod_entry.configure(state="normal")
            prod_entry.delete(0, END)
            prod_entry.insert(0, prod_code)
            prod_entry.configure(state="disabled")
            ic_entry.configure(state="normal")
            ic_entry.delete(0, END)
            ic_entry.insert(0, item_code)
            ic_entry.configure(state="disabled")
            weight_entry.delete(0, END)
            weight_entry.insert(0, weight)
            menu.destroy()

        menu.title("Browse")
        menu.geometry("1000x400")

        # Search entry
        search_frame = Frame(menu)
        search_frame.pack()
        search_entry = EntryWithPlaceholder(search_frame, "Search...")

        search_entry.grid(row=0, column=0, padx=20, pady=20, ipady=5)
        btn_submit = Button(search_frame, text="Submit", command=submitted)
        btn_submit.grid(row=0, column=1, padx=20, pady=20, ipady=5)
        # search_entry.bind("<KeyRelease>", searched)

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
        prod_tree_frame = Frame(menu)
        prod_tree_frame.pack()

        # Create a Treeview Scrollbar
        prod_tree_scrolly = Scrollbar(prod_tree_frame)
        prod_tree_scrolly.pack(side=RIGHT, fill=Y)
        prod_tree_scrollx = Scrollbar(prod_tree_frame, orient=HORIZONTAL)
        prod_tree_scrollx.pack(side=BOTTOM, fill=X)

        # Create The Treeview
        prod_tree = ttk.Treeview(prod_tree_frame, xscrollcommand=prod_tree_scrollx.set,
                                 yscrollcommand=prod_tree_scrolly.set, selectmode="browse")
        prod_tree.pack(padx=20)

        # Configure the Scrollbar
        prod_tree_scrolly.config(command=prod_tree.yview)
        prod_tree_scrollx.config(command=prod_tree.xview)

        # Define Our Columns
        prod_tree['columns'] = ("ID", "Product Code", "Item Code", "Drawing Number", "Description", "Weight")

        # Format Our Columns
        prod_tree.column("#0", width=0, stretch=NO)
        prod_tree.column("ID", anchor=W, width=75)
        prod_tree.column("Product Code", anchor=W, width=200)
        prod_tree.column("Item Code", anchor=W, width=200)
        prod_tree.column("Drawing Number", anchor=CENTER, width=300)
        prod_tree.column("Description", anchor=CENTER, width=300)
        prod_tree.column("Weight", anchor=CENTER, width=150)

        # Create Headings
        prod_tree.heading("#0", text="", anchor=W)
        prod_tree.heading("ID", text="ID", anchor=W)
        prod_tree.heading("Product Code", text="Product Code", anchor=W)
        prod_tree.heading("Item Code", text="Item Code", anchor=W)
        prod_tree.heading("Drawing Number", text="Drawing Number", anchor=CENTER)
        prod_tree.heading("Description", text="Description", anchor=CENTER)
        prod_tree.heading("Weight", text="Weight", anchor=CENTER)

        # Create Striped Row Tags
        prod_tree.tag_configure('oddrow', background="white")
        prod_tree.tag_configure('evenrow', background="lightblue")

        prod_tree.bind("<ButtonRelease-1>", selected)

        search_entry.bind("<KeyRelease>", searched)
        search_entry.focus()
        # Run to pull data from database on start
        query_db()

    btn_rt_details = Button(bottom_frame, text="Browse", command=select_rt_details)
    btn_rt_details.bind("<Return>", lambda e: select_rt_details())
    weight_entry = Entry(bottom_frame)
    grade_label = Label(bottom_frame, text="Grade")
    grade_entry = MatchOnlyAutocompleteCombobox(bottom_frame, completevalues=grade)
    hn_label = Label(bottom_frame, text="Heat No")
    hn_entry = Entry(bottom_frame)
    qty_label = Label(bottom_frame, text="Quantity")
    qty_entry = Entry(bottom_frame)
    cov_label = Label(bottom_frame, text="Coverage")
    cov_entry = MatchOnlyAutocompleteCombobox(bottom_frame, completevalues=coverage)
    rem_label = Label(bottom_frame, text="Remarks")
    rem_entry = MatchOnlyAutocompleteEntry(bottom_frame, completevalues=remarks)

    sl2_label.grid(row=0, column=0, padx=5, pady=5)
    sl2_entry.grid(row=0, column=1, padx=5, pady=5)
    rt_no_label.grid(row=0, column=2, padx=5, pady=5)
    rt_no_entry.grid(row=0, column=3, padx=5, pady=5)
    prod_label.grid(row=0, column=4, padx=5, pady=5)
    prod_entry.grid(row=0, column=5, padx=5, pady=5)
    btn_rt_details.grid(row=0, column=6, padx=5, pady=5, ipadx=10)
    ic_label.grid(row=1, column=0, padx=5, pady=5)
    ic_entry.grid(row=1, column=1, padx=5, pady=5)
    weight_label.grid(row=1, column=2, padx=5, pady=5)
    weight_entry.grid(row=1, column=3, padx=5, pady=5)
    grade_label.grid(row=1, column=4, padx=5, pady=5)
    grade_entry.grid(row=1, column=5, padx=5, pady=5)
    hn_label.grid(row=1, column=6, padx=5, pady=5)
    hn_entry.grid(row=1, column=7, padx=5, pady=5)
    qty_label.grid(row=2, column=0, padx=5, pady=5)
    qty_entry.grid(row=2, column=1, padx=5, pady=5)
    cov_label.grid(row=2, column=2, padx=5, pady=5)
    cov_entry.grid(row=2, column=3, padx=5, pady=5)
    rem_label.grid(row=2, column=4, padx=5, pady=5)
    rem_entry.grid(row=2, column=5, padx=5, pady=5)

    # Create buttons for the secondary entries
    secondary_frame = LabelFrame(sec_frame, text="Secondary Commands")
    secondary_frame.pack(fill=X, padx=20, pady=10)

    btn_add_sec = Button(secondary_frame, text="Add Entry", command=add_sec_record)
    btn_update_sec = Button(secondary_frame, text="Update Entry", command=update_record)
    btn_del_sec = Button(secondary_frame, text="Delete Entry", command=delete_entry)
    btn_clear_sec = Button(secondary_frame, text="Clear Entries", command=clear_ent_btn)
    btn_add_sec.grid(row=0, column=0, padx=5, pady=5, ipadx=10)
    btn_update_sec.grid(row=0, column=1, padx=5, pady=5, ipadx=10)
    btn_del_sec.grid(row=0, column=2, padx=5, pady=5, ipadx=10)
    btn_clear_sec.grid(row=0, column=3, padx=5, pady=5, ipadx=10)

    # Add treeview

    # Add Some Style
    style_main = ttk.Style()

    # Pick A Theme
    style_main.theme_use('default')

    # Configure the Treeview Colors
    style_main.configure("Treeview",
                         background="#D3D3D3",
                         foreground="black",
                         rowheight=25,
                         fieldbackground="#D3D3D3")

    # Change Selected Color
    style_main.map('Treeview',
                   background=[('selected', "#347083")])

    # Create a Treeview Frame
    tree_frame = Frame(sec_frame)
    tree_frame.pack()

    # Create a Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    main_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse")
    main_tree.pack(padx=20)
    tree_scroll.config(command=main_tree.yview)

    # Define Our Columns
    main_tree['columns'] = (
        "Sl No", "RT No", "Product", "Item Code", "Weight", "Grade", "Heat No", "Quantity", "Coverage", "Remarks")

    # Format Our Columns
    main_tree.column("#0", width=0, stretch=NO)
    main_tree.column("Sl No", anchor=W, width=100)
    main_tree.column("RT No", anchor=W, width=200)
    main_tree.column("Product", anchor=W, width=200)
    main_tree.column("Item Code", anchor=CENTER, width=200)
    main_tree.column("Weight", anchor=CENTER, width=200)
    main_tree.column("Grade", anchor=CENTER, width=200)
    main_tree.column("Heat No", anchor=CENTER, width=200)
    main_tree.column("Quantity", anchor=CENTER, width=200)
    main_tree.column("Coverage", anchor=CENTER, width=200)
    main_tree.column("Remarks", anchor=CENTER, width=200)

    # Create Headings
    main_tree.heading("#0", text="", anchor=W)
    main_tree.heading("Sl No", text="Sl No", anchor=W)
    main_tree.heading("RT No", text="RT No", anchor=W)
    main_tree.heading("Product", text="Product", anchor=W)
    main_tree.heading("Item Code", text="Item Code", anchor=CENTER)
    main_tree.heading("Weight", text="Weight", anchor=CENTER)
    main_tree.heading("Grade", text="Grade", anchor=CENTER)
    main_tree.heading("Heat No", text="Heat No", anchor=CENTER)
    main_tree.heading("Quantity", text="Quantity", anchor=CENTER)
    main_tree.heading("Coverage", text="Coverage", anchor=CENTER)
    main_tree.heading("Remarks", text="Remarks", anchor=CENTER)

    # Create Striped Row Tags
    main_tree.tag_configure('oddrow', background="white")
    main_tree.tag_configure('evenrow', background="lightblue")

    def entered_tree(e):
        canvas.unbind_all("<MouseWheel>")

    def exit_tree(e):
        canvas.bind_all("<MouseWheel>", lambda ev: scrolled(ev))

    # Create buttons for the primary entries
    prim_frame = LabelFrame(sec_frame, text="Primary Commands")
    prim_frame.pack(fill=X, padx=20, pady=10)
    btn_add = Button(prim_frame, text="Add Record", command=add_prim_record)
    btn_update = Button(prim_frame, text="Update", command=update_prim_rec)
    btn_add.grid(row=0, column=0, padx=5, pady=5, ipadx=10)
    btn_update.grid(row=0, column=1, padx=5, pady=5, ipadx=10)

    main_tree.bind("<Enter>", entered_tree)
    main_tree.bind("<Leave>", exit_tree)
    main_tree.bind("<ButtonRelease-1>", select_record)
    canvas.bind("<Configure>", canvas_configure)
    # Bind mouse wheel for setting scrollbar on entering
    canvas.bind('<Enter>', lambda e: canvas.bind_all("<MouseWheel>", lambda ev: scrolled(ev)))
    canvas.bind('<Leave>', lambda e: canvas.unbind_all("<MouseWheel>"))
    cov_entry.unbind_class("TCombobox", "<MouseWheel>")
    btn_add_sec.bind("<Return>", lambda e: add_sec_record())
    btn_rt_details.bind("<Return>", lambda e: select_rt_details())
    root.bind("<F8>", view_dc)
    root.bind("<F9>", lambda e: update_prim_rec())

    if platform.system() != 'Windows' or platform.system() != 'Linux':
        sl_entry.bind('<KeyPress>', validate)
        dd_entry.bind("<KeyPress>", validate)
        cust_entry.bind("<KeyPress>", validate)
        sl2_entry.bind("<KeyPress>", validate)
        rt_no_entry.bind("<KeyPress>", validate)
        weight_entry.bind("<KeyPress>", validate)
        grade_entry.bind("<KeyPress>", validate)
        hn_entry.bind("<KeyPress>", validate)
        qty_entry.bind("<KeyPress>", validate)
        cov_entry.bind("<KeyPress>", validate)
        rem_entry.bind("<KeyPress>", validate)

    root.mainloop()
