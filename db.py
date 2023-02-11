from contextlib import contextmanager
import sqlite3
import json


class DB_Bills:
    
    @contextmanager
    def db_con(path="bills.db"):
        conn = sqlite3.Connection(path)
        cur = conn.cursor()
        yield cur
        conn.commit()
        conn.close()
        
    def gen_table(path="bills.db"):
        clause = """
            CREATE TABLE IF NOT EXISTS bills(
                bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_name TEXT NOT NULL,
                bill_amt INTEGER NOT NULL,
                period TEXT NOT NULL,
                date_added TEXT NOT NULL,
                UNIQUE (bill_name, period)
            )
        """
        
        with DB_Bills.db_con(path) as c:
            c.execute(clause)
            
    def entry(payload, path="bills.db"):
        clause = """
            INSERT INTO bills(bill_name, bill_amt, period, date_added)
            VALUES({})
        """
        
        with DB_Bills.db_con(path) as c:
            c.execute(clause.format(json.dumps(payload.type) + ", " + str(payload.amt) + ", " + json.dumps(payload.period)+ ", " + json.dumps(payload.date_added)))
            
    def fetch_period(period, path="bills.db"):
        clause = """
            SELECT * FROM bills
            WHERE period = '{}'
        """
        
        with DB_Bills.db_con(path) as c:
            c.execute(clause.format(period))
            return c.fetchall()
        
    def fetch_type_year(type, year, path="bills.db"):
        
        clause = """
            SELECT * FROM bills
            WHERE bill_name = '{}' AND CAST(SUBSTR(period, 4) AS INTEGER) >= {}
        """
        
        
        
        with DB_Bills.db_con(path) as c:
            c.execute(clause.format(type, year))
            return c.fetchall()
            