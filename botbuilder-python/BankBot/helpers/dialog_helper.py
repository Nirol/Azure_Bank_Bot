from enum import Enum

from botbuilder.schema import InputHints

from botbuilder.core import MessageFactory
from salary_data_handler import SalaryDataHandler
from salary_details import SalaryDetails

from botbuilder.core import StatePropertyAccessor, TurnContext
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus


class PromptMessage(Enum):
    ENTRY_MSG = " Welcome to BankBot !, What can I help you with?"
    SALARY_TYPE_PROMPT_MSG = "Would you prefer viewing  :"
    PAY_TYPE_MSG = "Please specify if the salary is net, gross  or both:"
    WHAT_ELSE_MSG = "What else can I do for you?"


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


@staticmethod
def generate_message_ignore_input(msg_txt):
    message = MessageFactory.text(
        msg_txt, msg_txt, InputHints.ignoring_input
    )
    return message


@staticmethod
def generate_message_expect_input(msg_txt):
    message = MessageFactory.text(
        msg_txt, msg_txt, InputHints.expecting_input
    )
    return message





@staticmethod
def get_bonus(salary_db_handler: SalaryDataHandler):
    # get client last salary bonus
    bonus_text = salary_db_handler.get_bonus_info()
    bonus_message = generate_message_ignore_input(bonus_text)
    return bonus_message


async def show_warning_for_unsupported_actions(
        context: TurnContext, luis_result: SalaryDetails
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


def get_salary_info(salary_db_handler, salary_details):
    salary_text = salary_db_handler.get_salary_info(salary_details)
    final_message = generate_message_ignore_input(salary_text)
    return final_message


@staticmethod
def get_prompt_message(prompt_msg_enum: PromptMessage):
    message_text = prompt_msg_enum.value
    prompt_msg = generate_message_expect_input(message_text)
    return prompt_msg
