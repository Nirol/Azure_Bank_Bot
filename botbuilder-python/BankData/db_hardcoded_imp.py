from db_wrapper import BankDataWrapper
from intent_helper import DBIntent
from intent.enums.pay_type_enum import PayType

db_data = {
    'LAST': {'net': 17000, 'gross': 24000},
    'AVG': {'net': 16780.11, 'gross': 23671.23},
    'YTD': {'net': 76345, 'gross': 97612},
    'BONUS': {'LAST': 570}
}


class DBHardcoded(BankDataWrapper):
    def __init__(self):
        pass

    def get_bonus(self) -> float:
        res = db_data[DBIntent.BONUS.value][DBIntent.LAST.value]
        return res

    def find_salary_data(self, db_intent : DBIntent, pay_type:PayType) -> float:
        res = db_data[db_intent][pay_type.value]
        return res

