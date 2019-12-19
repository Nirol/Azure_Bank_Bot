from enum import Enum


class Intent(Enum):
    AVG_SALARY = "Bank_PayCheck_CheckAvgSalary"
    YTD_SALARY = "Bank_PayCheck_CheckSalaryYTD"
    LAST_SALARY = "Bank_PayCheck_CheckLastSalary"
    BONUS = "Bank_PayCheck_CheckLastBonus"
    GENERAL_SALARY = "Bank_PayCheck_Salary"
    NONE_INTENT = "NoneIntent"


class DBIntent(Enum):
    AVG = "AVG"
    YTD = "YTD"
    LAST = "LAST"
    BONUS = "BONUS"


def convert_luis_intent_to_db_intent(intent: Intent):
    db_intent_result = None
    if intent == Intent.LAST_SALARY.value:
        db_intent_result = DBIntent.LAST.value
    elif intent == Intent.YTD_SALARY.value:
        db_intent_result = DBIntent.YTD.value
    elif intent == Intent.AVG_SALARY.value:
        db_intent_result = DBIntent.AVG.value
    else:
        pass
        "TODO: implement error"
    return db_intent_result


def is_specific_salary(intent: Intent):
    if intent == Intent.LAST_SALARY.value or intent == Intent.AVG_SALARY.value or \
            intent == Intent.YTD_SALARY.value:
        return True
    return False


def specific_salary_entities_list():
    entities_list = ["net", "gross"]
    return entities_list
