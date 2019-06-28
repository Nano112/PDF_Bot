import io
import os

from pdf2image import convert_from_path
from pathlib import Path
import discord
import requests




#TODO OPEN TOKEN FROM FILE
TOKEN = 'NTk0MTU1NzA3MzIyODU5NTI5.XRYVJA.u9-_hZkvaKNBoxKoZXHazUIRv9Y'

client = discord.Client()


async def sendPage(c, n):
    r = None
    with io.BytesIO() as output:
        pages = convert_from_path('pdf_file/test.pdf', 200, first_page=n, last_page=n)
        for page_num, page in enumerate(pages):
            page.save('pages/temp', 'PNG')
    with open('pages/temp') as f:
        c.send(file=discord.File(f.read()))


def savePDF():
    pages = convert_from_path('pdf_file/test.pdf', 200)
    for page_num, page in enumerate(pages):
        page.save('pages/page_n'+"{:03d}".format(page_num)+'.jpg', 'JPEG')

@client.event
async def on_message(message):
     # we do not want the bot to reply to itself
     if message.author == client.user:
        return
     attachments = message.attachments
     if len(attachments) == 0:
         return
     url = attachments[0].url
     if(url == None or not url.endswith('.pdf')):
         return
     print(url)
     response = requests.get(url)
     filename = Path('pdf_file/test.pdf')
     filename.write_bytes(response.content)
     savePDF()

     #await sendPage(message.channel, 0)
     for filename in sorted(os.listdir('pages/')):
        print(filename)
        with open('pages/'+filename, 'rb') as f:
             await message.channel.send(file=discord.File(f))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)



