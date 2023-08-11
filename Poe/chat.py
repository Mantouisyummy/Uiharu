from disnake.utils import MISSING

from .poe import PoeClient

import json

class Chat:
    def __init__(self, poeclient: PoeClient):
        self.poe: PoeClient = poeclient

        self.chat_id = MISSING

    async def talk(self, prompt: str):
        if not self.chat_id:
            result = await self.poe.chat(
                botname="uiharu",
                text=prompt
            )
            
            return result
        
        result = await self.poe.chat(
            botname="uiharu",
            text=prompt
        )

        return result

    async def remove(self):
        await self.poe.remove_chat(botname="uiharu")
