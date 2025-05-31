# dialogs/consult_dialog.py

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    TextPrompt,
    PromptOptions,
)
from botbuilder.core import MessageFactory, CardFactory
from botbuilder.schema import HeroCard
from services.api_service import ApiService


class ConsultDialog(ComponentDialog):
    def __init__(self, dialog_id: str = "consultDialog"):
        super(ConsultDialog, self).__init__(dialog_id)
        self.add_dialog(TextPrompt("matriculaPrompt"))
        self.add_dialog(
            WaterfallDialog(
                "consultWaterfall",
                [self.prompt_matricula_step, self.final_step_consult],
            )
        )

        self.initial_dialog_id = "consultWaterfall"

    async def prompt_matricula_step(self, step: WaterfallStepContext) -> DialogTurnResult:
        return await step.prompt(
            "matriculaPrompt",
            PromptOptions(prompt=MessageFactory.text("Qual matrícula deseja consultar?")),
        )

    async def final_step_consult(self, step: WaterfallStepContext) -> DialogTurnResult:
        matricula = step.result
        aluno = await ApiService.get_student_by_matricula(matricula)
        if aluno:
            card = HeroCard(
                title=aluno["nome"],
                text=(
                    f"Matrícula: {aluno['matricula']}\n\n"
                    f"Curso: {aluno['curso']}\n\n"
                    f"E-mail: {aluno['email']}"
                ),
            )
            await step.context.send_activity(MessageFactory.attachment(CardFactory.hero_card(card)))
        else:
            await step.context.send_activity(MessageFactory.text("❌ Matrícula não encontrada."))

        return await step.end_dialog()


def get_consult_dialog() -> ConsultDialog:
    return ConsultDialog()
