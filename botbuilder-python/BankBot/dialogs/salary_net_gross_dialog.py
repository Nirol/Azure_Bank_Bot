# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints
from cancel_and_help_dialog import CancelAndHelpDialog
from date_resolver_dialog import DateResolverDialog
from salary_data_handler import  SalaryDataHandler


class SalaryNetGrossDialog(CancelAndHelpDialog):
    def __init__(self, salary_db_handler : SalaryDataHandler,  dialog_id: str = None,):
        super(SalaryNetGrossDialog, self).__init__(dialog_id or SalaryNetGrossDialog.__name__)

        self.salary_db_handler = salary_db_handler
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(DateResolverDialog(DateResolverDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.net_gross_step,
                    self.final_step,
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def net_gross_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        If a net or gross salary type has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        salary_details = step_context.options
        if salary_details.net is None and salary_details.gross is None:
            message_text = "Please specify if the salary is net, gross  or both:"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )

            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )

        return await step_context.next(salary_details.pay_type)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Complete the interaction and end the dialog.
        :param step_context:
        :return DialogTurnResult:
        """
        salary_details = step_context.options
        #Capture the results of the previous step
        salary_details.pay_type = step_context.result

        if salary_details:
            get_bonus_text = self.salary_db_handler.get_salary_info(salary_details)
            get_bonus_message = MessageFactory.text(
                get_bonus_text, get_bonus_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(get_bonus_message)
            return await step_context.end_dialog(salary_details)
        return await step_context.end_dialog()

    def is_ambiguous(self, timex: str) -> bool:
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
