# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import dialog_helper
import intent_helper
import salary_details
import text_from_clients_helper
import text_to_clients_helper
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from cancel_and_help_dialog import CancelAndHelpDialog
from date_resolver_dialog import DateResolverDialog
from salary_data_handler import  SalaryDataHandler


class GeneralSalaryDialog(CancelAndHelpDialog):
    def __init__(self, salary_db_handler : SalaryDataHandler,  dialog_id: str = None,):
        super(GeneralSalaryDialog, self).__init__(dialog_id or GeneralSalaryDialog.__name__)

        self.salary_db_handler = salary_db_handler
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(DateResolverDialog(DateResolverDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.salary_type_step,
                    self.net_gross_step,
                    self.final_step,
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__


    async def salary_type_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        If a net or gross salary type has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        general_salary_details = step_context.options
        if general_salary_details.salary_type is None:
            prompt_message = dialog_helper.get_prompt_message(
                text_to_clients_helper.PromptMessage.SALARY_TYPE_PROMPT_MSG)
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )

        return await step_context.next(general_salary_details.salary_type)


    async def net_gross_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        If a net or gross salary type has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        general_salary_details = step_context.options
        salary_type_user_input_text = step_context.result
        if general_salary_details:
            general_salary_details.salary_type = text_from_clients_helper.fix_user_salary_type_input(
                salary_type_user_input_text)


        if general_salary_details.net is None and general_salary_details.gross is None:
            prompt_message = dialog_helper.get_prompt_message(
                text_to_clients_helper.PromptMessage.PAY_TYPE_MSG)
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )

        else:
            salary_details.update_pay_type(salary_details)
        return await step_context.next(general_salary_details.pay_type)


    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Complete the interaction and end the dialog.
        :param step_context:
        :return DialogTurnResult:
        """
        general_salary_details = step_context.options
        #Capture the results of the previous step
        pay_type_user_input_text = step_context.result
        if general_salary_details and pay_type_user_input_text:
            general_salary_details.pay_type = text_from_clients_helper.fix_user_pay_type_input(pay_type_user_input_text)

        if general_salary_details:
            if  intent_helper.is_specific_general_salary(general_salary_details.salary_type):
                salary_msg = dialog_helper.get_salary_info(self.salary_db_handler, general_salary_details)
            elif intent_helper.is_total_salary(general_salary_details.salary_type):
                salary_msg = dialog_helper.get_total_salary_info(
                    self.salary_db_handler, general_salary_details)

            await step_context.context.send_activity(salary_msg)
            return await step_context.end_dialog(general_salary_details)
        return await step_context.end_dialog()
