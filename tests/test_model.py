from finance_tracker.models import Transaction
from datetime import date

def test_transaction_creation():
    tr = Transaction(trans_type='income', amount=1000, category='Зарплата')
    assert tr.trans_type == 'income'
    assert tr.amount == 1000
    assert tr.category == 'Зарплата'

def test_transaction_default_vals():
    tr = Transaction(trans_type='expense', amount=15000)
    assert tr.trans_type == 'expense'
    assert tr.amount == 15000
    assert tr.category == 'Other'
    assert tr.id == None

def test_creation_with_date():
    tr = Transaction(trans_type='income', amount=100000, date='12.11.2023')
    assert tr.trans_type == 'income'
    assert tr.amount == 100000
    assert tr.date == date(day=12, month=11, year=2023)