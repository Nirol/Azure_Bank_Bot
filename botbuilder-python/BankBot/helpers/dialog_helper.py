from botbuilder.schema import InputHints

from botbuilder.core import MessageFactory
from salary_data_handler import SalaryDataHandler
from salary_details import SalaryDetails

from botbuilder.core import StatePropertyAccessor, TurnContext
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus


class DialogHelper:
    @staticmethod
    async def run_dialog(
        dialog: Dialog, turn_context: TurnContext, accessor: StatePropertyAccessor
    ):
        dialog_set = DialogSet(accessor)
        dialog_set.add(dialog)

        dialog_context = await dialog_set.create_context(turn_context)
        results = await dialog_context.continue_dialog()
        if results.status == DialogTurnStatus.Empty:
            await dialog_context.begin_dialog(dialog.id)

@staticmethod
def generate_message(msg_txt):
    message = MessageFactory.text(
        msg_txt, msg_txt, InputHints.ignoring_input
    )
    return message

@staticmethod
def get_bonus(salary_db_handler : SalaryDataHandler):
    # get client last salary bonus
    bonus_text = salary_db_handler.get_bonus_info()
    bonus_message = generate_message(bonus_text)
    return bonus_message

@staticmethod
def get_try_again_message():
    # get client last salary bonus
    didnt_understand_text = (
        "Sorry, I didn't get that. Please try asking in a different way"
    )
    try_again_message = generate_message(didnt_understand_text)
    return try_again_message


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


