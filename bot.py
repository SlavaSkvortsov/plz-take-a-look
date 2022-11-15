import asyncio
from typing import Any

from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.context.ack.async_ack import AsyncAck
from slack_bolt.context.say.async_say import AsyncSay

from config import settings
from handlers.set_devs import SetDevsHandler
from handlers.take_a_look import TakeALookHandler
from types import UserID

app = AsyncApp(token=settings.slack_bot_token)


@app.command('/plz-tal')
async def plz_tal(ack: AsyncAck, say: AsyncSay, body: dict[str, Any]) -> None:
    handler = TakeALookHandler(
        user_id=UserID(body['user_id']),
        workspace_id=body['team_id'],
    )
    user_id = await handler.handle()
    await say(f'Hello, <{user_id}>! Please, take a look')
    await ack()


@app.command('/plz-set-devs')
async def plz_set_devs(ack: AsyncAck, say: AsyncSay, body: dict[str, Any]) -> None:
    await SetDevsHandler(
        user_id=UserID(body['user_id']),
        workspace_id=body['team_id'],
        dev_ids=body['text'].split(),
    ).handle()
    await say('Done!')
    await ack()


async def main() -> None:
    handler = AsyncSocketModeHandler(app, settings.slack_app_token)
    await handler.start_async()


if __name__ == '__main__':
    asyncio.run(main())
