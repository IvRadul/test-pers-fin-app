import argparse
from finance_tracker.db import FinanceRepository, create_connection
from finance_tracker.models import Transaction
from finance_tracker.config import db_config, csv_config
from finance_tracker.tables import export_to_csv
from rich.console import Console
from rich.table import Table

def show_table(data):
    console = Console()

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Тип операции")
    table.add_column("Сумма", justify="right")
    table.add_column("Дата")
    table.add_column("Категория", justify="right")
    for row in data:
        new_row = list(map(str, row))
        table.add_row(*new_row)
    console.print(table)

def build_parser():
    parser = argparse.ArgumentParser(description="Личный финансовый учёт")
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

    parser_add = subparsers.add_parser('add', help="Добавить транзакцию")
    parser_add.add_argument('t_type', choices=['expense', 'income'], nargs='?', default="expense", help="Тип операции: доход(icome) или расход(expense)")
    parser_add.add_argument('amount', type=float, help="Сумма в рублях")
    parser_add.add_argument('--category', required=False, default="Другое", help="Категория операции (опционально)")
    parser_add.add_argument('--date', required=False)

    parser_list = subparsers.add_parser('list', help="Показать транзакции")
    parser_list.add_argument('t_type', choices=['expense', 'income'], nargs='?', default="expense", help="Тип операции: доход(icome) или расход(expense)")
    parser_list.add_argument('--category', help="Фильтр по категории")

    parser_summary = subparsers.add_parser('summary', help="Итоги по месяцам")
    parser_summary.add_argument('--month', type=int, help="Месяц (1-12). Если не указан — текущий")
    parser_summary.add_argument('--year', type=int, help="Год. Если не указан — текущий")

    parser_export = subparsers.add_parser('export', help="Экспорт транзакций")
    parser_export.add_argument('format', choices=['csv'])
    parser_export.add_argument('--output', help="Имя файла (без расширения)")
    parser_export.add_argument('--category')
    parser_export.add_argument('--year', type=int)
    parser_export.add_argument('--month', type=int)
    
    return parser

def main(argv=None, rep=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if rep is None:
        conn = create_connection(db_config())
        rep = FinanceRepository(conn)
        own_conn = True
    else:
        own_conn = False

    try:
    #Обработчик команд
        if args.command == 'add':
            new_transaction = Transaction(trans_type=args.t_type, amount=args.amount, category=args.category, date=args.date)
            rep.add(new_transaction)
        elif args.command == 'list':
            show_table(rep.show_transactions(args.category))
        elif args.command == 'summary':
            show_table(rep.show_period(args.month, args.year))
        elif args.command == 'export':
            export_to_csv(csv_config(), rep.show_transactions(args.category))
        else:
            parser.print_help()
    finally:
        if own_conn and rep.conn:
            rep.conn.close()