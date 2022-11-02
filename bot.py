from email import message
from os import system
from discord import channel
import config
import discord
import random
import asyncio
import json
import time
import pymongo
import re
import numpy as np
from rusyll import rusyll
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.utils import get
from datetime import datetime, timedelta

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

client_db = pymongo.MongoClient("mongodb+srv://zero3601:chbsHruosuFhv6XJ@cluster0-1igvs.mongodb.net/test?retryWrites=true&w=majority")
db = client_db.test
member_roles = db.member_roles
muted = db.muted
social_credit = db.social_credit

system_social_credit_star_date = datetime(2022, 1, 18)


@client.event
async def on_ready():
    print('бот работает!')

@client.event
async def on_message(message):
    if message.channel.id == 698053783732879400:
        await message.add_reaction('👍')
        await message.add_reaction('❌')
    

    if message.channel.id == 703727328571686953:
        await message.delete(delay=8)

    
    if message.author.id in [293264769375272961, 506463391922257931]:
        if random.random() < 1 / 40:
            await message.channel.send(f'{message.author.mention} душнила')

    
    if message.channel.id == 586697305084788736:
        for emoji in config.EMOJI:
            if emoji in message.content:
                await message.add_reaction(emoji)
        if len(message.reactions) == 0:
            await message.add_reaction('👍')
            await message.add_reaction('👎')
    

    if message.channel.id == 493820286890934284 and message.mention_everyone == False:
        ne_poet = get(message.guild.roles, id = 830814041265143849)
        member = get(message.guild.members, name = message.author.name)
        if ne_poet not in member.roles:
            h = getHaiku(message.content)
            if (h != 0):
                user = message.author.mention
                chan = get(message.guild.channels, id = 810164590058930236)
                await chan.send(f'----------------------------------\n{h}\n\n - {user}\n{message.jump_url}\n----------------------------------')


    if message.content == 'https://tenor.com/view/national-camera-day-vintage-camera-camera-lens-gif-12084416':
        url_zakat = 'https://tenor.com/view/sunset-beach-water-flow-clouds-gif-16976563'
        mes = await message.channel.history(limit = 1, before = message).flatten()
        if mes[0].content == url_zakat:
            lenny = get(message.guild.members, id = 220762084676337674)
            await message.channel.send(lenny.mention)
        
    
    mention_bot = '<@!607898525019144241>'
    mention_bot_mobile = '<@607898525019144241>'
    if mention_bot in message.content or mention_bot_mobile in message.content:
        await message.channel.send('ты хули меня пингуешь')

    
    if message.channel.id == 586981682326798373:
        if len(message.attachments) != 0 or 'http' in message.content:
                await message.add_reaction(get(message.guild.emojis, name = 'PepeCringe'))
                await message.add_reaction(get(message.guild.emojis, name = 'ugh'))
                await message.add_reaction(get(message.guild.emojis, name = 'degHa'))
                await message.add_reaction(get(message.guild.emojis, name = 'KEKW'))
                await message.add_reaction(get(message.guild.emojis, name = 'KEKL'))


    await client.process_commands(message)
        
        
@client.event
async def on_voice_state_update(member, before, after):
    await c_channel(member, after)
    await d_channel(before, after)


async def c_channel(member, after):
    if after.channel == None:
        return
    
    if after.channel.id == 724727777202405527:
        category = get(member.guild.categories, id = 645340595224576000)
        role = get(member.guild.roles, id=748136026039386113)
        if role in member.roles:
            prava = {
                member: discord.PermissionOverwrite(manage_channels=True)
            }
        else:
            prava = {
                member: discord.PermissionOverwrite(manage_channels=True, manage_roles=True)
            }
        chan = await member.guild.create_voice_channel(name=f'канал: {member.name}', overwrites=prava, category=category)
        await member.move_to(chan, reason=None)
        await chan.edit(reason=None, overwrites=prava)

    if after.channel.id == 996499798414872618:
        category = get(member.guild.categories, id = 438775404875087876)
        prava = {
            member: discord.PermissionOverwrite(manage_channels=True, manage_roles=True)
        }
        chan = await member.guild.create_voice_channel(name=f'канал: {member.name}', overwrites=prava, category=category)
        await member.move_to(chan, reason=None)
        await chan.edit(reason=None, overwrites=prava)



