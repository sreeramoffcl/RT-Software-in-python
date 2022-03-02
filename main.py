from tkinter import *
import sqlite3
import CRM
import PM

root = Tk()
root.title("Menu")
root.geometry("700x300")

# Database setup
conn_mast = sqlite3.connect("masters.db")
cursor_mast = conn_mast.cursor()

cursor_mast.execute("""CREATE TABLE if not exists prod_master (
    prod_code text,
    item_code text,
    draw_no text,
    desc text,
    weight real
)
""")

cursor_mast.execute("""CREATE TABLE if not exists cust_master (
        cust_code text,
        cust_name text,
        add_1 text,
        add_2 text,
        add_3 text,
        city text,
        district text,
        pincode text,
        gst text,
        pan text,
        remarks text
    )
    """)
conn_mast.commit()
conn_mast.close()

conn_trans = sqlite3.connect("transactions.db")
cursor_trans = conn_trans.cursor()
cursor_trans.execute("""CREATE TABLE if not exists mat_inw_prim (
        sl_no text,
        customer text,
        dc_no text,
        dc_date text
    )
    """)
cursor_trans.execute("""CREATE TABLE if not exists mat_inw_sec (
        uid text,
        sl_no text,
        rt_no text,
        prod text,
        ic text,
        weight real,
        grade text,
        heat_no text,
        qty text,
        coverage text,
        remarks text
    )
    """)
conn_trans.commit()
conn_trans.close()


def prod_master():
    PM.run_pm()


def cust_master():
    CRM.run_crm()


def masters():
    menu = Toplevel()
    menu.title("Masters")
    menu.geometry("400x200")
    btn_prod_mas = Button(menu, text="Product Master", command=prod_master)
    btn_prod_mas.pack(padx=20, pady=10, ipadx=20)
    btn_cus_mas = Button(menu, text="Customer Master", command=cust_master)
    btn_cus_mas.pack(padx=20, pady=10, ipadx=15)
    btn_exit = Button(menu, text="Exit", command=menu.destroy)
    btn_exit.pack(padx=20, pady=10, ipadx=60)


def transactions():
    menu = Toplevel()
    menu.title("Transactions")
    btn_prod_mas = Button(menu, text="Material Inward")
    btn_prod_mas.pack(padx=20, pady=10, ipadx=20)
    btn_cus_mas = Button(menu, text="Material Outward")
    btn_cus_mas.pack(padx=20, pady=10, ipadx=15)
    btn_exit = Button(menu, text="Exit", command=menu.destroy)
    btn_exit.pack(padx=20, pady=10, ipadx=60)


# Create frame for buttons
main_frame = Frame(root)
main_frame.pack()

# Create buttons
btn_masters = Button(main_frame, text="Masters", command=masters)
btn_masters.pack(padx=20, pady=10, ipadx=30)
btn_trans = Button(main_frame, text="Transactions", command=transactions)
btn_trans.pack(padx=20, pady=10, ipadx=15)
btn_exit = Button(main_frame, text="Exit", command=root.destroy)
btn_exit.pack(padx=20, pady=10, ipadx=45)


root.mainloop()
