from typing import List

from intent.enums.db_intent_enum import DBIntent
from intent.enums.intent_enum import Intent


def convert_luis_intent_to_db_intent(intent: Intent) -> DBIntent:
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


def is_specific_salary(intent: Intent) -> bool:
    if intent == Intent.LAST_SALARY.value or intent == Intent.AVG_SALARY.value or \
            intent == Intent.YTD_SALARY.value:
        return True
    return False


from intent.enums.pay_type_enum import PayType

#TODO: merge methods
def specific_salary_entities_list() -> List[PayType]:
    entities_list = [PayType.NET, PayType.GROSS]
    return entities_list


def general_salary_entities_list()-> List[PayType]:
    entities_list = [PayType.NET, PayType.GROSS]
    return entities_list


def is_total_salary(salary_type : DBIntent) -> bool:
    if salary_type.value == DBIntent.TOTAL.value or salary_type == DBIntent.TOTAL:
        return True
    return False

#TODO : solve enums ambguity usage
def is_specific_general_salary(db_intent: DBIntent) -> bool:
    if db_intent == DBIntent.LAST.value or db_intent == DBIntent.AVG.value or \
            db_intent == DBIntent.YTD.value:
        return True
    elif db_intent == DBIntent.LAST or db_intent == DBIntent.AVG or \
                db_intent == DBIntent.YTD:
        return True
    return False