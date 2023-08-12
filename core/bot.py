import logging
from os import getenv

from disnake.ext.commands import Bot as OriginalBot
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.server_api import ServerApi

from core.conversations import ConversationManager
from core.nicknames import NicknameManager
from Poe import PoeClient


class Uiharu(OriginalBot):
    def __init__(self, *args, **kwargs):
        """
        :param args: args to pass to the bot
        :param kwargs: kwargs to pass to the bot
        """
        super().__init__(*args, **kwargs)

        self.db: Database = MongoClient(
            getenv("MONGO_URI"),
            server_api=ServerApi('1')
        )["main"]

        self.poe = PoeClient(
            getenv("PB_TOKEN"), getenv("FORMKEY")
        )

        self.nickname_manager = NicknameManager(self)

        self.conversation_manager = ConversationManager(self)

    async def on_ready(self):
        await self.poe.setup()
        logging.info(f"Logged in as {self.user} (ID: {self.user.id})")

