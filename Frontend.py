from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkcalendar import Calendar, DateEntry  # This as well
import sys  # Creating a new browse path
import os  # Obtaiing existing path
import Backend as bk
import exception_window
import pandas as pd
from datetime import date
import random
import psycopg2
from Backend import Database  # Import obiektu (klasy) Database z pliku database
from sqlalchemy import inspect

# Mikołaj Mrówka creds:

# db_string = "postgres://postgres:Mrowka1!@localhost:5432/shop_db"

# Sebastian Wach Credentials

user="postgres"
password="12345"
host="localhost"
db_name="shop_db2"
db_string = "postgresql://"+user+":"+password+"@"+host+"/"+db_name

# Rafał Kordaczek credentials:

# db_string = "postgresql://postgres:postgres@localhost:5432/postgres"


class Frontend:
    def __init__(self, master):
        self.master = master
        self.DatabaseBackend = bk.Database(db_string)  # FIXME: dodaj baze danych jako argument
        master.title("Database Food Management")
        master.geometry("1145x630")
        master.resizable(width=False, height=False)  # Disables changing dimensions of a window

        self.button_historical_data = tk.Button(master, text="Dane historyczne")
        # command=show_hist_window(read_json_data)
        # (NOTE A:)It appears, that giving 'self' argument in 'Refesh_data' is forbidden, since this metod
        # is called from the same class it belongs to.
        self.button_historical_data.place(x=380, y=550)

        self.filename_save = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\"  # Program default path
        self.filename_load = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\"
        self.filename_save = self.filename_save.replace("\\", "/")
        self.filename_load = self.filename_load.replace("\\", "/")
        # You can modify default save/load folder name here:
        self.filename_save = self.filename_save + "_measurements" + "/"
        self.filename_load = self.filename_load + "_measurements" + "/"
        # And insert it into the report field

        # Buffers used for validating entry values
        self.add_name = str()
        self.barcode = str()
        self.category = str()
        self.price = str()
        self.weight = str()
        self.quantity = str()
        self.hi_date = str()
        self.lo_date = str()
        self.exp_date = str()

        # Buffers used during operation
        self.data_records_buffer = pd.DataFrame([])
        self.query_buffer = str()

        # Label Frames
        self.lf_add_item = tk.LabelFrame(master, text="ADD NEW ITEM")
        self.lf_add_item.grid(row=0, column=0, columnspan=3, rowspan=6, sticky='NW', padx=1, pady=1, ipadx=1, ipady=1)
        self.lf_supply_batch = tk.LabelFrame(master, text="SUPPLY BATCH")
        self.lf_supply_batch.grid(row=0, column=3, columnspan=3, rowspan=6, sticky='NW', padx=1, pady=1, ipadx=1,
                                  ipady=1)
        self.lf_product_management = tk.LabelFrame(master, text="PRODUCT MANAGEMENT")
        self.lf_product_management.grid(row=0, column=7, columnspan=3, rowspan=6, sticky='NW', padx=1, pady=1, ipadx=1,
                                        ipady=1)
        self.lf_manage_supply = tk.LabelFrame(master, text="MANAGE SUPPLY")
        self.lf_manage_supply.grid(row=7, column=0, columnspan=6, rowspan=6, sticky='NW', padx=1, pady=1, ipadx=1,
                                   ipady=1)
        self.lf_report_generation = tk.LabelFrame(master, text="GENERATING REPORT")
        self.lf_report_generation.grid(row=7, column=9, columnspan=3, rowspan=6, sticky='NE', padx=1, pady=1, ipadx=1,
                                       ipady=1)

        # Scrollbar and table view
        self.tree = ttk.Treeview(master, selectmode='browse')
        self.tree.place(x=5, y=200, height=420)
        self.vsb = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        self.vsb.place(x=1120, y=200, height=420)
        self.tree["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8")
        self.tree['show'] = 'headings'
        self.tree.heading("1", text="Barcode")
        self.tree.heading("2", text="Name")
        self.tree.heading("3", text="Category")
        self.tree.heading("4", text="Expiration date")
        self.tree.heading("5", text="Price")
        self.tree.heading("6", text="Status")
        self.tree.heading("7", text="Weight")
        self.tree.heading("8", text="Quantity")
        self.tree.column("1", width=160, anchor='c')
        self.tree.column("2", width=200, anchor='c')
        self.tree.column("3", width=170, anchor='c')
        self.tree.column("4", width=150, anchor='c')
        self.tree.column("5", width=80, anchor='c')
        self.tree.column("6", width=150, anchor='c')
        self.tree.column("7", width=100, anchor='c')
        self.tree.column("8", width=100, anchor='c')
        self.tree.insert("", 'end', text="L1",
                         values=("Big1", "Best", "Ahjo1", "21-37-2137", "420.69", "Wasted", "123", "42"))

        # Labels for naming:
        self.l_add_name = tk.Label(self.lf_add_item, text='Name: ')
        self.l_add_name.grid(row=0, column=0, sticky=tk.NW)
        self.l_barcode = tk.Label(self.lf_add_item, text='Barcode: ')
        self.l_barcode.grid(row=1, column=0, sticky=tk.NW)
        self.l_category = tk.Label(self.lf_add_item, text='Category: ')
        self.l_category.grid(row=2, column=0, sticky=tk.NW)
        self.l_price = tk.Label(self.lf_add_item, text='Price: ')
        self.l_price.grid(row=3, column=0, sticky=tk.NW)
        self.l_supply_barcode = tk.Label(self.lf_supply_batch, text='Barcode: ')
        self.l_supply_barcode.grid(row=0, column=3, sticky=tk.NW)
        self.l_supply_expdate = tk.Label(self.lf_supply_batch, text='Expiration date: ')
        self.l_supply_expdate.grid(row=1, column=3, sticky=tk.NW)
        self.l_supply_quantity = tk.Label(self.lf_supply_batch, text='Quantity: ')
        self.l_supply_quantity.grid(row=2, column=3, sticky=tk.NW)
        self.l_supply_weight = tk.Label(self.lf_supply_batch, text='Weight: ')
        self.l_supply_weight.grid(row=3, column=3, sticky=tk.NW)
        self.l_prod_low_date = tk.Label(self.lf_product_management, text='Lower date: ')
        self.l_prod_low_date.grid(row=0, column=3, sticky=tk.NW)
        self.l_prod_high_date = tk.Label(self.lf_product_management, text='Upper date: ')
        self.l_prod_high_date.grid(row=1, column=3, sticky=tk.NW)
        self.l_prod_category = tk.Label(self.lf_product_management, text='Category: ')
        self.l_prod_category.grid(row=2, column=3, sticky=tk.NW)
        self.l_prod_name = tk.Label(self.lf_product_management, text='Name: ')
        self.l_prod_name.grid(row=3, column=3, sticky=tk.NW)
        self.l_manage_barcode = tk.Label(self.lf_manage_supply, text='Barcode: ')
        self.l_manage_barcode.grid(row=1, column=0, sticky=tk.NW)
        self.l_manage_weight = tk.Label(self.lf_manage_supply, text='Weight: ')
        self.l_manage_weight.grid(row=1, column=2, sticky=tk.NW)
        self.l_manage_quantity = tk.Label(self.lf_manage_supply, text='Quantity: ')
        self.l_manage_quantity.grid(row=1, column=4, sticky=tk.NW)

        # Entry fields:
        self.e_add_name = tk.Entry(self.lf_add_item, width=30, justify='left')
        self.e_add_name.grid(row=0, column=1, sticky=tk.NW)
        self.e_barcode = tk.Entry(self.lf_add_item, width=30, justify='left')
        self.e_barcode.grid(row=1, column=1, sticky=tk.NW)
        self.e_category = tk.Entry(self.lf_add_item, width=30, justify='left')
        self.e_category.grid(row=2, column=1, sticky=tk.NW)
        self.e_price = tk.Entry(self.lf_add_item, width=15, justify='left')
        self.e_price.grid(row=3, column=1, sticky=tk.NW)
        self.e_supply_barcode = tk.Entry(self.lf_supply_batch, width=30, justify='left')
        self.e_supply_barcode.grid(row=0, column=4, sticky=tk.NW)
        self.e_supply_exp_date = tk.Entry(self.lf_supply_batch, width=20, justify='left')
        self.e_supply_exp_date.grid(row=1, column=4, sticky=tk.NW)
        self.e_supply_quantity = tk.Entry(self.lf_supply_batch, width=15, justify='left')
        self.e_supply_quantity.grid(row=2, column=4, sticky=tk.NW)
        self.e_supply_weight = tk.Entry(self.lf_supply_batch, width=15, justify='left')
        self.e_supply_weight.grid(row=3, column=4, sticky=tk.NW)
        self.e_prod_low_date = tk.Entry(self.lf_product_management, width=20, justify='left')
        self.e_prod_low_date.grid(row=0, column=7, sticky=tk.NW)
        self.e_prod_hi_date = tk.Entry(self.lf_product_management, width=20, justify='left')
        self.e_prod_hi_date.grid(row=1, column=7, sticky=tk.NW)
        self.e_prod_category = tk.Entry(self.lf_product_management, width=30, justify='left')
        self.e_prod_category.grid(row=2, column=7, sticky=tk.NW)
        self.e_prod_name = tk.Entry(self.lf_product_management, width=30, justify='left')
        self.e_prod_name.grid(row=3, column=7, sticky=tk.NW)
        self.e_manage_barcode = tk.Entry(self.lf_manage_supply, width=30, justify='left')
        self.e_manage_barcode.grid(row=1, column=1, sticky=tk.NW)
        self.e_manage_weight = tk.Entry(self.lf_manage_supply, width=14, justify='left')
        self.e_manage_weight.grid(row=1, column=3, sticky=tk.NW)
        self.e_manage_quantity = tk.Entry(self.lf_manage_supply, width=14, justify='left')
        self.e_manage_quantity.grid(row=1, column=5, sticky=tk.NW)
        self.e_report_path = tk.Entry(self.lf_report_generation, width=60, justify='left')
        self.e_report_path.grid(row=1, column=1, sticky=tk.E)

        # Other Buttons
        self.b_add_item = tk.Button(self.lf_add_item, text="Add item", width=10, command=self.AddItem)
        self.b_add_item.grid(row=3, column=1, sticky=tk.NE)
        self.b_add_batch = tk.Button(self.lf_supply_batch, text="Add batch", width=10, command=self.SupplyBatch)
        self.b_add_batch.grid(row=3, column=4, sticky=tk.NE)
        self.b_sh_all_sup = tk.Button(self.lf_product_management, text="Show all supply", width=13,
                                      command=self.ShowAllSupply)
        self.b_sh_all_sup.grid(row=2, column=9, sticky=tk.NE)
        self.b_sh_sold_sup = tk.Button(self.lf_product_management, text="Show sold supply", width=15,
                                       command=self.ShowSoldSupply)
        self.b_sh_sold_sup.grid(row=1, column=9, sticky=tk.NE)
        self.b_sh_aval_sup = tk.Button(self.lf_product_management, text="Show avaliable supply", width=18,
                                       command=self.ShowAvSupply)
        self.b_sh_aval_sup.grid(row=0, column=9, sticky=tk.NE)
        self.b_sell_mng = tk.Button(self.lf_manage_supply, text="Sell item(s)", width=15, command=self.SellItem)
        self.b_sell_mng.grid(row=2, column=0, columnspan=2, sticky=tk.NW)
        self.b_wasted_mng = tk.Button(self.lf_manage_supply, text="Classify as wasted", width=18,
                                      command=self.MoveWasted)
        self.b_wasted_mng.grid(row=2, column=4, columnspan=2, sticky=tk.E)
        self.b_prod_low_date = tk.Button(self.lf_product_management, text='...', command=self.cal_init_1)
        self.b_prod_low_date.grid(row=0, column=8, sticky=tk.W)  # Lower date choice
        self.b_prod_hi_date = tk.Button(self.lf_product_management, text='...', command=self.cal_init_2)
        self.b_prod_hi_date.grid(row=1, column=8, sticky=tk.W)  # Higher date choice
        self.b_prod_exp_date = tk.Button(self.lf_supply_batch, text='...', command=self.cal_init_3)
        self.b_prod_exp_date.grid(row=1, column=5, sticky=tk.W)  # Expiration date choice
        # Save button
        self.button_save = tk.Button(self.lf_report_generation, text="Generate csv report", width=18,
                                     command=self.AddItem)  # FIXME
        self.button_save.grid(row=2, column=2, columnspan=2, sticky=tk.E)

        # Open button
        self.button_open = tk.Button(self.lf_report_generation, text="Open csv report", width=18,
                                     command=self.OpenReport)
        self.button_open.grid(row=2, column=1, sticky=tk.W)

        # Browse button
        self.b_button_load = tk.Button(self.lf_report_generation, text="Browse...", width=12, command=self.Browse)
        self.b_button_load.grid(row=1, column=3, sticky=tk.W)

        # Calendar entries

    def cal_init_1(self):
        top = tk.Tk()

        def print_sel():
            self.lo_date = cal.selection_get()
            self.e_prod_low_date.delete(0, tk.END)
            self.e_prod_low_date.insert(0, str(self.lo_date))
            top.destroy()
            type(self.lo_date)

        cal = Calendar(top,
                       font="Arial 14", selectmode='day',
                       cursor="hand1", year=2020, month=9, day=1)
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=print_sel).pack()

    def cal_init_2(self):
        top = tk.Tk()

        def print_sel():
            self.hi_date = cal.selection_get()
            self.e_prod_hi_date.delete(0, tk.END)
            self.e_prod_hi_date.insert(0, str(self.hi_date))
            top.destroy()

        cal = Calendar(top,
                       font="Arial 14", selectmode='day',
                       cursor="hand1", year=2020, month=9, day=1)
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=print_sel).pack()

    def cal_init_3(self):
        """Used for inserting an expiration date for batch supply"""
        top = tk.Tk()

        def print_sel():
            self.exp_date = cal.selection_get()
            self.e_supply_exp_date.delete(0, tk.END)
            self.e_supply_exp_date.insert(0, str(self.exp_date))
            top.destroy()

        cal = Calendar(top,
                       font="Arial 14", selectmode='day',
                       cursor="hand1", year=2020, month=9, day=1)
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=print_sel).pack()

    def QueryExecute(self):
        print("In development")

    def AddItem(self):
        # ALL BUFFERS should be initially RESET
        """During validation of entries ->
            add_name should contain chaaracters not exceeding ??
            category should contain chaaracters not exceeding ??
            price should be convertable to float, which value should not exceed 1000
            barcode should be convertable to int, and should not be negative

            psycopg2.errors.UniqueViolation - Exception for adding the same thing twice.
        """
        self.add_name = self.e_add_name.get()
        self.barcode = self.e_barcode.get()
        self.category = self.e_category.get()
        self.price = self.e_price.get()
        if self.barcode.isdecimal():
            try:
                self.price = float(self.price)
                if self.price <= 0:
                    exception_window.pop_up_window("Weight value must be positive!",
                                                   "ADD NEW ITEM EXCEPTION")
                else:
                    print("Carry on")
                    # Execute Backend command
                    try:
                        self.DatabaseBackend.add_product(self.barcode, self.add_name, self.category, self.price)
                    except:
                        exception_window.pop_up_window("The specified product has been already added!",
                                                       "ADD ITEM EXCEPTION")
            except ValueError:
                exception_window.pop_up_window("Weight must have a positive numerical value separated by dots (.)!",
                                               "ADD NEW ITEM EXCEPTION")
        else:
            exception_window.pop_up_window("Use only digits in Barcode entry!", "ADD NEW ITEM EXCEPTION")

    def SupplyBatch(self):
        # ALL BUFFERS should be initially RESET
        """During validation of entries ->
            barcode should be convertable to int, and should not be negative
            exp_date should be formatted according to calendar entry
                (thus, it should be validated in this regard, or should not be editable at all)
            quantity should be convertable to int, and should not be negative
            weight should be convertable to float, and should not be negative
                XOR - logic between variables quantity and weight
        """
        self.barcode = self.e_supply_barcode.get()
        # self.exp_date
        self.quantity = self.e_supply_quantity.get()
        self.weight = self.e_supply_weight.get()
        is_query_executable = 0
        if self.barcode.isdecimal():
            if len(self.quantity) > 0 or len(self.weight) > 0:
                if len(self.quantity) > 0 and len(self.weight) == 0:
                    try:
                        self.quantity = int(self.quantity)
                        if self.quantity > 0:
                            is_query_executable = 1
                            self.weight = 0
                        else:
                            exception_window.pop_up_window("Quantity value is not numeric", "SUPPLY BATCH EXCEPTION")
                    except ValueError:
                        exception_window.pop_up_window("Quantity value is not numeric", "SUPPLY BATCH EXCEPTION")
                elif len(self.quantity) == 0 and len(self.weight) > 0:
                    try:
                        self.weight = int(self.weight)
                        if self.weight > 0:
                            is_query_executable = 1
                            self.quantity = 0
                        else:
                            exception_window.pop_up_window("Weight value is not numeric",
                                                           "SUPPLY BATCH EXCEPTION")
                    except ValueError:
                        exception_window.pop_up_window("Weight value is not numeric", "SUPPLY BATCH EXCEPTION")
                if self.exp_date > date.today():
                    if is_query_executable == 1:
                        self.DatabaseBackend.import_supply('available', random.randint(1, 10000000), self.barcode,
                                                           str(self.exp_date), self.quantity, self.weight)
                    else:
                        exception_window.pop_up_window("The query is not allowed to execute", "SUPPLY BATCH EXCEPTION")
                else:
                    exception_window.pop_up_window("Invalid expiration date", "SUPPLY BATCH EXCEPTION")
            else:  # The are no data entered
                exception_window.pop_up_window("No data entered", "SUPPLY BATCH EXCEPTION")
            # Quantity and Weight specified, not float
            # Quantity specified, Weight not, not float
            # Weight specified, Quantity not, not float
            # Nothing specified,
            # Quantity and Weight specified, float
            # Quantity specified, Weight not, float
            # Weight specified, Quantity not, float
        else:
            exception_window.pop_up_window("Barcode should be decimal!", "SUPPLY BATCH EXCEPTION")

    def ShowAvSupply(self):
        # ALL BUFFERS should be initially RESET
        self.data_records_buffer = pd.DataFrame([])
        """During validation of entries ->
            prod_name should contain chaaracters not exceeding ??
            prod_category should contain chaaracters not exceeding ??
            e_prod_low_date should be formatted according to calendar entry
                (thus, it should be validated in this regard, or should not be editable at all)
            e_prod_hi_date should be formatted according to calendar entry
                (thus, it should be validated in this regard, or should not be editable at all)
            The Hi date must be larger than low date

            If only category is specified, the function should used any name
            We assume, that adding a category and name at the same time is pointless,
            so in that case, we take only name into account
        """
        try:
            if self.hi_date > self.lo_date:
                self.category = self.e_prod_category.get()
                self.add_name = self.e_prod_name.get()
                if len(self.category) > 0 and len(self.add_name) == 0 or len(self.category) == 0 and len(
                        self.add_name) > 0:
                    print("ShowAvSupply: GOOD!")
                    self.data_records_buffer = pd.from_dict(
                        self.DatabaseBackend.get_available_supply(self.lo_date, self.hi_date, self.category,
                                                                  self.add_name))
                    print(self.data_records_buffer)
                else:
                    exception_window.pop_up_window("Only Category or only Name can be inserted!",
                                                   "PRODUCT MANAGEMENT EXCEPTION")
            else:
                exception_window.pop_up_window("Invalid date constrains!", "PRODUCT MANAGEMENT EXCEPTION")
        except:
            exception_window.pop_up_window("Invalid date constrains! or entries", "PRODUCT MANAGEMENT EXCEPTION")

    def ShowSoldSupply(self):
        # ALL BUFFERS should be initially RESET
        self.data_records_buffer = pd.DataFrame([])
        """During validation of entries ->
            prod_name should contain chaaracters not exceeding ??
            prod_category should contain chaaracters not exceeding ??
            e_prod_low_date should be formatted according to calendar entry
                (thus, it should be validated in this regard, or should not be editable at all)
            e_prod_hi_date should be formatted according to calendar entry
                (thus, it should be validated in this regard, or should not be editable at all)
            The Hi date must be larger than low date

            If only category is specified, the function should used any name
            We assume, that adding a category and name at the same time is pointless,
            so in that case, we take only name into account
        """
        try:
            if self.hi_date > self.lo_date:
                self.category = self.e_prod_category.get()
                self.add_name = self.e_prod_name.get()
                if len(self.category) > 0 and len(self.add_name) == 0 or len(self.category) == 0 and len(
                        self.add_name) > 0:
                    print("Carry on")
                    self.data_records_buffer = self.DatabaseBackend.get_sold_supply(self.lo_date, self.hi_date,
                                                                                    self.category, self.add_name)
                    self.InsertData()
                    print(self.data_records_buffer)
                else:
                    exception_window.pop_up_window("Only Category or only Name can be inserted!",
                                                   "PRODUCT MANAGEMENT EXCEPTION")
            else:
                exception_window.pop_up_window("Invalid date constrains!", "PRODUCT MANAGEMENT EXCEPTION")
        except:
            exception_window.pop_up_window("Invalid date constrains! or entries", "PRODUCT MANAGEMENT EXCEPTION")

    def ShowAllSupply(self):
        # ALL BUFFERS should be initially RESET
        """During validation of entries ->
            prod_name should contain chaaracters not exceeding ??
            prod_category should contain chaaracters not exceeding ??
            e_prod_low_date should be formatted according to calendar entry
                (thus, it should be validated in this regard, or should not be editable at all)
            e_prod_hi_date should be formatted according to calendar entry
                (thus, it should be validated in this regard, or should not be editable at all)
            The Hi date must be larger than low date

            If only category is specified, the function should used any name
            We assume, that adding a category and name at the same time is pointless,
            so in that case, we take only name into account
        """
        print("ShowAllSupply: lo_Date" + str(self.lo_date) + "hi_date: " + str(self.hi_date))
        print(str(self.hi_date) > str(self.lo_date))
        try:
            if str(self.hi_date) > str(self.lo_date):
                print("ShowAllSupply: GOOD!")
                self.data_records_buffer = self.DatabaseBackend.get_all_supply(self.lo_date, self.hi_date,
                                                                               self.category, self.add_name)
                print("ShowAllSupply: VERY GOOD!")
                print(self.data_records_buffer)
                self.InsertData()
            else:
                exception_window.pop_up_window("Invalid date constrains!", "PRODUCT MANAGEMENT EXCEPTION",
                                               "PRODUCT MANAGEMENT EXCEPTION")
        except:
            exception_window.pop_up_window("Invalid date constrains! or entries", "PRODUCT MANAGEMENT EXCEPTION")

    def SellItem(self):
        # ALL BUFFERS should be initially RESET
        """During validation of entries ->
            barcode should be convertable to int, and should not be negative
            quantity should be convertable to int, and should not be negative
            weight should be convertable to float, and should not be negative
                XOR - logic between variables quantity and weight
        """
        self.barcode = self.e_manage_barcode.get()
        self.weight = self.e_manage_weight.get()
        self.quantity = self.e_manage_quantity.get()


        if self.barcode.isdecimal():
            print("Carry on")
        else:
            exception_window.pop_up_window("Use only digits in Barcode entry!", "MANAGE SUPPLY EXCEPTION")


        if not self.quantity and self.weight:
            try:
                self.weight = float(self.weight)
                if self.weight <= 0:
                    exception_window.pop_up_window("Weight value must be positive!",
                                                   "MANAGE SUPPLY EXCEPTION")
            except ValueError:
                exception_window.pop_up_window("Weight must have a positive numerical value separated by dots (.)!",
                                               "MANAGE SUPPLY EXCEPTION")
            sell_response = self.DatabaseBackend.sell_item(self.barcode, self.weight, self.quantity)
            print(sell_response)

        if self.quantity and not self.weight:

            if not self.quantity.isdecimal():
                exception_window.pop_up_window("Quantity must be a numerical value!", "MANAGE SUPPLY EXCEPTION")

            try:
                self.quantity = int(self.quantity)
                if self.quantity <= 0:
                    exception_window.pop_up_window("Quantity value must be positive!",
                                                   "MANAGE SUPPLY EXCEPTION")
            except ValueError:
                exception_window.pop_up_window("Quantity must have a positive numerical value!",
                                               "MANAGE SUPPLY EXCEPTION")
            sell_response = self.DatabaseBackend.sell_item(self.barcode, self.weight, self.quantity)
            print(sell_response)

        if self.quantity and self.weight:
            exception_window.pop_up_window(
                "Do not enter both values weight and quantity!",
                "MANAGE SUPPLY EXCEPTION")
        if not self.quantity and not self.weight:
            exception_window.pop_up_window(
                "Enter the quantity or weight of the product! Please do not enter both values!",
                "MANAGE SUPPLY EXCEPTION")



    def MoveWasted(self):
        """During validation of entries ->
            barcode should be convertable to int, and should not be negative
            quantity should be convertable to int, and should not be negative
            weight should be convertable to float, and should not be negative
                XOR - logic between variables quantity and weight
        """
        self.barcode = self.e_manage_barcode.get()
        self.weight = self.e_manage_weight.get()
        self.quantity = self.e_manage_quantity.get()


        if self.barcode.isdecimal():
            print("Carry on")
        else:
            exception_window.pop_up_window("Use only digits in Barcode entry!", "MANAGE SUPPLY EXCEPTION")


        if not self.quantity and self.weight:
            try:
                self.weight = float(self.weight)
                if self.weight <= 0:
                    exception_window.pop_up_window("Weight value must be positive!",
                                                   "MANAGE SUPPLY EXCEPTION")
            except ValueError:
                exception_window.pop_up_window("Weight must have a positive numerical value separated by dots (.)!",
                                               "MANAGE SUPPLY EXCEPTION")
            wasted_response = self.DatabaseBackend.classify_as_wasted(self.barcode, self.weight, self.quantity)
            print(wasted_response)

        if self.quantity and not self.weight:

            if not self.quantity.isdecimal():
                exception_window.pop_up_window("Quantity must be a numerical value!", "MANAGE SUPPLY EXCEPTION")

            try:
                self.quantity = int(self.quantity)
                if self.quantity <= 0:
                    exception_window.pop_up_window("Quantity value must be positive!",
                                                   "MANAGE SUPPLY EXCEPTION")
            except ValueError:
                exception_window.pop_up_window("Quantity must have a positive numerical value!",
                                               "MANAGE SUPPLY EXCEPTION")
            wasted_response = self.DatabaseBackend.classify_as_wasted(self.barcode, self.weight, self.quantity)
            print(wasted_response)

        if self.quantity and self.weight:
            exception_window.pop_up_window(
                "Do not enter both values weight and quantity!",
                "MANAGE SUPPLY EXCEPTION")
        if not self.quantity and not self.weight:
            exception_window.pop_up_window(
                "Enter the quantity or weight of the product! Please do not enter both values!",
                "MANAGE SUPPLY EXCEPTION")

    def OpenReport(self):
        """
            No mechanism of overwirting existing file - maybe there is a way to check this
        """
        self.filename_load = tk.filedialog.askopenfilename(initialdir=self.filename_load, title="Open report",
                                                           filetypes= \
                                                               (("csv files", "*.csv"), ("all files", "*.*")))
        try:
            if self.filename_load[-1] == '/':
                exception_window.pop_up_window("Nie wybrano pliku!", "Wczytaj plik")
            print("Load path: " + self.filename_load)
            # else:
            #     self.filename_load = self.filename_load + '.csv'
            if (self.filename_load[-3:] == 'csv'):
                print("Go on")
            else:
                exception_window.pop_up_window("Należy podać scieżkę oraz nazwę pliku")
        except IndexError:
            print("OpenReport: FYI - open path to file wasn't specified!")

    def Browse(self):
        """
            No mechanism of overwirting existing file - maybe there is a way to check this
        """
        self.filename_save = tk.filedialog.asksaveasfilename(initialdir=self.filename_save, title="Zapisz jako",
                                                             filetypes= \
                                                                 (("csv files", "*.csv"), ("all files", "*.*")))
        if self.filename_save[-3:] == 'csv':
            print("Save path: " + self.filename_save)
        elif len(self.filename_save) < 3:
            print("Browse: FYI - open path to file wasn't specified!")
        else:
            self.filename_save = self.filename_save + '.csv'
            print("Save path: " + self.filename_save)

    def InsertData(self):
        """Here the loaded data, of the data form a given quiery will be pended to the tree (table)
            There might be an issue with empty records - pandas dataframes usually perceive them as nans,
             but we will see how it will go.
        """

        for i in self.tree.get_children():  # This is how it should be reset
            self.tree.delete(i)
        # Based on the dataframe (from pandas), following records should be inserted into the table
        for j in range(len(self.data_records_buffer)):  # This is how it should be reset
            self.tree.insert("", 'end', text="L1", values=(
                self.data_records_buffer[j]['barcode'], self.data_records_buffer[j]['name'],
                self.data_records_buffer[j]['category'], self.data_records_buffer[j]['expiration_date'],
                self.data_records_buffer[j]['price'], self.data_records_buffer[j]['status'],
                self.data_records_buffer[j]['weight'], self.data_records_buffer[j]['quantity']))


if __name__ == "__main__":
    root = tk.Tk()  # must be running, when adding an image.
    # ---------Reading json file in a loop

    my_gui = Frontend(root)
    # my_gui.combobox_choice(root)
    # my_gui.building_chosen(root)
    # my_gui.refresh_labels()

    root.mainloop()
