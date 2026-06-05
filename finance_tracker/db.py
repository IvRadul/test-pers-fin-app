import sqlite3
import datetime
from finance_tracker.models import Finance, Expense, Income
from datetime import date

def reg_adapters():
    ### Адаптеры datetime для sqlite3 в ISO формат и обратно
    # 1. Register an adapter to convert Python date/datetime to ISO strings
    def adapt_date_iso(val):
        """Adapt datetime.date to ISO 8601 date."""
        return val.isoformat()

    def adapt_datetime_iso(val):
        """Adapt datetime.datetime to ISO 8601 timestamp."""
        return val.isoformat()

    sqlite3.register_adapter(datetime.date, adapt_date_iso)
    sqlite3.register_adapter(datetime.datetime, adapt_datetime_iso)

    # 2. Register a converter to read strings back into Python objects
    def convert_date(val):
        """Convert ISO 8601 date to datetime.date object."""
        return datetime.date.fromisoformat(val.decode())

    def convert_timestamp(val):
        """Convert ISO 8601 timestamp to datetime.datetime object."""
        return datetime.datetime.fromisoformat(val.decode())

    sqlite3.register_converter("date", convert_date)
    sqlite3.register_converter("timestamp", convert_timestamp)

    # 3. Enable converter support when connecting
    con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)

#here we go
class FinanceRepository:
    def __init__(self, db_conn):
        self.conn = sqlite3.connect(db_conn)
        reg_adapters()
        self.conn.execute('''CREATE TABLE IF NOT EXISTS Expenses(
                    id INTEGER PRIMARY KEY,
                    amount INTEGER,
                    date DATE,
                    category TEXT)''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS Incomes(
                    id INTEGER PRIMARY KEY,
                    amount INTEGER,
                    date DATE,
                    category TEXT)''')
    
    def add(self, finance_elem):
        if isinstance(finance_elem, Expense):
            if finance_elem.id is None:
                cur = self.conn.execute(
                    "INSERT INTO Expenses (amount, date, category) VALUES (?, ?, ?)",
                    (finance_elem.amount, finance_elem.date, finance_elem.cat) 
                )
                finance_elem.id = cur.lastrowid
            else:
                self.conn.execute(
                    "UPDATE Expenses SET amount = ?, date = ?, category = ? WHERE id = ?",
                    (finance_elem.amount, finance_elem.date, finance_elem.cat, finance_elem.id) 
                )
            self.conn.commit()
        else:
            if finance_elem.id is None:
                cur = self.conn.execute(
                    "INSERT INTO Incomes (amount, date, category) VALUES (?, ?, ?)",
                    (finance_elem.amount, finance_elem.date, finance_elem.group) 
                )
                finance_elem.id = cur.lastrowid
            else:
                self.conn.execute(
                    "UPDATE Incomes SET amount = ?, date = ?, category = ? WHERE id = ?",
                    (finance_elem.amount, finance_elem.date, finance_elem.group, finance_elem.id) 
                )
            self.conn.commit()

    def delete(self, finance_elem):
        if isinstance(finance_elem, Expense):
            if finance_elem.id:
                self.conn.execute(
                    "DELETE FROM Expenses WHERE id = ?",
                    (finance_elem.id) 
                )
                self.conn.commit()
            else:
                raise KeyError(f"У записи {finance_elem} нет id")
        else:
            if finance_elem.id:
                self.conn.execute(
                    "DELETE FROM Incomes WHERE id = ?",
                    (finance_elem.id) 
                )
                self.conn.commit()
            else:
                raise KeyError(f"У записи {finance_elem} нет id")
                  
    def show_expenses(self, category):
        if category:
            data = self.conn.execute(
                "SELECT * FROM Expenses WHERE category = ?", (category)
            ).fetchall()
        else:
            data = self.conn.execute(
                "SELECT * FROM Expenses"
            ).fetchall()
        return data
    
    def show_incomes(self, category):
        if category:
            data = self.conn.execute(
                "SELECT * FROM Incomes WHERE category = ?", (category)
            ).fetchall()
        else:
            data = self.conn.execute(
                "SELECT * FROM Incomes"
            ).fetchall()
        return data
    
    def show_period(self, month, year):
        if not year:
            year = date.today().year
        if not month:
            month = date.today().month
        period = f"{year}-{month:02d}"
        data_e = self.conn.execute(
            "SELECT * FROM Expenses WHERE strftime('%Y-%m', date) = ?", (period,)
        ).fetchall()
        data_i = self.conn.execute(
            "SELECT * FROM Incomes WHERE strftime('%Y-%m', date) = ?", (period,)
        ).fetchall()
        return data_e + data_i
        
        