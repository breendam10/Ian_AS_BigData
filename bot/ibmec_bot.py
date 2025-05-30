import os
import requests
from typing import List
from botbuilder.core import TurnContext, MessageFactory, ActivityHandler, MemoryStorage, ConversationState, UserState, CardFactory
from botbuilder.schema import CardAction, ActionTypes, HeroCard, CardImage, Attachment
from botbuilder.dialogs import DialogSet, WaterfallDialog, WaterfallStepContext, PromptOptions, TextPrompt

API_BASE_URL = "https://ian-as-bigdata-gca5hxdng8e8fdhu.centralus-01.azurewebsites.net/api"

class IBMECBot(ActivityHandler):
    def __init__(self, conversation_state: ConversationState, user_state: UserState):
        self.conversation_state = conversation_state
        self.user_state = user_state

        self.dialog_state = conversation_state.create_property("DialogState")
        self.dialogs = DialogSet(self.dialog_state)

        self.dialogs.add(TextPrompt("namePrompt"))
        self.dialogs.add(TextPrompt("emailPrompt"))
        self.dialogs.add(TextPrompt("coursePrompt"))
        self.dialogs.add(TextPrompt("matriculaPrompt"))

        self.dialogs.add(
            WaterfallDialog(
                "newRegistration",
                [
                    self.prompt_name_step,
                    self.prompt_email_step,
                    self.prompt_course_step,
                    self.final_step_registration,
                ],
            )
        )

        self.dialogs.add(
            WaterfallDialog(
                "consultDialog",
                [
                    self.prompt_matricula_step,
                    self.final_step_consult,
                ],
            )
        )

    async def on_turn(self, turn_context: TurnContext):
        dc = await self.dialogs.create_context(turn_context)

        if turn_context.activity.type == "message":
            result = await dc.continue_dialog()
            if not dc.context.responded:
                await self.on_message_activity(turn_context)
        else:
            await super().on_turn(turn_context)

        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_members_added_activity(
        self, members_added: List, turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.attachment(self._welcome_card())
                )

    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.strip()

        if text == "Matrícula":
            await turn_context.send_activity(
                MessageFactory.attachment(self._matricula_card())
            )

        elif text == "Calendário":
            await turn_context.send_activity(
                MessageFactory.attachment(self._calendar_card())
            )

        elif text == "Boletos":
            await turn_context.send_activity(
                MessageFactory.attachment(self._boletos_card())
            )

        elif text == "Horários":
            await turn_context.send_activity(
                MessageFactory.attachment(self._horarios_card())
            )

        elif text == "Secretaria":
            await turn_context.send_activity(
                MessageFactory.attachment(self._secretaria_card())
            )

        elif text == "Novo Cadastro":
            dc = await self.dialogs.create_context(turn_context)
            await dc.begin_dialog("newRegistration")

        elif text == "Consultar Cadastro":
            dc = await self.dialogs.create_context(turn_context)
            await dc.begin_dialog("consultDialog")

        elif text == "Listar Cadastros":
            resp = requests.get(f"{API_BASE_URL}/matriculas")
            data = resp.json()

            cards = []
            for item in data:
                card = HeroCard(
                    title=item["nome"],
                    text=f"Matrícula: {item['matricula']}\n\nCurso: {item['curso']}",
                )
                cards.append(CardFactory.hero_card(card))

            await turn_context.send_activity(MessageFactory.carousel(cards))

        else:
            await turn_context.send_activity(
                "Desculpe, não entendi. Por favor, escolha uma das opções pelo card."
            )

    def _welcome_card(self) -> Attachment:
        card = HeroCard(
            title="Bem-vindo ao chatbot da IBMEC!",
            text="Escolha uma das opções abaixo:",
            buttons=[
                CardAction(type=ActionTypes.im_back, title="Matrícula", value="Matrícula"),
                CardAction(type=ActionTypes.im_back, title="Calendário", value="Calendário"),
                CardAction(type=ActionTypes.im_back, title="Boletos", value="Boletos"),
                CardAction(type=ActionTypes.im_back, title="Horários", value="Horários"),
                CardAction(type=ActionTypes.im_back, title="Secretaria", value="Secretaria"),
            ],
        )
        return CardFactory.hero_card(card)

    def _matricula_card(self) -> Attachment:
        card = HeroCard(
            title="Matrícula",
            text="O que você deseja fazer?",
            buttons=[
                CardAction(type=ActionTypes.im_back, title="Novo Cadastro", value="Novo Cadastro"),
                CardAction(type=ActionTypes.im_back, title="Consultar Cadastro", value="Consultar Cadastro"),
                CardAction(type=ActionTypes.im_back, title="Listar Cadastros", value="Listar Cadastros"),
            ],
        )
        return CardFactory.hero_card(card)

    def _calendar_card(self) -> Attachment:
        card = HeroCard(
            title="Calendário Acadêmico 2025.1",
            images=[CardImage(url="https://marketplace.canva.com/EAD_vFS6BFY/1/0/1600w/canva-azul-simples-hor%C3%A1rio-de-aula-NzLOlx91dD0.jpg")],
        )
        return CardFactory.hero_card(card)

    def _boletos_card(self) -> Attachment:
        card = HeroCard(
            title="Emissão de Boletos",
            text="Acesse o portal do aluno e na aba 'Financeiro' clique em 'Mensalidade'.",
            buttons=[
                CardAction(type=ActionTypes.open_url, title="Portal do Aluno", value="https://sia.ibmec.br/sianet")
            ],
        )
        return CardFactory.hero_card(card)

    def _horarios_card(self) -> Attachment:
        card = HeroCard(
            title="Quadro de Horários",
            images=[CardImage(url="https://marketplace.canva.com/EAD_vFS6BFY/1/0/1600w/canva-azul-simples-hor%C3%A1rio-de-aula-NzLOlx91dD0.jpg")],
        )
        return CardFactory.hero_card(card)

    def _secretaria_card(self) -> Attachment:
        card = HeroCard(
            title="Secretaria",
            images=[CardImage(url="https://marketplace.canva.com/EAD_vFS6BFY/1/0/1600w/canva-azul-simples-hor%C3%A1rio-de-aula-NzLOlx91dD0.jpg")],
            buttons=[
                CardAction(type=ActionTypes.open_url, title="Contato", value="mailto:secretaria@ibmec.br")
            ],
        )
        return CardFactory.hero_card(card)

    async def prompt_name_step(self, step: WaterfallStepContext):
        return await step.prompt(
            "namePrompt",
            PromptOptions(prompt=MessageFactory.text("Qual seu nome?")),
        )

    async def prompt_email_step(self, step: WaterfallStepContext):
        step.values["name"] = step.result
        return await step.prompt(
            "emailPrompt",
            PromptOptions(prompt=MessageFactory.text("Qual seu e-mail?")),
        )

    async def prompt_course_step(self, step: WaterfallStepContext):
        step.values["email"] = step.result
        return await step.prompt(
            "coursePrompt",
            PromptOptions(prompt=MessageFactory.text("Qual seu curso?")),
        )

    async def final_step_registration(self, step: WaterfallStepContext):
        # 1) Recupere nome e e-mail dos valores salvos
        name = step.values.get("name")
        email = step.values.get("email")
        # 2) O resultado deste passo é o curso
        curso = step.result

        # 3) Monte o payload e logue no console
        payload = {"nome": name, "email": email, "curso": curso}
        print("🔄 Novo Cadastro payload:", payload)

        # 4) Execute o POST
        url = f"{API_BASE_URL}/matriculas"
        resp = requests.post(url, json=payload)

        # 5) Log de status e corpo
        print("🖥️ Status POST:", resp.status_code, "–", resp.text)

        # 6) Envie feedback ao usuário
        if resp.status_code in (200, 201):
            retorno = resp.json()
            # Se veio lista, pega o último item
            if isinstance(retorno, list):
                criado = retorno[-1]
            else:
                criado = retorno

            await step.context.send_activity(
                MessageFactory.text(
                    "✅ Cadastro criado!\n"
                    f"• Nome: {criado['nome']}\n"
                    f"• Matrícula: {criado['matricula']}\n"
                    f"• Curso: {criado['curso']}\n"
                    f"• E-mail: {criado['email']}"
                )
            )
        else:
            await step.context.send_activity(
                MessageFactory.text(f"❌ Erro ao cadastrar ({resp.status_code}): {resp.text}")
            )

        # 7) Encerre o diálogo
        return await step.end_dialog()


    async def prompt_matricula_step(self, step: WaterfallStepContext):
        return await step.prompt(
            "matriculaPrompt",
            PromptOptions(prompt=MessageFactory.text("Qual matrícula deseja consultar?")),
        )

    async def final_step_consult(self, step: WaterfallStepContext):
        matricula_id = step.result
        resp = requests.get(f"{API_BASE_URL}/matriculas/{matricula_id}")
        data = resp.json()

        if data.get("error"):
            await step.context.send_activity(f"❌ {data['error']}")
        else:
            card = HeroCard(
                title=f"Cadastro: {data['matricula']}",
                text=f"• Nome: {data['nome']}\n• E-mail: {data['email']}\n• Curso: {data['curso']}",
            )
            await step.context.send_activity(
                MessageFactory.attachment(CardFactory.hero_card(card))
            )

        return await step.end_dialog()
