import pytest
import sqlite3
from finance_tracker.db import FinanceRepository, create_connection

@pytest.fixture
def in_memory_conn():
    conn = create_connection(':memory:')
    yield conn
    conn.close()

@pytest.fixture
def repo(in_memory_conn):
    return FinanceRepository(in_memory_conn)