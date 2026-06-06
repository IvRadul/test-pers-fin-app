from finance_tracker.cli import build_parser
from tests.conftest import in_memory_conn

def test_parser_add():
    parser = build_parser()
    args = parser.parse_args(['add', 'expense', '150', '--category', 'Еда'])
    assert args.command == 'add'
    assert args.t_type == 'expense'
    assert args.amount == 150.0
    assert args.category == 'Еда'

def test_parser_list_defaults():
    parser = build_parser()
    args = parser.parse_args(['list'])
    assert args.category is None

def test_main_list_full(in_memory_conn, capsys):
    from finance_tracker.db import FinanceRepository
    from finance_tracker.cli import main
    repo = FinanceRepository(in_memory_conn)
    # Предварительно добавим запись через репозиторий
    from finance_tracker.models import Transaction
    repo.add(Transaction('income', 500, date='2026-02-15', category='Зарплата'))
    
    main(argv=['summary', '--year', '2026', '--month', '2'], rep=repo)
    captured = capsys.readouterr()
    assert 'Зарплата' in captured.out