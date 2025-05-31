import os
from aiohttp import web

from botbuilder.core import (
    BotFrameworkAdapterSettings,
    BotFrameworkAdapter,
    MemoryStorage,
    ConversationState,
    UserState,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity

from bots.ibmec_bot import IBMECBot

APP_ID = os.getenv("MICROSOFT_APP_ID", "")
APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD", "")

settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)

memory = MemoryStorage()
conversation_state = ConversationState(memory)
user_state = UserState(memory)

bot = IBMECBot(conversation_state, user_state)

async def messages(req: web.Request) -> web.Response:
    if not req.headers.get("Content-Type", "").startswith("application/json"):
        return web.Response(status=415)

    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    response = await adapter.process_activity(activity, auth_header, bot.on_turn)
    if response:
        return web.json_response(data=response.body, status=response.status)
    return web.Response(status=200)

app = web.Application(middlewares=[aiohttp_error_middleware])
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(app, host="localhost", port=3978)
