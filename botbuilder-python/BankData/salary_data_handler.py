from db_wrapper import BankDataWrapper
from intent_helper import convert_luis_intent_to_db_intent
from salary_details import SalaryDetails


class SalaryDataHandler:
    def __init__(
            self,
            db: BankDataWrapper,
    ):
        self.db = db


    def get_salary_text(self, db_intent, pay_type, salary):
        return "Your {} {} salary was={}".format(db_intent, pay_type, salary)

    def get_salary_info(self, salary_details: SalaryDetails):
        intent = salary_details.intent
        db_intent = convert_luis_intent_to_db_intent(intent)
        pay_type = self._find_salary_pay_type(salary_details)
        if pay_type == "both":
            both_pay_type_string = self.both_pay_type_string(db_intent)
            return both_pay_type_string
        else:
            salary_value = self.db.find_salary_data(db_intent, pay_type)
            return_string = self.get_salary_text( db_intent, pay_type, salary_value)
            return return_string

    def get_bonus_info(self):
        bonus_value = self.db.get_bonus()
        return_string = "Your last month bonus was={}".format(bonus_value)
        return return_string


    def both_pay_type_string(self, db_intent):
        salary_value_net = self.db.find_salary_data(db_intent, "net")
        salary_value_gross = self.db.find_salary_data(db_intent, "gross")
        string_net = self.get_salary_text(db_intent, "net", salary_value_net)
        string_gross = self.get_salary_text(db_intent, "gross",
                                            salary_value_gross)
        return_string = string_net + "\n" + string_gross
        return return_string

    def _find_salary_pay_type( self, salary_details):
        pay_type = ""
        if salary_details.gross:
            pay_type="gross"
        elif salary_details.net:
            pay_type = "net"
        elif salary_details.pay_type:
            fixed_pay_type = self._fix_user_pay_type_input(salary_details.pay_type)
            pay_type = fixed_pay_type
        return pay_type

    def _fix_user_pay_type_input(self, pay_type):
        return pay_type.lower()