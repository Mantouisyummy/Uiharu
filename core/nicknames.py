from typing import TYPE_CHECKING, Union

from pymongo.collection import Collection, ReturnDocument

if TYPE_CHECKING:
    from core.bot import Uiharu


class NicknameLocked(Exception):
    pass


class NicknameManager:
    # {
    #     "user_id": int,
    #     "nickname": string,
    #     "locked": boolean
    # }

    def __init__(self, bot: "Uiharu"):
        self.bot = bot
        self.collection: Collection = bot.db["nicknames"]

    def list_nicknames(self, **kwargs) -> dict[int, str]:
        """
        List nicknames from the database.
        :param kwargs: kwargs to pass to the find method
        :return: dict of nicknames, key is user_id, value is nickname
        """
        result = self.collection.find(kwargs)

        return {entry["user_id"]: entry["nickname"] for entry in result}

    def get_nickname(self, **kwargs) -> Union[str, None]:
        """
        Get a nickname from the database.
        :param kwargs: kwargs to pass to the find_one method, possible values are user_id, nickname, locked
        :return: nickname if found, None if not
        """
        result = self.collection.find_one(kwargs)

        if result is None:
            return None

        return result["nickname"]

    def set_nickname(self, user_id: int, force: bool = False, **kwargs):
        """
        Set a nickname in the database.
        :param user_id:
        :param force: Force the nickname to be set, even if it's locked
        :param kwargs: kwargs to pass to the update_one method, possible values are nickname, locked
        """
        if self.collection.find_one({"user_id": user_id, "locked": True}) and not force:
            raise NicknameLocked(f"{user_id} already has a locked nickname")

        self.collection.update_one({"user_id": user_id}, {"$set": kwargs}, upsert=True)

    def lock_nickname(self, user_id: int) -> bool:
        """
        Toggle the locked status of a nickname.
        :param user_id: user_id to lock
        :return: True if locked, False if unlocked
        """
        result = self.collection.find_one_and_update(
            {"user_id": user_id}, {"$bit": {"locked": {"xor": 1}}}, return_document=ReturnDocument.AFTER
        )

        return result["locked"]

    def remove_nickname(self, user_id: int) -> Union[str, None]:
        """
        Remove a nickname from the database.
        :param user_id: user_id to remove
        :return: Original nickname, None if not found
        """
        result = self.collection.find_one_and_delete({"user_id": user_id})

        if result:
            return result["nickname"]

        return None
