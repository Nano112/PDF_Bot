import io

import discord
from pdf2image import convert_from_path


class Reader:

    def __init__(self, reader, channel, pdf_name = None, page = 0, page_count = 0):
        self.channel = channel
        self.reader = reader
        self.pdf_name = pdf_name
        self.page = page
        self.page_count = page_count

    async def read(self, pdf_name):
        self.pdf_name = pdf_name
        self.page = 1
        await self.sendPage()

    async def next(self):
        if self.page < self.page_count:
            self.page = self.page+1
        else:
            await self.channel.send('End of pdf')
        await self.sendPage()

    async def seak(self, n):
        if n<self.page_count and n>0:
            await self.sendPage()
            self.page = n
        else:
            await self.channel.send('Page n°' + n + ' does not exist')






    async def sendPage(self):
            with io.BytesIO() as output:
                pages = convert_from_path('pdf_files/'+self.pdf_name, 200, first_page=self.page, last_page=self.page + 1)
                pages[0].save('pages/temp.png', 'PNG')
            with open('pages/temp.png', 'rb') as f:
                await self.channel.send(file=discord.File(f))
