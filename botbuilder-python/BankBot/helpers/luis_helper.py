# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import Dict, List

import intent_helper
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext, \
    RecognizerResult
from general_salary_details import GeneralSalaryDetails
from intent_details import IndentDetailsABS
from intent_helper import Intent
from pay_type_enum import PayType
from specific_salary_details import SpecificSalaryDetails


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(
            luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> (Intent, object):
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None
        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)
            intent = get_intent(recognizer_result)

            if intent_helper.is_specific_salary(intent):
                result = SpecificSalaryDetails()
                result.intent = intent
                update_result_entity(recognizer_result, result,
                                     intent_helper.specific_salary_entities_list())



            elif intent == Intent.GENERAL_SALARY.value:
                result = GeneralSalaryDetails()
                update_result_entity(recognizer_result, result,
                                     intent_helper.general_salary_entities_list())

        except Exception as exception:
            print(exception)
        return intent, result


def get_intent(recognizer_result: RecognizerResult) -> str:
    intent = (
        sorted(
            recognizer_result.intents,
            key=recognizer_result.intents.get,
            reverse=True,
        )[:1][0]
        if recognizer_result.intents
        else None
    )
    return intent


def update_result_entity(recognizer_result: RecognizerResult,
                         result: IndentDetailsABS,
                         entities_list: List[PayType]) -> None:
    for entity in entities_list:
        entity_found = recognizer_result.entities.get("$instance", {}).get(
            entity.value, [])
        if len(entity_found) > 0:
            result.update_entity(entity.value,
                                 entity_found[0]["text"].capitalize())