async def d_channel(before, after):
    if before.channel == None:
        return
    for channel in after.channel.guild.channels:
        if channel.category_id in [645340595224576000, 438775404875087876]:
            if len(channel.members) == 0:
                if channel.id in [724727777202405527, 996499798414872618, 438775404875087877, 678278311855521837, 637266667977834526, 637266904381259776, 439135089188667402]:
                    continue
                await channel.delete()


@client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot == True:
        return

    if payload.channel_id == 586981682326798373:
        guild = get(client.guilds, id = 493820286890934282)
        channel = get(guild.channels, id = 586981682326798373)
        message = await channel.fetch_message(payload.message_id)

        if message.created_at.date() < system_social_credit_star_date.date():
            return

        if message.author.id == payload.user_id:
            return

        user_social_credit = social_credit.find_one({'user_id': message.author.id})
        if user_social_credit == None:
            social_credit.insert_one({'user_id': message.author.id, 'social_credit_count': 0})
            user_social_credit = social_credit.find_one({'user_id': message.author.id})
        
        reactions_count = 0
        for reaction in message.reactions:
            async for user in reaction.users():
                if user.id == payload.user_id:
                    reactions_count = reactions_count + 1
                    
        if reactions_count > 1:
            return

        social_credit_count_now = user_social_credit['social_credit_count']
        if payload.emoji.name == 'PepeCringe':
            social_credit_count_now = user_social_credit['social_credit_count'] - 10
        if payload.emoji.name == 'ugh':
            social_credit_count_now = user_social_credit['social_credit_count'] - 5
        if payload.emoji.name == 'degHa':
            social_credit_count_now = user_social_credit['social_credit_count'] + 1
        if payload.emoji.name == 'KEKW':
            social_credit_count_now = user_social_credit['social_credit_count'] + 3
        if payload.emoji.name == 'KEKL':
            social_credit_count_now = user_social_credit['social_credit_count'] + 5

        if social_credit_count_now <= -100:
            role = get(guild.roles, id = 692666251629166633)
            await message.author.add_roles(role)

        if social_credit_count_now < -150:
            social_credit_count_now = -150
        elif social_credit_count_now > 100:
            social_credit_count_now = 100

        social_credit.update_one({'user_id': message.author.id}, {'$set': {'social_credit_count': social_credit_count_now}})

    

    if payload.channel_id == 698053783732879400:
        await finding_partner(payload)


@client.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id == 586981682326798373:
        guild = get(client.guilds, id = 493820286890934282)
        channel = get(guild.channels, id = 586981682326798373)
        message = await channel.fetch_message(payload.message_id)
        if message.created_at.date() < system_social_credit_star_date.date():
            return

        if message.author.id == payload.user_id:
            return

        user_social_credit = social_credit.find_one({'user_id': message.author.id})
        if user_social_credit == None:
            return

        for reaction in message.reactions:
            async for user in reaction.users():
                if user.id == payload.user_id:
                    return

        social_credit_count_now = user_social_credit['social_credit_count']
        if payload.emoji.name == 'PepeCringe':
            social_credit_count_now = user_social_credit['social_credit_count'] + 10
        if payload.emoji.name == 'ugh':
            social_credit_count_now = user_social_credit['social_credit_count'] + 5
        if payload.emoji.name == 'degHa':
            social_credit_count_now = user_social_credit['social_credit_count'] - 1
        if payload.emoji.name == 'KEKW':
            social_credit_count_now = user_social_credit['social_credit_count'] - 3
        if payload.emoji.name == 'KEKL':
            social_credit_count_now = user_social_credit['social_credit_count'] - 5

        if social_credit_count_now >= -100:
            role = get(guild.roles, id = 692666251629166633)
            await message.author.remove_roles(role)

        if social_credit_count_now < -150:
            social_credit_count_now = -150
        elif social_credit_count_now > 100:
            social_credit_count_now = 100

        social_credit.update_one({'user_id': message.author.id}, {'$set': {'social_credit_count': social_credit_count_now}})



