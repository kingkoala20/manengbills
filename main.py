from datetime import datetime as dt

from pdf import PdfGenerator
from db import DB_Bills
import math


class Bayarin:
    
    paylist = [
        "Water",
        "Gas",
        "Electricity",
        "Rent"
    ]
    
    def __init__(self, period: str):
        self.bills = []
        self.period = period
    
    def split(self):
        self.bills = DB_Bills.fetch_period(period=self.period, path="bills.db")
        total = 0
        for b in self.bills:
            total += b[2]
        
        x, _ = [round(total/2)] * 2
        ineng = math.floor(x/1000)*1000
        manong = total - ineng
        
        return {"Manong": manong, "Ineng": ineng, "Total": total}
    
class Bill:
    
    def __init__(self, type, amt, period):
        
        """
            Bill object containing type, amount and period
        """
        
        self.type = type
        self.amt = amt
        self.period = period
        self.date_added = dt.now().strftime('%Y-%m-%d, %H:%M')
        DB_Bills.entry(self)
            
    
if __name__ == "__main__":
    """DB_Bills.gen_table("bills.db")
    DB_Bills.entry("bills.db", Bill("Electricity", 10000, "2/2023"))
    pdf = PdfGenerator("test")
    pdf.gen_report("3-23", [Bill("Electricity", 1000, "3-23"), Bill("Gas", 1000, "3-23")])"""
    
    today = dt.now()
    today_str = today.strftime("%m-%Y")
    
    DB_Bills.gen_table("bills.db")
    
    """electric = Bill("Electricity", 1000, today_str)
    gas = Bill("Gas", 3234, today_str)
    rent = Bill("Rent", 42340, today_str)"""
    
    gas = Bill("Gas", 1000, "02-2023")
    
                      