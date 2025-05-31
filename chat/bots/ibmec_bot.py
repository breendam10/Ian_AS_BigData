# bots/ibmec_bot.py

from typing import List
from botbuilder.core import TurnContext, MessageFactory, ActivityHandler, CardFactory, ConversationState, UserState
from botbuilder.schema import HeroCard, CardAction, ActionTypes, CardImage
from botbuilder.dialogs import DialogSet
import requests
from cards.card_factory import (
    create_welcome_card,
    create_matricula_menu_card,
    create_calendar_card
)
from dialogs.new_registration_dialog import get_new_registration_dialog
from dialogs.consult_dialog import get_consult_dialog
from services.api_service import ApiService, API_BASE_URL

class IBMECBot(ActivityHandler):
    def __init__(self, conversation_state: ConversationState, user_state: UserState):
        self.conversation_state = conversation_state
        self.user_state = user_state

        self.dialog_state = conversation_state.create_property("DialogState")
        self.dialogs = DialogSet(self.dialog_state)

        self.dialogs.add(get_new_registration_dialog())
        self.dialogs.add(get_consult_dialog())

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

    async def on_members_added_activity(self, members_added: List, turn_context: TurnContext):
        for mem in members_added:
            if mem.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(MessageFactory.attachment(create_welcome_card()))

    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.strip()

        if text == "Matrícula":
            await turn_context.send_activity(MessageFactory.attachment(create_matricula_menu_card()))

        elif text == "Calendário":
            await turn_context.send_activity(MessageFactory.attachment(create_calendar_card()))

        elif text == "Boletos":
            await turn_context.send_activity(
                MessageFactory.attachment(CardFactory.hero_card(
                    HeroCard(
                        title="Emissão de Boletos",
                        text="Acesse o portal do aluno e na aba 'Financeiro' clique em 'Mensalidade'.",
                        buttons=[CardAction(type=ActionTypes.open_url, title="Portal do Aluno", value="https://sia.ibmec.br/sianet")],
                    )
                ))
            )

        elif text == "Horários":
            await turn_context.send_activity(
                MessageFactory.attachment(CardFactory.hero_card(
                    HeroCard(
                        title="Quadro de Horários",
                        images=[CardImage(url="https://marketplace.canva.com/EAD_vFS6BFY/1/0/1600w/canva-azul-simples-hor%C3%A1rio-de-aula-NzLOlx91dD0.jpg")],
                    )
                ))
            )

        elif text == "Secretaria":
            await turn_context.send_activity(
                MessageFactory.attachment(CardFactory.hero_card(
                    HeroCard(
                        title="Secretaria",
                        text="Horário de atendimento:\n\nSegunda a sexta-feira das 8h às 21h\n\nSábado das 8h às 12h",
                        images=[CardImage(url="https://i.ibb.co/Qv9PFjzZ/secretaria.jpg")],
                        buttons=[CardAction(type=ActionTypes.open_url, title="Atendimento via Whatsapp", value="https://wa.me/558008806771")],
                    )
                ))
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
            for aluno in data:
                card = HeroCard(
                    title=aluno["nome"],
                    text=f"Matrícula: {aluno['matricula']}\n\nCurso: {aluno['curso']}\n\nE-mail: {aluno['email']}",
                )
                cards.append(CardFactory.hero_card(card))

            await turn_context.send_activity(MessageFactory.carousel(cards))

        else:
            await turn_context.send_activity("❓ Desculpe, não entendi. Escolha uma opção pelo card.")
