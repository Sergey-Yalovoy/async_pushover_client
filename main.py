import requests
import settings
from exceptions import AuthenticationError, MessagesError
from typing import Union
import aiohttp


class OpenAPI:
    def __init__(self, email: str, password: str,
                 device_id=None):
        self.email: str = email
        self.password: str = password
        self.secret: Union[str, None] = None
        self.device_id: Union[str, None] = device_id

    def login(self):
        response = requests.post(settings.LOGIN_URL, data=self.__dict__)
        if response.status_code == 200:
            auth_data = response.json()
            self.secret = auth_data.get('secret')
        else:
            raise AuthenticationError()

    async def a_login(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(settings.LOGIN_URL, data=self.__dict__) as response:
                if response.status == 200:
                    auth_data: dict = await response.json()
                    self.secret = auth_data.get('secret')
                else:
                    raise AuthenticationError()

    def device_registration(self, name, os='O'):
        response = requests.post(settings.DEVICE_REGISTRATION_URL,
                                 data=dict(secret=self.secret,
                                           name=name,
                                           os=os))
        if response.status_code == 200:
            data = response.json()
            self.device_id = data.get('id')
        else:
            raise AuthenticationError(message=response.text)

    async def a_device_registration(self, name, os='O'):
        async with aiohttp.ClientSession() as session:
            async with session.post(settings.DEVICE_REGISTRATION_URL,
                                    data=dict(secret=self.secret,
                                              name=name,
                                              os=os)) as response:
                if response.status == 200:
                    data: dict = await response.json()
                    self.device_id = data.get('id')
                else:
                    raise AuthenticationError(message=await response.text())

    def get_messages(self):
        response = requests.get(settings.MESSAGE_URL,
                                params=dict(secret=self.secret,
                                            device_id=self.device_id))
        if response.status_code == 200:
            data = response.json()
            return data.get('messages')
        else:
            raise MessagesError(message=response.text)

    async def a_get_messages(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(settings.MESSAGE_URL,
                                   params=dict(secret=self.secret,
                                               device_id=self.device_id)) as response:
                if response.status == 200:
                    data: dict = await response.json()
                    return data.get('messages')
                else:
                    raise MessagesError(message=await response.text())

    def clear_messages(self, message_id):
        url = f"https://api.pushover.net/1/devices/{self.device_id}/update_highest_message.json"
        response = requests.post(url, data=dict(secret=self.secret,
                                                message=message_id))
        if response.status_code == 200:
            return response.json()
        else:
            raise MessagesError(message=response.text)

    async def a_clear_messages(self, message_id):
        url = settings.CLEAR_MESSAGE_URL.format(device_id=self.device_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(url,
                                   params=dict(secret=self.secret,
                                               message_id=message_id)) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise MessagesError(message=await response.text())
