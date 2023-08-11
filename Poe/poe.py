from async_poe_client import Poe_Client


class PoeClient(Poe_Client):
    def __init__(self, pb_token: str, formkey: str):
        self.token: str = pb_token
        self.formkey: str = formkey

        super().__init__(p_b=pb_token, formkey=formkey)

    async def setup(self):
        await self.create()

    async def chat(self, botname:str, text:str):
        sentences = []
        async for message in self.ask_stream(url_botname=botname, question=text):
            sentences.append(message)

        result = "".join(sentences)

        return result

    async def remove_chat(self, botname: str):
        await self.send_chat_break(url_botname=botname)
