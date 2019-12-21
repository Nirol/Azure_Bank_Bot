from db_intent_enum import DBIntent

from pay_type_enum import PayType
from salary_details import SalaryDetailsABS


class GeneralSalaryDetails(SalaryDetailsABS):
    def __init__(
            self,gross=None, net=None , pay_type=PayType.NONE,
            salary_type: DBIntent = None,

    ):
        super().__init__(gross, net, pay_type)
        self.salary_type = salary_type





