from difflib import SequenceMatcher
from enum import Enum
from typing import List

import numpy as np

from db_intent_enum import DBIntent
from intent.enums.pay_type_enum import PayType
from intent_enum import Intent


def _get_pay_type_enum_list() -> List[PayType]:
    return [e.value for e in PayType]


def _get_DBIntent_enum_list() -> List[DBIntent]:
    return [e.value for e in DBIntent]


def _find_user_input_score_against_all(
        user_input: str, enum: Enum) -> List[float]:
    enum_list = []
    if enum is PayType:
        enum_list = _get_pay_type_enum_list()
    elif enum is DBIntent:
        enum_list = _get_DBIntent_enum_list()

    enum_match_result_list = [
        calculate_user_input_word_distance(pay_type_enum, user_input)
        for pay_type_enum in enum_list]
    return enum_match_result_list


def _find_best_fitting_enum(score_list: List[float], enum: Enum) -> Enum:
    most_fitting_enum_index = np.argmax(score_list)
    best_fitting_score = score_list[most_fitting_enum_index]
    if best_fitting_score > 0.4:
        if enum is PayType:
            enum_list = _get_pay_type_enum_list()
            return PayType(
                enum_list[most_fitting_enum_index])
        elif enum is DBIntent:
            enum_list = _get_DBIntent_enum_list()
            return DBIntent(
                enum_list[most_fitting_enum_index])


def fix_user_pay_type_input(user_input_pay_type: str) -> PayType:
    if user_input_pay_type is PayType:
        user_input_pay_type = user_input_pay_type.value.lower()
    else:
        user_input_pay_type = user_input_pay_type.lower()
    # calculate distance of the user input for pay type from each of the pay type options in PayType enum
    score_list = _find_user_input_score_against_all(
        user_input_pay_type, PayType)
    # find best fitting pay type enum or -1 if none with score above 0.5
    return _find_best_fitting_enum(score_list, PayType)


def calculate_user_input_word_distance(pay_type_enum: PayType,
                                       user_input_pay_type: str) -> float:
    s = SequenceMatcher(None, user_input_pay_type, pay_type_enum)
    return s.ratio()


def fix_user_salary_type_input(salary_type_user_input_text: str) -> DBIntent:
    user_input_salary_type = salary_type_user_input_text.upper()
    # calculate distance of the user input for pay type from each of the pay type options in PayType enum
    score_list = _find_user_input_score_against_all(user_input_salary_type,
                                                    DBIntent)
    # find best fitting pay type enum or -1 if none with score above 0.5
    return _find_best_fitting_enum(score_list, DBIntent)
