from abc import ABC, abstractmethod

from intent.enums.pay_type_enum import PayType
from intent_details import IndentDetailsABS


class SalaryDetailsABS(IndentDetailsABS):
    def __init__(self,
                 gross: str = None,
                 net: str = None,
                 # pay_type used in case the user did not mention salary type in salary_net_gross_dialog.
                 pay_type: PayType = None, ):
        self.gross = gross
        self.net = net
        self.pay_type = pay_type


def update_pay_type(salary_detail : SalaryDetailsABS):
    if salary_detail.gross != None:
        salary_detail.pay_type=PayType.GROSS
    if salary_detail.net != None:
        salary_detail.pay_type=PayType.NET