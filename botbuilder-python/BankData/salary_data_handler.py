from db_wrapper import BankDataWrapper
from intent_helper import DBIntent
from intent.enums.pay_type_enum import PayType



class SalaryDataHandler:
    def __init__(
            self,
            db: BankDataWrapper,
    ):
        self.db = db

    def find_salary_data(self, db_intent : DBIntent, pay_type : PayType) -> float:
        salary_value = self.db.find_salary_data(db_intent, pay_type)
        return salary_value



    def get_bonus_info(self) -> float:
        bonus_value = self.db.get_bonus()
        return bonus_value




