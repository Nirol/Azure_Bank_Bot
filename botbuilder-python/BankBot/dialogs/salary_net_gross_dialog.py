# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datatypes_date_time.timex import Timex

import dialog_helper
import salary_details
import specific_salary_details
import text_from_clients_helper
import text_to_clients_helper
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions

from cancel_and_help_dialog import CancelAndHelpDialog
from date_resolver_dialog import DateResolverDialog
from salary_data_handler import  SalaryDataHandler



class SalaryNetGrossDialog(CancelAndHelpDialog):
    def __init__(self, salary_db_handler : SalaryDataHandler,  dialog_id: str = None,):
        super(SalaryNetGrossDialog, self).__init__(dialog_id or SalaryNetGrossDialog.__name__)

        self.is_pay_type_user_input = False
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
        specific_salary_details = step_context.options
        if specific_salary_details.net is None and specific_salary_details.gross is None:
            self.is_pay_type_user_input = True
            prompt_message = dialog_helper.get_prompt_message(
                text_to_clients_helper.PromptMessage.PAY_TYPE_MSG)
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        else:
            salary_details.update_pay_type(specific_salary_details)

        return await step_context.next(specific_salary_details.pay_type)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Complete the interaction and end the dialog.
        :param step_context:
        :return DialogTurnResult:
        """
        salary_details = step_context.options
        #Capture the results of the previous step
        pay_type_user_input_text = step_context.result
        if salary_details and self.is_pay_type_user_input:
            salary_details.pay_type = text_from_clients_helper.fix_user_pay_type_input(pay_type_user_input_text)

        if salary_details:
            salary_msg = dialog_helper.get_salary_info(self.salary_db_handler, salary_details)
            await step_context.context.send_activity(salary_msg)
        return await step_context.end_dialog()
