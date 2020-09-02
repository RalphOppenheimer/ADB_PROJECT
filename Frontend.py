from tkinter import ttk
import tkinter as tk
from tkcalendar import Calendar, DateEntry #This as well

def cal_init_1():
    def print_sel():
        print(cal.selection_get())

    top = tk.Toplevel(root)

    cal = Calendar(top,
                   font="Arial 14", selectmode='day',
                   cursor="hand1", year=2018, month=2, day=5)
    cal.pack(fill="both", expand=True)
    ttk.Button(top, text="ok", command=print_sel).pack()

class Frontend:
    def __init__(self, master):
        self.master = master
        master.title("Database Food Management")
        master.geometry("1145x630")
        master.resizable(width=False, height=False) #Disables changing dimensions of a window

        self.button_historical_data = tk.Button(master, text="Dane historyczne")
        # command=show_hist_window(read_json_data)
        # (NOTE A:)It appears, that giving 'self' argument in 'Refesh_data' is forbidden, since this metod
        # is called from the same class it belongs to.
        self.button_historical_data.place(x=380, y=550)

        # Label Frames
        self.lf_add_item = tk.LabelFrame(master, text="ADD NEW ITEM")
        self.lf_add_item.grid(row=0, column=0, columnspan=3, rowspan=6, sticky='NW', padx=1, pady=1, ipadx=1, ipady=1)
        self.lf_supply_batch = tk.LabelFrame(master, text="SUPPLY BATCH")
        self.lf_supply_batch.grid(row=0, column=3, columnspan=3, rowspan=6, sticky='NW', padx=1, pady=1, ipadx=1, ipady=1)
        self.lf_product_management = tk.LabelFrame(master, text="PRODUCT MANAGEMENT")
        self.lf_product_management.grid(row=0, column=7, columnspan=3, rowspan=6, sticky='NW', padx=1, pady=1, ipadx=1, ipady=1)
        self.lf_manage_supply = tk.LabelFrame(master, text="MANAGE SUPPLY")
        self.lf_manage_supply.grid(row=7, column=0, columnspan=6, rowspan=6, sticky='NW', padx=1, pady=1, ipadx=1, ipady=1)
        self.lf_report_generation= tk.LabelFrame(master, text="GENERATING REPORT")
        self.lf_report_generation.grid(row=7, column=9, columnspan=3, rowspan=6, sticky='NE', padx=1, pady=1, ipadx=1, ipady=1)

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
        self.tree.insert("",'end',text="L1",values=("Big1","Best", "Ahjo1"))

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
        self.l_prod_high_date= tk.Label(self.lf_product_management, text='Upper date: ')
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
        self.b_add_item = tk.Button(self.lf_add_item, text="Add item", width=10)
        self.b_add_item.grid(row=3, column=1, sticky=tk.NE)
        self.b_add_batch = tk.Button(self.lf_supply_batch, text="Add batch", width=10)
        self.b_add_batch.grid(row=3, column=4, sticky=tk.NE)
        self.b_sh_all_sup = tk.Button(self.lf_product_management, text="Show all supply", width=13)
        self.b_sh_all_sup.grid(row=2, column=9, sticky=tk.NE)
        self.b_sh_sold_sup = tk.Button(self.lf_product_management, text="Show sold supply", width=15)
        self.b_sh_sold_sup.grid(row=1, column=9, sticky=tk.NE)
        self.b_sh_aval_sup = tk.Button(self.lf_product_management, text="Show avaliable supply", width=18)
        self.b_sh_aval_sup.grid(row=0, column=9, sticky=tk.NE)
        self.b_sell_mng = tk.Button(self.lf_manage_supply, text="Sell item(s)", width=15)
        self.b_sell_mng.grid(row=2, column=0, columnspan=2, sticky=tk.NW)
        self.b_wasted_mng = tk.Button(self.lf_manage_supply, text="Classify as wasted", width=18)
        self.b_wasted_mng.grid(row=2, column=4, columnspan=2, sticky=tk.E)
        self.b_prod_low_date = tk.Button(self.lf_product_management, text='...', command=self.cal_init_1)
        self.b_prod_low_date.grid(row=0, column=8, sticky=tk.W)
        self.b_prod_hi_date = tk.Button(self.lf_product_management, text='...', command=self.cal_init_2)
        self.b_prod_hi_date.grid(row=1, column=8, sticky=tk.W)
        # Save button
        self.button_save = tk.Button(self.lf_report_generation, text="Generate csv report", width=18)
        self.button_save.grid(row=2, column=2, columnspan=2, sticky=tk.E)

        # Open button
        self.button_open = tk.Button(self.lf_report_generation, text="Open csv report", width=18)
        self.button_open.grid(row=2, column=1, sticky=tk.W)

        # Browse button
        self.b_button_load = tk.Button(self.lf_report_generation, text="Browse...", width=12)
        self.b_button_load.grid(row=1, column=3, sticky=tk.W)

        # Calendar entries
        # self.cal = DateEntry(root_3, width=12, background='darkblue', date_pattern='yyyy-mm-dd',
        #                      foreground='white', borderwidth=2)
        # self.cal.pack(side=tk.LEFT, expand=True)

    def cal_init_1(self):
        top = tk.Tk()
        def print_sel():
            print(cal.selection_get())
            self.e_prod_low_date.delete(0, tk.END)
            self.e_prod_low_date.insert(0, str(cal.selection_get()))
            top.destroy()

        cal = Calendar(top,
                       font="Arial 14", selectmode='day',
                       cursor="hand1", year=2020, month=9, day=1)
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=print_sel).pack()

    def cal_init_2(self):
        top = tk.Tk()
        def print_sel():
            print(cal.selection_get())
            self.e_prod_hi_date.delete(0, tk.END)
            self.e_prod_hi_date.insert(0, str(cal.selection_get()))
            top.destroy()

        cal = Calendar(top,
                       font="Arial 14", selectmode='day',
                       cursor="hand1", year=2020, month=9, day=1)
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=print_sel).pack()


if __name__ == "__main__":
    root = tk.Tk()  # must be running, when adding an image.
    # ---------Reading json file in a loop

    my_gui = Frontend(root)
    #my_gui.combobox_choice(root)
    #my_gui.building_chosen(root)
    #my_gui.refresh_labels()

    root.mainloop()