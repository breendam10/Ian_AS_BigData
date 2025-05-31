# dialogs/new_registration_dialog.py

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    TextPrompt,
    PromptOptions,
)
from botbuilder.core import MessageFactory
from services.api_service import ApiService


class NewRegistrationDialog(ComponentDialog):
    def __init__(self, dialog_id: str = "newRegistration"):
        super(NewRegistrationDialog, self).__init__(dialog_id)

        self.add_dialog(TextPrompt("namePrompt"))
        self.add_dialog(TextPrompt("emailPrompt"))
        self.add_dialog(TextPrompt("coursePrompt"))
        self.add_dialog(
            WaterfallDialog(
                "newRegistrationWaterfall",
                [
                    self.prompt_name_step,
                    self.prompt_email_step,
                    self.prompt_course_step,
                    self.final_step_registration,
                ],
            )
        )

        self.initial_dialog_id = "newRegistrationWaterfall"

    async def prompt_name_step(self, step: WaterfallStepContext) -> DialogTurnResult:
        return await step.prompt(
            "namePrompt",
            PromptOptions(prompt=MessageFactory.text("Qual seu nome?")),
        )

    async def prompt_email_step(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["name"] = step.result
        return await step.prompt(
            "emailPrompt",
            PromptOptions(prompt=MessageFactory.text("Qual seu e-mail?")),
        )

    async def prompt_course_step(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["email"] = step.result
        return await step.prompt(
            "coursePrompt",
            PromptOptions(prompt=MessageFactory.text("Qual seu curso?")),
        )

    async def final_step_registration(self, step: WaterfallStepContext) -> DialogTurnResult:
        name = step.values["name"]
        email = step.values["email"]
        curso = step.result
        criado = await ApiService.create_student(name, email, curso)

        if criado:
            await step.context.send_activity(
                MessageFactory.text(
                    "✅ Cadastro criado com sucesso!\n\n"
                    f"• Nome: {criado['nome']}\n\n"
                    f"• Matrícula: {criado['matricula']}\n\n"
                    f"• Curso: {criado['curso']}\n\n"
                    f"• E-mail: {criado['email']}"
                )
            )
        else:
            await step.context.send_activity(
                MessageFactory.text("❌ Erro ao cadastrar. Tente novamente mais tarde.")
            )

        return await step.end_dialog()


def get_new_registration_dialog() -> NewRegistrationDialog:
    return NewRegistrationDialog()
