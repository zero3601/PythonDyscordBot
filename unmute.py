import discord
import random
import time
from discord import channel
from discord import guild
from discord.errors import NotFound
import pymongo
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime

client = pymongo.MongoClient("mongodb+srv://zero3601:chbsHruosuFhv6XJ@cluster0-1igvs.mongodb.net/test?retryWrites=true&w=majority")
db = client.test
muted = db.muted
class unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def cog_load(self):
        self.unmuted_member.start()
        self.birthday_check.start()

    async def cog_unload(self):
        self.unmuted_member.cancel()
        self.birthday_check.cancel()


    @tasks.loop(minutes=1)
    async def unmuted_member(self):
        now = datetime.now()
        for m in muted.find({}):
            d = m["mute_end"]
            id_m = m["member_id"]
            if now >= d:
                guild = await self.bot.fetch_guild(493820286890934282)
                try:
                    member = await guild.fetch_member(id_m)
                except NotFound:
                    muted.delete_one(m)
                    return
                role = get(guild.roles, id = 867767778395553843)
                print(role.name)
                await member.remove_roles(role)
                muted.delete_one(m)
                for c in await guild.fetch_channels():
                    if c.name == 'балаболим':
                        await c.send(f'{member.mention} размучен')
                        break


    @tasks.loop(hours=1)
    async def birthday_check(self):
        this_time = datetime.now()
        if this_time.hour != 7:
            return
        curent_guild = get(self.bot.guilds, id = 493820286890934282)
        try:
            channel = get(curent_guild.channels, id = 493820286890934284)
            birthday_threads = get(curent_guild.threads, id = 877311056849027144)
            async for message in birthday_threads.history():
                if len(message.content) < 5:
                    continue
                if message.content[2] != '.':
                    continue
                if int(message.content[:2]) == this_time.day and int(message.content[3:5]) == this_time.month:
                    await channel.send('Сегодня др у пирожочка' + message.author.mention + '!')
        except AttributeError:
            pass


async def setup(bot):
    await bot.add_cog(unmute(bot))