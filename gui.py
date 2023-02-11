from main import *
import tkinter
import customtkinter
from PIL import Image
from datetime import datetime as dt
import sqlite3

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

class BillsApp(customtkinter.CTk):
    
    width = "900"
    height = "600"
    
    current_period = dt.now().strftime("%m-%Y")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #--Initialization--
        DB_Bills.gen_table("bills.db")
        
        #--Event Handlers--
        
        def gen_pdf():
            pdf = PdfGenerator(filename=self.current_period)
            bayarin = Bayarin(self.current_period)
            pdf.gen_report(bayarin)
        
        #--Font--
    
        self.fstyle_heading = customtkinter.CTkFont(family="Lucida Bright", size=40, weight='bold')
        self.fstyle_footer = customtkinter.CTkFont(family="Times", size=15)
        
        #--Main Config--
        self.title("Maneng Bills")
        #self.geometry(f"{self.width}x{self.height}")
        #self.resizable(False, False)
        
        
        
        #--Widgets--
        self.heading = customtkinter.CTkLabel(self, font=self.fstyle_heading, text=f"Maneng Bills App")
        self.heading.grid(row=0, column=0, columnspan=2, stick="NSEW", pady=(20,10))
        
        self.entry_frame = EntryFrame(self, height=500, width=600, border_width=1)
        self.entry_frame.grid(row = 1, column = 0, padx=10, pady=10, sticky="NEWS")
        
        self.tools_frame = ToolsFrame(self, height=500, width=200, border_width=1)
        self.tools_frame.grid(row = 1, column = 1, padx=10, pady=10, sticky="NSEW")
        
        self.footer = customtkinter.CTkLabel(self, font=self.fstyle_footer, text=f"  Current Period: {self.current_period}")
        self.footer.grid(row=3, column=0, sticky="W")
        
        self.footer_pdf = customtkinter.CTkButton(self, text="Gen PDF", command=gen_pdf)
        self.footer_pdf.grid(row=3, column=1, sticky="E", padx=20, pady=10)
        
        
        #--Grid Config--
        self.columnconfigure(1,weight=1)
        self.rowconfigure(1, weight=1)
        
        
        
class EntryFrame(customtkinter.CTkFrame):
    
    
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        
        #--Fonts--
        
        self.fstyle_label = customtkinter.CTkFont(family="Lucida Bright", size=20)
        self.fstyle_button = customtkinter.CTkFont(family="Lucida Fax", size=18)
        
        #--Variable Handling---#
        
        self.amountvar = customtkinter.StringVar()
        self.typevar = customtkinter.StringVar()
        self.periodvar = customtkinter.StringVar(value=BillsApp.current_period)
        
        #-- Widgets --
        
        self.add_label = customtkinter.CTkLabel(self, text="Add Bill:", font=self.fstyle_label)
        self.add_label.grid(row=0, column=0, columnspan=2, pady=30)
        
        self.type_combo_label = customtkinter.CTkLabel(self, text="Bill Type: ", font=self.fstyle_label)
        self.type_combo_label.grid(row=1, column=0, padx=20, pady=10, sticky="WE")
        self.type_combo = customtkinter.CTkOptionMenu(self, values=[*Bayarin.paylist], variable=self.typevar)
        self.type_combo.grid(row=1, column=1, padx=20, pady=10)
        
        self.amount_label = customtkinter.CTkLabel(self, text="Amount: ", font=self.fstyle_label)
        self.amount_label.grid(row=2, column=0, padx=20, pady=10)
        self.amount_text = customtkinter.CTkEntry(self, width=100, placeholder_text="Enter Amount Here", textvariable=self.amountvar)
        self.amount_text.grid(row=2, column=1, padx=20, pady=10, sticky="WE")
        
        self.btn_add = customtkinter.CTkButton(self, width=150, text="Add", font=self.fstyle_button, command=self.gen_bill)
        self.btn_add.grid(row=3, column=0, columnspan=2, pady=20)
        
        self.status_label = customtkinter.CTkLabel(self, font=self.fstyle_button, text_color="red", text="")
        self.status_label.grid(row=4, column=0, columnspan = 2, pady=(20,10))
        
        
        
    # -- Event Methods --
    
    def gen_bill(self):
        type = self.typevar.get()
        amount = int(self.amountvar.get())
        period = self.periodvar.get()
        
        try:
            bill = Bill(type, amount, period)
            self.status_label.configure(text=f"{bill.type} entry added!")
            self.status_label.after(2000, self.empty_confirm)
            app.tools_frame.reload_table()
        except sqlite3.IntegrityError:
            self.status_label.configure(text=f"{type} entry exist for period {period}")
        
        
    def empty_confirm(self):
        self.status_label.configure(text="")
        
    
        
        
class ToolsFrame(customtkinter.CTkFrame):
    
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        
        #--Fonts--
        self.fstyle_label = customtkinter.CTkFont(family="Lucida Bright", size=20)
        self.fstyle_button = customtkinter.CTkFont(family="Lucida Fax", size=18)
        
        #--Widget--
        self.table_label = customtkinter.CTkLabel(self, text="Table Entries:", font=self.fstyle_label)
        self.table_label.pack(padx = 20, pady = 10)
        
        self.reload_btn = customtkinter.CTkButton(self, text="Reload", command=self.reload_table)
        self.reload_btn.pack(padx=20,)
        
        self.table_frame = DataViz(master=self)
        self.table_frame.pack(padx=10, pady=10)
           
    def reload_table(self):
        if self.table_frame:
            self.table_frame.destroy()
        self.table_frame = DataViz(master=self)
        self.table_frame.pack(padx=10, pady=10)
        
               
        
        

class DataViz(customtkinter.CTkFrame):
    
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        
        #-- Fonts --
        self.fstyle_header = customtkinter.CTkFont(family="Lucida Bright", weight="bold")
        
        #-- Table --
        with DB_Bills.db_con("bills.db") as c:
            c.execute("SELECT * from bills")
            entries = c.fetchall()
            
        headers = ("_","Bill Name", "Bill Amount", "Period", "Timestamp")
        entries.insert(0, headers)
        
        i=0
        for entry in entries:
            for col in range(1, len(entry)):
                e = customtkinter.CTkLabel(self, width=10, anchor="w", text=entry[col])
                if i == 0:
                    e.configure(font=(self.fstyle_header))
                e.grid(row=i, column=col-1, padx=10)
            i += 1
        

if __name__ == "__main__":
    app = BillsApp()
    app.mainloop()
    