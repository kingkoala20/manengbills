from fpdf import FPDF
import os
import webbrowser

class PdfGenerator:
    
    
    def __init__(self, filename):
        self.filename = filename + ".pdf"
    
    def gen_report(self, bayarin):
        
        period = bayarin.period
        
        pdf = FPDF(orientation="P", format="A4", unit="pt")
        
        pdf.add_page()
        pdf.image("graphics/house.png", w=40, h=40)
        pdf.set_font(family="Times", style="B", size=30)
        
        pdf.cell(w=0, h=50, txt="Maneng Bills {}".format(period), align="C", ln=1)
        pdf.cell(w=0, h=50, txt="", align="C", ln=1)
        
        pdf.set_font(family="Times", style="", size=18)
        
        bill_dic = bayarin.split()
        
        for bill in bayarin.bills:
            pdf.cell(w=150, h=30, txt=bill[1])
            pdf.cell(w=150, h=30, txt=str(bill[2])+" ¥", ln=1)
            
        pdf.cell(w=250, h=50, txt="Total Amount:")
        pdf.cell(w=0, h=50, txt=str(bill_dic["Total"])+" ¥", ln=1)
        
        pdf.set_font(family="Times", style="IB", size=20)
        pdf.cell(w=0, h=80, align="C", txt="Split: ", ln=1)
        
        pdf.set_font(family="Times", style="", size=18)
        pdf.cell(w=200, h=30, txt="Manong: ")
        pdf.cell(w=100, h=30, txt=str(bill_dic["Manong"])+" ¥", ln=1)
        pdf.cell(w=200, h=30, txt="Ineng: ")
        pdf.cell(w=100, h=30, txt=str(bill_dic["Ineng"])+" ¥", ln=1)
        
        
        os.chdir("reports")
        pdf.output(self.filename)
        webbrowser.open(self.filename)