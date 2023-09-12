from async_websocket_client.dispatchers import BaseDispatcher
from main import OpenAPI
import settings
from typing import Any


class WSClientPushOver(BaseDispatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        api = OpenAPI(settings.EMAIL_USERNAME, settings.PASSWORD,
                      device_id=settings.DEVICE_ID)
        await api.a_launch_preparation()
        self.api: OpenAPI = api

    async def on_connect(self) -> Any:
        await self.api.a_login()
        return await self.ws.send(
            f'login:{self.api.device_id}:{self.api.secret}')

    async def receiver_messages(self, message: dict):
        pass

    async def on_message(self, message: bytes):
        message: str = message.decode(encoding='utf-8')
        if message == '!':
            messages = await self.api.a_get_messages()
            await self.receiver_messages(messages)
