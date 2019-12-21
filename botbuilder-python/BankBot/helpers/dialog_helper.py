
from botbuilder.schema import InputHints
from botbuilder.core import MessageFactory
from botbuilder.core import StatePropertyAccessor, TurnContext
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus
from general_salary_details import GeneralSalaryDetails

from salary_data_handler import SalaryDataHandler
from specific_salary_details import SpecificSalaryDetails

from text_to_clients_helper import PromptMessage
import text_to_clients_helper
from intent_helper import convert_luis_intent_to_db_intent


class DialogHelper:
    @staticmethod
    async def run_dialog(
            dialog: Dialog, turn_context: TurnContext,
            accessor: StatePropertyAccessor
    ):
        dialog_set = DialogSet(accessor)
        dialog_set.add(dialog)

        dialog_context = await dialog_set.create_context(turn_context)
        results = await dialog_context.continue_dialog()
        if results.status == DialogTurnStatus.Empty:
            await dialog_context.begin_dialog(dialog.id)



def generate_message_ignore_input(msg_txt: str) -> str:
    message = MessageFactory.text(
        msg_txt, msg_txt, InputHints.ignoring_input
    )
    return message



def generate_message_expect_input(msg_txt : str) -> str:
    message = MessageFactory.text(
        msg_txt, msg_txt, InputHints.expecting_input
    )
    return message



def get_bonus(salary_db_handler: SalaryDataHandler) -> str:
    # get client last salary bonus
    bonus_value = salary_db_handler.get_bonus_info()
    # wrap it in text message
    bonus_message_text = text_to_clients_helper.create_bonus_message(
        bonus_value)
    bonus_message = generate_message_ignore_input(bonus_message_text)
    return bonus_message


async def show_warning_for_unsupported_actions(
        context: TurnContext, luis_result: SpecificSalaryDetails
) -> None:
    if luis_result.unsupported_actions:
        message_text = (
            f"Sorry but the following actions are not supported:"
            f" {', '.join(luis_result.unsupported_actions)}"
        )
        message = MessageFactory.text(
            message_text, message_text, InputHints.ignoring_input
        )
        await context.send_activity(message)



def get_salary_info(salary_db_handler : SalaryDataHandler, salary_details: SpecificSalaryDetails) -> str:
    intent = salary_details.intent
    db_intent = convert_luis_intent_to_db_intent(intent)
    pay_type = salary_details.pay_type

    from intent.enums.pay_type_enum import PayType
    if pay_type == PayType.BOTH.value:
        return_string = text_to_clients_helper.get_both_pay_type_salary_massage(
            salary_db_handler, db_intent)
    else:
        return_string =text_to_clients_helper.get_pay_type_salary_massage(
            salary_db_handler, db_intent, pay_type)

    final_message = generate_message_ignore_input(return_string)
    return final_message



def get_prompt_message(prompt_msg_enum: PromptMessage) -> str:
    message_text = prompt_msg_enum.value
    prompt_msg = generate_message_expect_input(message_text)
    return prompt_msg


def get_total_salary_info(salary_db_handler  : SalaryDataHandler, general_salary_details : GeneralSalaryDetails) -> str:
    pay_type = general_salary_details.pay_type
    from intent.enums.pay_type_enum import PayType
    if pay_type == PayType.BOTH:
        return_string = text_to_clients_helper.get_both_pay_type_total_salary_massage(
            salary_db_handler)
    else:
        return_string = text_to_clients_helper.get_pay_type_total_salary_massage(
            salary_db_handler, pay_type)
    return return_string