from pdf2image import convert_from_path
import discord
#TODO OPEN TOKEN FROM FILE
TOKEN = 'NTk0MTU1NzA3MzIyODU5NTI5.XRYVJA.u9-_hZkvaKNBoxKoZXHazUIRv9Y'

client = discord.Client()

@client.event
async def on_message(message):
     # we do not want the bot to reply to itself
     if message.author == client.user:
        return
     if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)



def savePDF(name):
    pages = convert_from_path('test.pdf',500)
    for  page_num,page in enumerate(pages):
        page.save('page_n'+repr(page_num)+'.jpg','JPEG')