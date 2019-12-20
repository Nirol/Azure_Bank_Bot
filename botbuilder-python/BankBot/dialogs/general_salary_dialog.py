# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datatypes_date_time.timex import Timex

import dialog_helper
import salary_details
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints
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
                dialog_helper.PromptMessage.SALARY_TYPE_PROMPT_MSG)
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )

        return await step_context.next(salary_details.pay_type)
