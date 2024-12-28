import discord
import asyncio

intents = discord.Intents.default()
client = discord.Client(intents=intents)

TOKEN = "TOKEN HERE"

aruid=1
armsg=''
flood = "a\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" * 30

lock=True
gcid=1
gcn=''

spam=False
spamid=1
spamn=''
spamd=1

react=False
@client.event
async def on_message(message):
    global aruid
    global armsg

    global react
    global emoji

    global lock
    global gcid
    global gcn

    global spam
    global spamid
    global spamn
    global spamd

    global react
    if message.author.id==int(aruid):
        await message.channel.send(flood+f"{armsg} <@{str(aruid)}>")
    if message.author!=client.user:
        return
    if react:
        await message.add_reaction('☠️')
    if message.content.startswith('.ar '):
        await message.delete()
        aruid = message.content.split()[1].replace('<@', '').replace('>', '')
        armsg = ' '.join(message.content.split()[2:])
    if message.content=='c':
        await message.delete()
        aruid=1
        armsg=''
    if message.content.startswith('.gc ') and lock:
            await message.delete()
            gcid = message.channel.id
            gcn = message.content[3:]
            x=1
            if lock==True:
                while lock:
                    await message.channel.edit(name=f"{gcn} {x}")
                    x += 1
                    await asyncio.sleep(0.01)
                else:
                    x -= 1
    elif message.content == '.stop' and lock:
                await message.delete()
                lock = False
                await message.channel.edit(name='')
                await message.channel.send('isgbrgrnfernhegrger')
    elif message.content == 'isgbrgrnfernhegrger' and not lock:
            await message.delete()
            lock = True

    if message.content.startswith('.ap ') and not spam:
            await message.delete()
            spamid = message.channel.id
            spamid=client.get_channel(int(spamid))
            spamn = message.content[3:]
            spam=True
            if spam:
                while spam:
                    for _ in range(10):
                        await spamid.send(f"{spamn} {spamd}")
                        spamd += 1
                        await asyncio.sleep(0.01)
                    await asyncio.sleep(10)
                else:
                    x -= 1
    elif message.content == '.quit' and spam:
                await message.delete()
                spam=False
                spamid=1
                spamd=1
    if message.content==".react":
        if not react:
            await message.delete()
            react=True
        if react:
            await message.delete()
            react=False

    if message.content=='.help':
        c="""
***```ansi
[2;34mProdigy's Selfbot |PREFIX IS ,|
```***
*```ansi
[2;31mUse Anywhere[0m
```*
**```ansi
[2;32m.ar (UserID/Mention) (Message) - AutoResponder[0m
```**
**```ansi
[2;33m.ap (Message) - AutoPaster
.quit - Stops AP[0m
```**
**```ansi
[2;35m.react - AutoReact[0m
```**
**```ansi
[2;34mGroupchats Only[0m
```**
**```ansi
[2;36m.gc (Message) - GcChanger[0m
```**
**```ansi
[2;31m.stop - stops GcChanger[0m
```**
join discord.gg/backwood
"""
        await message.edit(content=c)

client.run(TOKEN, bot=False)
