
import discord

from PDF_files import PDF_files
from Reader import Reader
from Temporay_PDF import Temporary_PDF

temp_PDF = {}
readers = {}
files = PDF_files()

# TODO OPEN TOKEN FROM FILE
TOKEN = 'NTk0MTU1NzA3MzIyODU5NTI5.XRYVJA.u9-_hZkvaKNBoxKoZXHazUIRv9Y'

client = discord.Client()

async def savePDF(channel, sender, name = None):
    pdf = temp_PDF[sender.id]
    if pdf is None:
        await channel.send(sender.name + ' you must upload a pdf first')
        return
    if name is not None:
        pdf.name = name
    await pdf.save()
    files.reload()


async def get_PDF(attachments, author, channel):
    url = attachments[0].url
    if url is None or not url.endswith('.pdf'):
        return
    await channel.send("To save pdf type pdf save if you want a custome name type pdf save \"name\"")
    name = attachments[0].filename
    print('Got pdf called ' + name + ' from ' + repr(author.name) + ' url:' + url)
    temp_PDF[author.id] = Temporary_PDF(channel, author.id, url, name)


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    author = message.author
    if author == client.user:
        return
    channel = message.channel
    content = message.content
    attachments = message.attachments

    if len(attachments) != 0:
        await get_PDF(attachments, author, channel)
        return
    # message is a command for the bot
    if content.startswith('pdf '):
        print('Got message from' + repr(author.name) + 'the message contains ' + content)
        content = content[4:]
        if content == 'test':
            await channel.send('test')
            return
        if content[:4] == 'save':
            content = content[4:]
            content = content.lstrip()
            if content != '':
                await savePDF(channel, author, content)
                return
            else:
                await savePDF(channel, author)
                return

        if content == 'list':
            embed = discord.Embed(description='List of available PDF\'s')
            for i, file in enumerate(files.list()):
                embed.add_field(name = '{:03d}'.format(i+1)+': ', value=file[:-4])
            await channel.send(embed=embed)

        if content[:4] == 'read':
            content = content[4:]
            content = content.lstrip()
            if content == '':
                await channel.send('pdf read requires a name type pdf list to see available pdf\'s')
                return
            if files.does_exist(content+'.pdf'):
                readers[author.id] = Reader(author, channel, content, 0, files.get_page_count(content+'.pdf'))
                await readers[author.id].read(content+'.pdf')
            else:
                await channel.send(content+' is not a valid pdf')
            return

        if content[:4] == 'next':
            if author.id in readers:
                await readers[author.id].next()
            else:
                await channel.send('You need to read a pdf first ex: pdf read hello.pdf')
            return

        if content[:4] == 'seek':
            content = content[4:]
            content = content.lstrip()
            page = 0
            try:
                page = int(content)
            except ValueError:
                await channel.send('wrong use of seak pdf seak \'num\'')
                return
            if author.id in readers:
                await readers[author.id].seak(page)
            else:
                await channel.send('You need to read a pdf first ex: pdf read hello.pdf')
            return


        if content[:6] == 'status':
            if author.id in readers:
                embed = discord.Embed(description='Reading status')
                embed.add_field(name="File Name", value=readers[author.id].pdf_name)
                embed.add_field(name="Page Count", value=readers[author.id].page_count)
                embed.add_field(name="Current Page", value=readers[author.id].page)
                await channel.send(embed=embed)
            return

        if content[:4] == 'help':
            embed=discord.Embed(title='Help')
            embed.add_field(name='Upload', value='Upload a pdf file to start')
            embed.add_field(name='Save', value='Type \"pdf save [name]\" to save pdf')
            embed.add_field(name='List', value='Type \"pdf list\" to list readable pdf files')
            embed.add_field(name='Read', value='Type \"pdf read [pdf name]\" to read a pdf')
            embed.add_field(name='Status', value='Type \"pdf status\" to see reading status')
            embed.add_field(name='Next', value='Type \"pdf next\" to get next page')
            embed.add_field(name='Seek', value='Type \"pdf status\" to seek a page')
            await channel.send(embed=embed)




    # await sendPage(message.channel, 0)
    # for filename in sorted(os.listdir('pages/')):
    #   print(filename)
    #   with open('pages/'+filename, 'rb') as f:
    #        await message.channel.send(file=discord.File(f))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
