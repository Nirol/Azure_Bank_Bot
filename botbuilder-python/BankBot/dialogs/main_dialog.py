# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import dialog_helper
import intent_helper
from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints
from general_salary_dialog import GeneralSalaryDialog
from salary_data_handler import SalaryDataHandler

from salary_details import SalaryDetails
from bank_recognizer import BankRecognizer
from helpers.luis_helper import LuisHelper, Intent
from salary_net_gross_dialog import SalaryNetGrossDialog



class MainDialog(ComponentDialog):
    def __init__(
        self, luis_recognizer: BankRecognizer, salary_net_gross_dialog: SalaryNetGrossDialog,
            general_salary_dialog_id : GeneralSalaryDialog, salary_db_handler : SalaryDataHandler
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self.salary_db_handler = salary_db_handler
        self._luis_recognizer = luis_recognizer
        self._salary_net_gross_dialog_id = salary_net_gross_dialog.id
        self._general_salary_dialog_id = general_salary_dialog_id

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(salary_net_gross_dialog)
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.intro_step, self.act_step, self.final_step]
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input,
                )
            )
            return await step_context.next(None)
        prompt_entry_message = dialog_helper.get_prompt_message(
            dialog_helper.PromptMessage.ENTRY_MSG)
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_entry_message)
        )


    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            # LUIS is not configured, we just run the full salary dialog path with an empty FullSalarDetail.
            return await step_context.begin_dialog(
                self._salary_net_gross_dialog_id, SalaryDetails()
            )

        # Call LUIS and gather any potential bank operation  details.
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )

        if intent_helper.is_specific_salary(intent) and luis_result:
            # Show a warning for
            await dialog_helper.show_warning_for_unsupported_actions(
                step_context.context, luis_result
            )
            # Run the salary net gross dialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._salary_net_gross_dialog_id, luis_result)

        if intent == Intent.GENERAL_SALARY.value:
            # Run general salary dialog, complete data required from the user
            return await step_context.begin_dialog(
                self._general_salary_dialog_id, luis_result)

        if intent == Intent.BONUS.value:
            bonus_message = dialog_helper.get_bonus(self.salary_db_handler)
            await step_context.context.send_activity(bonus_message)
        else:
            didnt_understand_message = dialog_helper.get_try_again_message()
            await step_context.context.send_activity(didnt_understand_message)
        return await step_context.next(None)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        prompt_message = dialog_helper.get_prompt_message(
            dialog_helper.PromptMessage.WHAT_ELSE_MSG)
        return await step_context.replace_dialog(self.id, prompt_message)