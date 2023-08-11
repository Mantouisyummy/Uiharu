import asyncio
from typing import TYPE_CHECKING

# noinspection PyProtectedMember
from disnake.abc import MISSING

from core.utils import get_initial_prompt
from Poe import Chat

if TYPE_CHECKING:
    from core.bot import Uiharu


class Conversation:
    def __init__(self,
                 bot: "Uiharu",
                 author_id: int,
                 nickname: str = MISSING):
        self.bot: "Uiharu" = bot

        self.author_id: int = author_id
        self.nickname: str = nickname

        self.chat: Chat = Chat(bot.poe)

        self.ready: bool = False

    async def ask(self, text: str) -> str:
        while not self.ready:
            await asyncio.sleep(1)

        return await self.chat.talk(text)

    async def setup(self):
        """
        Initialize the conversation, including sending the first message to the bot
        """
        self.ready = True

    async def close(self):
        await self.chat.remove()


class ConversationManager:
    def __init__(self, bot: "Uiharu"):
        self.bot = bot

        self.conversations: dict[int, Conversation] = {}

    async def close_conversation(self, user_id: int):
        if user_id not in self.conversations:
            return

        await self.conversations[user_id].close()

        del self.conversations[user_id]

    async def get_conversation(self, user_id: int) \
            -> Conversation:
        
        if user_id in self.conversations:
            return self.conversations[user_id]

        self.conversations[user_id] = Conversation(
            self.bot, user_id, self.bot.nickname_manager.get_nickname(user_id=user_id)
        )

        await self.conversations[user_id].setup()
        print("??")

        return self.conversations[user_id]
