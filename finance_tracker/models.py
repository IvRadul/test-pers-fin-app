import datetime

class Transaction:
    def __init__(self, trans_type, amount, category='Other', date=datetime.date.today(), id=None):
        self._id = id
        self.trans_type = trans_type
        self.amount = amount
        self.category = category
        self.date = date

    @property 
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def amount(self):
        return self._amount
    
    @amount.setter
    def amount(self, some_amount):
        if isinstance(some_amount, (int, float)):
            if some_amount < 0:
                raise ValueError("Запись не может быть отрицательной")
            self._amount = some_amount
        else:
            raise TypeError(f"{some_amount} не является числом")
        
    @property
    def trans_type(self):
        return self._trans_type
    
    @trans_type.setter
    def trans_type(self, t_type):
        if t_type in ('income', 'expense'):
            self._trans_type = t_type
        else:
            raise TypeError(f"{t_type} не явялется типом income или expense")

    @property 
    def date(self):
        return self._date
    
    @date.setter
    def date(self, record_date):
        if isinstance(record_date, datetime.date):
            self._date = record_date
        elif isinstance(record_date, str):
            for s in ("%Y-%m-%d", "%d.%m.%Y"):
                try:
                    self._date = datetime.date.strptime(record_date, s)
                    break
                except ValueError:
                    continue
            else:
                raise ValueError(f"Не удалось распознать дату: '{record_date}'.Используйте форматы YYYY-MM-DD или DD.MM.YYYY")
        elif isinstance(record_date, (int, float)):
            self._date = datetime.date.fromtimestamp(record_date)
        else:
            raise TypeError(f"Неподдерживаемый тип {type(record_date)}."
                            "Ожидается str, int, float, date")
        
    
