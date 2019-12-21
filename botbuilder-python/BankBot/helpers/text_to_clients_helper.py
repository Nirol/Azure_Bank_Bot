from enum import Enum
from intent_helper import DBIntent
from intent.enums.pay_type_enum import PayType


class PromptMessage(Enum):
    ENTRY_MSG = "Welcome to BankBot !, What can I help you with?"
    SALARY_TYPE_PROMPT_MSG = "Would you prefer viewing TOTAL salary data or AVG/LAST/YTD ?"
    PAY_TYPE_MSG = "Please specify if the salary is net, gross  or both:"
    WHAT_ELSE_MSG = "What else can I do for you?"
    TRY_AGAIN = "Sorry, I didn't get that. Please try asking in a different way"


class SalaryMessage(Enum):
    TOTAL_HEADLINE = "Overall {} Salary data:"
    SALARY_TEXT = "Your {} {} salary was={}"
    BONUS_TEXT = "Your last month bonus was={}"


def _get_salary_text(db_intent: DBIntent, pay_type: PayType,
                     salary: float) -> str:
    return SalaryMessage.SALARY_TEXT.value.format(db_intent, pay_type.value,
                                                  salary)


def create_bonus_message(bonus_value: float) -> str:
    return SalaryMessage.BONUS_TEXT.value.format(bonus_value)


from salary_data_handler import SalaryDataHandler


def get_both_pay_type_salary_massage(salary_db_handler: SalaryDataHandler,
                                     db_intent: DBIntent) -> str:
    string_net = get_pay_type_salary_massage(salary_db_handler, db_intent,
                                             PayType.NET.value)
    string_gross = get_pay_type_salary_massage(salary_db_handler, db_intent,
                                               PayType.GROSS.value)

    return_string = string_net + "\n" + string_gross
    return return_string


def get_pay_type_salary_massage(salary_db_handler: SalaryDataHandler,
                                db_intent: DBIntent,
                                pay_type: PayType) -> str:
    salary_value = salary_db_handler.find_salary_data(db_intent, pay_type)
    return_string = _get_salary_text(db_intent, pay_type, salary_value)
    return return_string


def _total_salary_headline_message(pay_type: PayType) -> str:
    return SalaryMessage.TOTAL_HEADLINE.value.format(pay_type.value)


def get_pay_type_total_salary_massage(salary_db_handler: SalaryDataHandler,
                                      pay_type: PayType) -> str:
    db_intents_list = [e.value for e in DBIntent]
    result_strings_list = []
    result_strings_list.append(
        _total_salary_headline_message(pay_type).strip())
    result_strings_list.append("\n")
    for db_intent in db_intents_list:
        if db_intent != DBIntent.TOTAL.value and db_intent != DBIntent.BONUS.value:
            salary_value = salary_db_handler.find_salary_data(db_intent,
                                                              pay_type)
            return_string = _get_salary_text(db_intent, pay_type, salary_value)
            result_strings_list.append(return_string.strip())
            result_strings_list.append("\n")
    result_strings_list.pop()
    return "".join(result_strings_list)


def get_both_pay_type_total_salary_massage(
        salary_db_handler: SalaryDataHandler) -> str:
    result_strings_list = []
    result_strings_list.append(get_pay_type_total_salary_massage(
        salary_db_handler, PayType.NET
    ))
    result_strings_list.append('\n')
    result_strings_list.append(get_pay_type_total_salary_massage(
        salary_db_handler, PayType.GROSS
    ))
    return "".join(result_strings_list)
