from pathlib import Path

import requests


class Temporary_PDF:

    def __init__(self, channel, sender, url,  name):
        self.channel = channel
        self.url = url
        self.sender = sender
        self.name = name

    async def save(self, name = None):
        if name is None:
            name = self.name
        response = requests.get(self.url)
        filename = Path('pdf_files/'+name+'.pdf')
        filename.write_bytes(response.content)
        await self.channel.send(self.name+' was saved')