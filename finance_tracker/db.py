import sqlite3
import datetime
from finance_tracker.models import Transaction
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

def create_connection(db_path):
    #поддержка типов для работы адаптеров
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")

    #регистрируем адаптеры
    reg_adapters()

    #создание таблицы (если её нет)
    conn.execute('''CREATE TABLE IF NOT EXISTS Transactions(
                    id INTEGER PRIMARY KEY,
                    type TEXT,
                    amount INTEGER,
                    date DATE,
                    category TEXT)''')
    conn.commit()
    return conn

#here we go
class FinanceRepository:
    def __init__(self, connection):
        self.conn = connection
    
    def add(self, finance_elem):
        if isinstance(finance_elem, Transaction):
            if finance_elem.id is None:
                cur = self.conn.execute(
                    "INSERT INTO Transactions (type, amount, date, category) VALUES (?, ?, ?, ?)",
                    (finance_elem.trans_type, finance_elem.amount, finance_elem.date, finance_elem.category) 
                )
                finance_elem.id = cur.lastrowid
            else:
                self.conn.execute(
                    "UPDATE Transactions SET type = ?, amount = ?, date = ?, category = ? WHERE id = ?",
                    (finance_elem.trans_type, finance_elem.amount, finance_elem.date, finance_elem.category, finance_elem.id) 
                )
            self.conn.commit()
            
    def delete(self, finance_elem):
        if isinstance(finance_elem, Transaction):
            if finance_elem.id:
                self.conn.execute(
                    "DELETE FROM Transactions WHERE id = ?",
                    (finance_elem.id) 
                )
                self.conn.commit()
            else:
                raise KeyError(f"У записи {finance_elem} нет id")
        else:
            pass
                  
    def show_transactions(self, transaction_type=None, category=None):
        if category:
            data = self.conn.execute(
                "SELECT * FROM Transactions WHERE category = ?", (category)
            ).fetchall()
        else:
            data = self.conn.execute(
                "SELECT * FROM Transactions"
            ).fetchall()
        return data
    
    def show_period(self, month=None, year=None):
        if year is None and month is None:
            year = date.today().year
            month = date.today().month
        if year is None:
            year = date.today().year

        if month:
            period = f"{year}-{month:02d}"
            data = self.conn.execute(
                "SELECT * FROM Transactions WHERE strftime('%Y-%m', date) = ?", (period,)
            ).fetchall()
        else:
            period = f"{year}"
            data = self.conn.execute(
                "SELECT * FROM Transactions WHERE strftime('%Y', date) = ?", (period,)
            ).fetchall()
        return data
        
        