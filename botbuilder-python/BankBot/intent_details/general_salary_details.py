from intent_details import IndentDetailsABS


class GeneralSalaryDetails(IndentDetailsABS):
    def __init__(
            self,
            gross: str = None,
            net: str = None,
            #pay_type used in case the user did not mention salary type in salary_net_gross_dialog.
            pay_type: str = None,
            salary_type: str = None,

    ):
        self.gross = gross
        self.net = net
        self.pay_type = pay_type
        self.salary_type = salary_type

    def update_entity(self, entity_name, entity_value):
        for attr in self.__dict__.items():
            if entity_name == attr:
                    self.__setattr__(attr, entity_value)