async def finding_partner(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    embed = message.embeds[0]
    user_embed = embed.author.name
    memb = get(payload.member.guild.members, name=user_embed)
    user = client.get_user(memb.id)
    if payload.emoji.name == '👍':
        await user.send(content=f'{payload.member} этот человек хочет с вами сыграть')
    if payload.emoji.name == '❌':
        if payload.member.name == user_embed:
            await message.delete(delay=None)


@client.event
async def on_member_join(member):
    user = member_roles.find_one({'user_id': member.id})
    if user is None:
        return
    for role_id in user['roles']:
        role = get(member.guild.roles, id = role_id)
        await member.add_roles(role)
    member_roles.delete_one({'user_id': member.id})


@client.event
async def on_member_remove(member):
    id_roles = []
    discord_roles_id = [647174108802449409, 674929537405943808, 529659976726347776, 689250969044910294, 689250969887834251, 689250969887834268, 689249038830403693, 689249038830403730, 689249039325462610, 493820286890934282]
    for role in member.roles:
        if role.id in discord_roles_id:
            continue
        id_roles.append(role.id)
    if len(id_roles) == 0:
        return
    member_roles.insert_one({'user_id': member.id, 'roles': id_roles})


@client.event
async def on_member_update(before, after):
    if len(before.roles) != len(after.roles):
        subscribers_roles_tear1 = 'Бусти25'
        subscribers_roles_tear2 = 'Бусти100'
        subscribers_roles_tear3 = 'Бусти500'
        subscribers_roles_tear200 = 'Бусти200'
        for r in after.roles:
            if r.name == subscribers_roles_tear1:
                role = get(after.guild.roles, id = 950110352790659153)
                await after.add_roles(role)
            if r.name == subscribers_roles_tear2:
                role = get(after.guild.roles, id = 950110482319159362)
                await after.add_roles(role)
            if r.name == subscribers_roles_tear3:
                role = get(after.guild.roles, id = 950110562950463528)
                await after.add_roles(role)
            if r.name == subscribers_roles_tear200:
                role = get(after.guild.roles, id = 1036584047624863764)
                await after.add_roles(role)
            


@client.command()
async def spam(ctx, Emoji: discord.Emoji, n_emoji: int, n_messages: int):
    if ctx.channel.id == 493820286890934284:
        return
    emoji = get(ctx.guild.emojis, name = Emoji.name)
    if emoji is None:
        return
    if n_messages > 30:
        await ctx.send('слишком много')
        return
    for _ in range(n_messages):
        await ctx.send(str(emoji) * n_emoji)

@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount = 1):
    await ctx.channel.purge(limit = amount + 1)
    await ctx.send('https://media.discordapp.net/attachments/922591357732810772/953393105493700668/yeet-1.gif')


@client.command()
async def party(ctx, age: int, game: str, other_inf: str):
    if ctx.channel.id == 703727328571686953:
        if age <= 0:
            await ctx.send('Ты что не рождался?')
            return
        if age > 120:
            await ctx.send('А не слишком ли ты старый?')
            return
        channel = get(ctx.guild.channels, id = 698053783732879400)
        embed = discord.Embed(title='Ищет пати', color = 0x25dc84)
        embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
        embed.add_field(name='Возраст', value=age, inline = True)
        embed.add_field(name='Игра', value=game, inline = True)
        embed.add_field(name='Дополнительная информация', value=other_inf, inline = True)
        embed.set_footer(text=f'Если хотите присоединиться - нажмите на 👍\nЕсли хотите удалить поиск нажмите ❌')
        await channel.send(embed = embed)
    else:
        await ctx.send('Нельзя писать эту команду здесь')

@client.command()
async def flipcoin(ctx):
    if ctx.channel.id == 493820286890934284:
        embed = discord.Embed(title = 'ребро')
        await ctx.send(embed=embed)
        return
    responses = ['орёл', 'решка', 'ребро']
    embed = discord.Embed(title = np.random.choice(responses, p=[0.45, 0.45, 0.1]), color = 0xfff396)
    await ctx.channel.send(embed = embed)


@client.command()
async def dance(ctx):
    emoji = get(ctx.guild.emojis, name='dance')
    await ctx.message.delete()
    await ctx.channel.send(emoji)


@client.command()
async def party_blob(ctx):
    emoji = get(ctx.guild.emojis, name='party_blob')
    await ctx.message.delete()
    await ctx.channel.send(emoji)


@client.command(aliases=['bаn', 'бан', 'bан', 'бaн', 'БАН', 'BAN'])
async def ban(ctx):
    if ctx.author.id == 247758870259302402:
        return
    if ctx.author.id == 601474620394307604:
        await ctx.send("Мы не можем тебя отпустить")
        return
    await ctx.send(f'{ctx.author.mention} забанил сам себя')
    member = get(ctx.guild.members, name=ctx.author.name)
    try:
        await member.ban(reason='забанил сам себя', delete_message_days=0)
    except:
        await ctx.send('Роль выше меня сними')


