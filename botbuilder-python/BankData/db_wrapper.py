from abc import ABC, abstractmethod

from intent_helper import DBIntent
from intent.enums.pay_type_enum import PayType


class BankDataWrapper(ABC):
    def __init__(self, value):
        self.value = value
        super().__init__()

    @abstractmethod
    def get_bonus(self) -> float:
        pass

    @abstractmethod
    def find_salary_data(self, db_intent: DBIntent, pay_type : PayType ) -> float:
        pass