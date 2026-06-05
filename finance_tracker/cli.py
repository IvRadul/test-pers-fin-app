import argparse
from finance_tracker.db import FinanceRepository
from finance_tracker.models import Expense, Income
from finance_tracker.config import db_config

def build_parcer():
    parser = argparse.ArgumentParser(description="Личный финансовый учёт")
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

    parser_add = subparsers.add_parser('add', help="Добавить транзакцию")
    parser_add.add_argument('type', choices=['expense', 'income'], nargs='?', default="expense", help="Тип операции: доход(icome) или расход(expense)")
    parser_add.add_argument('amount', type=float, help="Сумма в рублях")
    parser_add.add_argument('--category', required=False, default="Другое", help="Категория операции (опционально)")
    parser_add.add_argument('--date', required=False)

    parser_list = subparsers.add_parser('list', help="Показать транзакции")
    parser_list.add_argument('type', choices=['expense', 'income'], nargs='?', default="expense", help="Тип операции: доход(icome) или расход(expense)")
    parser_list.add_argument('--category', help="Фильтр по категории")

    parser_summary = subparsers.add_parser('summary', help="Итоги по месяцам")
    parser_summary.add_argument('month', type=int, nargs='?', help="Месяц (1-12). Если не указан — текущий")
    parser_summary.add_argument('year', type=int, nargs='?', help="Год. Если не указан — текущий")
    
    return parser

def main():
    parser = build_parcer()
    args = parser.parse_args()
    rep = FinanceRepository(db_config())

    #Обработчик команд
    if args.command == 'add':
        if args.type == 'expense':
            new_transaction = Expense(amount=args.amount, cat=args.category)
        else:
            new_transaction = Income(amount=args.amount, group=args.category)
        rep.add(new_transaction)
        #return f"Добавляем: {args.type} {args.amount} руб., категория {args.category}"
    elif args.command == 'list':
        if args.type == 'expense':
            print(rep.show_expenses(args.category))
        else:
            print(rep.show_incomes(args.category))
        #print("Список транзакций" + (f" для категории {args.category}" if args.category else ""))
    elif args.command == 'summary':
        print(rep.show_period(args.month, args.year))
    else:
        parser.print_help()
