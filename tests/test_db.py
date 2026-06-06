from tests.conftest import repo
from finance_tracker.models import Transaction

def test_add_tr(repo):
    tr = Transaction(trans_type="expense", amount=1000)
    repo.add(tr)
    rows = repo.show_transactions()
    assert len(rows) == 1

def test_add_some_tr(repo):
    tr_list = []
    tr_list.append(Transaction(trans_type="expense", amount=1000))
    tr_list.append(Transaction(trans_type="income", amount=3000))
    tr_list.append(Transaction(trans_type="income", amount=100))
    tr_list.append(Transaction(trans_type="expense", amount=10000))
    for tr in tr_list:
        repo.add(tr)
    rows = repo.show_transactions()
    assert len(rows) == 4

def test_show_today(repo):
    tr_list = []
    tr_list.append(Transaction(trans_type="expense", amount=1000))
    tr_list.append(Transaction(trans_type="income", amount=3000))
    tr_list.append(Transaction(trans_type="income", amount=100))
    tr_list.append(Transaction(trans_type="expense", amount=10000))
    for tr in tr_list:
        repo.add(tr)
    rows = repo.show_period()
    assert len(rows) == 4

def test_some_dates(repo):
    tr_list = []
    tr_list.append(Transaction(trans_type="expense", amount=1000, date="14.03.2026"))
    tr_list.append(Transaction(trans_type="income", amount=3000, date="12.11.2025"))
    tr_list.append(Transaction(trans_type="income", amount=100))
    tr_list.append(Transaction(trans_type="expense", amount=10000))
    for tr in tr_list:
        repo.add(tr)
    rows = repo.show_period()
    rows_2025 = repo.show_period(year=2025)
    assert len(rows) == 2
    assert len(rows_2025) == 1