from intent_details import IndentDetailsABS
from intent_helper import Intent


class SalaryDetails(IndentDetailsABS):
    def __init__(
            self,
            gross: str = None,
            net: str = None,
            #pay_type used in case the user did not mention salary type in salary_net_gross_dialog.
            pay_type: str = None,
            unsupported_actions=None,
            intent: Intent = None,
    ):
        if unsupported_actions is None:
            unsupported_actions = []
        self.gross = gross
        self.net = net
        self.pay_type = pay_type
        self.intent = intent
        self.unsupported_actions = unsupported_actions

    def update_entity(self, entity_name, entity_value):
        self.__dict__[entity_name] = entity_value






