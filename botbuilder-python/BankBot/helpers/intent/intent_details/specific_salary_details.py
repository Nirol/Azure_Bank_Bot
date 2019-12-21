from intent_details import IndentDetailsABS
from intent_helper import Intent
from pay_type_enum import PayType
from salary_details import SalaryDetailsABS


class SpecificSalaryDetails(SalaryDetailsABS):
    def __init__(
            self,gross=None, net=None , pay_type=PayType.NONE,
            unsupported_actions=None,
            intent: Intent = None
    ):
        super().__init__(gross, net, pay_type)
        if unsupported_actions is None:
            unsupported_actions = []
        self.intent = intent
        self.unsupported_actions = unsupported_actions








