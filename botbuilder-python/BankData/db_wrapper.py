from abc import ABC, abstractmethod


class BankDataWrapper(ABC):
    def __init__(self, value):
        self.value = value
        super().__init__()

    @abstractmethod
    def get_bonus(self):
        pass

    @abstractmethod
    def find_salary_data(self, intent, pay_type ):
        pass