@client.command()
async def lennyping(ctx):
    role = get(ctx.guild.roles, id = 647174108802449409)
    if role not in ctx.author.roles:
        await ctx.send('у вас нет прав для использования этой команды')
        return
    lenny = get(ctx.guild.members, id = 220762084676337674)
    for _ in range(5):
        await ctx.send(lenny.mention)
    await ctx.send('https://media.tenor.co/videos/8003c2d0816c3d6b15d2916e3ba71272/mp4')


@client.command()
async def ekiraping(ctx):
    members_id = [247758870259302402, 440900007810301972, 424898587261009930, 340483176193458177, 220762084676337674, 256716102761971713, 402102849703510018, 413660081930895361, 452118568189034496, 595147771867299841]
    if ctx.author.id not in members_id:
        await ctx.send('вы не можете использовать эту команду')
        return
    ekira = get(ctx.guild.members, id = 478146653258514432)
    for _ in range(5):
        await ctx.send(ekira.mention)


@client.command()
async def roll(ctx, min_number: int, max_number: int):
    max_n = max_number + 1
    await ctx.send(random.randrange(min_number, max_n))


@client.command()
async def get_member_by_id(ctx, id_member: int):
    if ctx.author.id != 424898587261009930:
        ctx.send('вы не можете использовать эту команду')
        return
    member = get(ctx.guild.members, id = id_member)
    if member is None:
        await ctx.send('такого пользователся нет на сервере')
        return
    await ctx.send(member.mention)


@client.command()
async def hartping(ctx):
    if ctx.author.id == 601474620394307604:
        await ctx.send('а тебе нельзя')
        return
    member = get(ctx.guild.members, id = 340483176193458177)
    for _ in range(5):
        await ctx.send(member.mention + 'когда дс и дмс? а?')


@client.command()
async def rexping(ctx):
    member = get(ctx.guild.members, id = 601474620394307604)
    for _ in range(5):
        await ctx.send(member.mention)


@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, form: str, count:int):
    role = get(member.guild.roles, id = 867767778395553843)
    await member.add_roles(role)
    m = muted.find_one({'member_id': member.id})
    if m is not None:
        print('этот пользователь уже замючен')
        return
    now = datetime.now()
    d = 0
    f = ''
    if form == 'm':
        d = now + timedelta(minutes=count)
        f = 'минут'
    elif form == 'h':
        d = now + timedelta(hours=count)
        f = 'час'
    elif form == 'd':
        d = now + timedelta(days=count)
        f = 'дней'
    if d == 0:
        await ctx.send('время введино не правильно')
        return
    muted.insert_one({'member_id': member.id, 'mute_end': d})
    await ctx.send(f'Пользователь {member.mention} замучен на {count} {f}')


@client.command()
async def sc(ctx):
    social_credit_count = social_credit.find_one({'user_id': ctx.author.id})
    if social_credit_count == None:
        await ctx.send('у вас 0 social credit')
        return
    sc = social_credit_count['social_credit_count']
    await ctx.send(f'у вас {sc} social credit')


@client.command()
@commands.has_permissions(administrator=True)
async def set_social_credit(ctx, member: discord.Member, social_credit_count):
    if ctx.guild.id != 493820286890934282:
        return
    social_credit_member = social_credit.find_one({'user_id': member.id})
    if social_credit_member == None:
        return
    social_credit.update_one({'user_id': member.id}, {'$set': {'social_credit_count': social_credit_count}})

    
def getHaiku(text):
    text = text.replace('\n', ' ')
    text = text.replace('@everyone', '@ everyone')
    text = text.replace('@here', '@ here')
    syllables = rusyll.token_to_syllables(text)
    if (len(syllables) == 17):
        haiku = [[], [], []]
        words = re.sub(r'/\s+/g', ' ', text).split(' ')
        i = 0
        for word in words:
            haiku[i].append(word)
            paragraphSyllableCount = len(rusyll.token_to_syllables(' '.join(haiku[i])))
            maxSyllables = [5, 7, 5]
            if (paragraphSyllableCount == maxSyllables[i]):
                i += 1
                continue
            if (paragraphSyllableCount > maxSyllables[i]):
                return 0
        retnText = '\n'.join(map(lambda line: ' '.join(line), haiku))
        return retnText
    return 0

async def main():
    async with client:
        await client.load_extension('game21')
        await client.load_extension('sistemgus')
        await client.load_extension('unmute')
        await client.start(config.TOKEN)

asyncio.run(main())