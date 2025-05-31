# cards/card_factory.py
from botbuilder.schema import HeroCard, CardAction, ActionTypes, CardImage
from botbuilder.core import CardFactory

def create_welcome_card() -> dict:
    card = HeroCard(
        title="Bem-vindo ao chatbot da IBMEC!",
        text="Escolha uma opção:",
        buttons=[
            CardAction(type=ActionTypes.im_back, title="Matrícula", value="Matrícula"),
            CardAction(type=ActionTypes.im_back, title="Calendário", value="Calendário"),
            CardAction(type=ActionTypes.im_back, title="Boletos", value="Boletos"),
            CardAction(type=ActionTypes.im_back, title="Horários", value="Horários"),
            CardAction(type=ActionTypes.im_back, title="Secretaria", value="Secretaria"),
        ],
    )
    return CardFactory.hero_card(card)

def create_matricula_menu_card() -> dict:
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

def create_calendar_card() -> dict:
    card = HeroCard(
        title="Calendário Acadêmico 2025.1",
        images=[CardImage(url="https://i.ibb.co/2YKXF4hT/Calendario-Academico-2025-1-V3-Ibmec5-RJ-1.png")],
    )
    return CardFactory.hero_card(card)
