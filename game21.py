import discord
import random
import pymongo
from discord.ext import commands
from discord.utils import get

client = pymongo.MongoClient("mongodb+srv://zero3601:chbsHruosuFhv6XJ@cluster0-1igvs.mongodb.net/test?retryWrites=true&w=majority")
db = client.test
users = db.users
goose = db.goose
goose_disc = db.goose_description

async def addgus(user_name, ctx):
    goose_name = "гачи гусь"
    user = users.find_one({'user_id' : user_name.id})
    if user == None:
        await ctx.send('Вы не зарегестрировались\nЧтобы зарегистрироваться напишите команду !reg')
        return
    if goose_name in user['гуси']:
        return
    users.update_one({'user_id': ctx.author.id}, {'$addToSet':{'гуси':{goose_name: 1}}})
    goose_image = goose.find_one({})[goose_name]
    goose_d = goose_disc.find_one({})[goose_name]
    embed = discord.Embed(title = f'{user_name.name} вам выдан {goose_name}', description=goose_d)
    embed.set_image(url=goose_image)
    await ctx.send(embed=embed)


class Point(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def game21(self, ctx):
        def player_move():
            random_card = random.choice(cards)
            cards.remove(random_card)
            if random_card in cards_bot:
                cards_bot.remove(random_card)
            hand_user.append(random_card)
            return True
        def bot_move(bot_turn):
            if bot_turn == 0:
                if point_bot <= 11:
                    random_card = random.choice(cards_bot)
                    cards_bot.remove(random_card)
                    hand_bot.append(random_card)
                    return True
                elif point_bot == 12:
                    if random.random() < 8 / 10:
                        random_card = random.choice(cards_bot)
                        cards_bot.remove(random_card)
                        hand_bot.append(random_card)
                        return True
                    else:
                        bot_turn = 1
                        return True
                elif point_bot == 13 or point_bot == 14:
                    if random.random() < 6 / 10:
                        random_card = random.choice(cards_bot)
                        cards_bot.remove(random_card)
                        hand_bot.append(random_card)
                        return True
                    else:
                        bot_turn = 1
                        return True
                elif point_bot == 15 or point_bot == 16:
                    if random.random() < 5 / 10:
                        random_card = random.choice(cards_bot)
                        cards_bot.remove(random_card)
                        hand_bot.append(random_card)
                        return True
                    else:
                        bot_turn = 1
                        return True
                elif point_bot >=17:
                    bot_turn = 1
            return True
        def check(reaction, user):
            return user == user_in_game
        if ctx.channel.id not in [700338583525130370, 500114602093445120]:
            await ctx.send("нельзя писать эту команду здесь")
            return
        cards_first = ['♠️2','♠️3','♠️4','♠️5','♠️6','♠️7','♠️валет','♠️дама','♠️король',
            '♣️2','♣️3','♣️4','♣️5','♣️6','♣️7','♣️валет','♣️дама','♣️король',
            '♥️2','♥️3','♥️4','♥️5','♥️6','♥️7','♥️валет','♥️дама','♥️король',
            '♦️2','♦️3','♦️4','♦️5','♦️6','♦️7','♦️валет','♦️дама','♦️король'
        ]
        cards = ['♠️A','♠️2','♠️3','♠️4','♠️5','♠️6','♠️7','♠️8','♠️9','♠️10','♠️валет','♠️дама','♠️король',
            '♣️A','♣️2','♣️3','♣️4','♣️5','♣️6','♣️7','♣️8','♣️9','♣️10','♣️валет','♣️дама','♣️король',
            '♥️A','♥️2','♥️3','♥️4','♥️5','♥️6','♥️7','♥️8','♥️9','♥️10','♥️валет','♥️дама','♥️король',
            '♦️A','♦️2','♦️3','♦️4','♦️5','♦️6','♦️7','♦️8','♦️9','♦️10','♦️валет','♦️дама','♦️король'
        ]
        cards_point = {'♠️2':2,'♠️3':3,'♠️4':4,'♠️5':5,'♠️6':6,'♠️7':7,'♠️8':8,'♠️9':9,'♠️10':10,'♠️валет':2,'♠️дама':3,'♠️король':4,
            '♣️2':2,'♣️3':3,'♣️4':4,'♣️5':5,'♣️6':6,'♣️7':7,'♣️8':8,'♣️9':9,'♣️10':10,'♣️валет':2,'♣️дама':3,'♣️король':4,
            '♥️2':2,'♥️3':3,'♥️4':4,'♥️5':5,'♥️6':6,'♥️7':7,'♥️8':8,'♥️9':9,'♥️10':10,'♥️валет':2,'♥️дама':3,'♥️король':4,
            '♦️2':2,'♦️3':3,'♦️4':4,'♦️5':5,'♦️6':6,'♦️7':7,'♦️8':8,'♦️9':9,'♦️10':10,'♦️валет':2,'♦️дама':3,'♦️король':4
        }
        cards_bot = ['♠️A','♠️6','♠️7','♠️8','♠️9','♠️10','♠️валет','♠️дама','♠️король',
            '♣️A','♣️6','♣️7','♣️8','♣️9','♣️10','♣️валет','♣️дама','♣️король',
            '♥️A','♥️6','♥️7','♥️8','♥️9','♥️10','♥️валет','♥️дама','♥️король',
            '♦️A','♦️6','♦️7','♦️8','♦️9','♦️10','♦️валет','♦️дама','♦️король'
        ]
        hand_user = []
        hand_bot = []
        point_user = 0
        point_bot = 0
        bot_turn = 0
        channel = get(ctx.guild.channels, id = ctx.channel.id)
        user_in_game = ctx.author
        bot_move(bot_turn)
        random_card = random.choice(cards_first)
        cards.remove(random_card)
        if random_card in cards_bot:
            cards_bot.remove(random_card)
        hand_user.append(random_card)
        while True:
            point_user = 0
            point_bot = 0
            for card in hand_user:
                if card[-1] == 'A':
                    residual = 21 - point_user
                    if residual >= 11:
                        point_user = point_user + 11
                    else:
                        point_user = point_user + residual
                else:
                    point_user = point_user + int(cards_point[card])
            for card in hand_bot:
                if card[-1] == 'A':
                    residual_bot = 21 - point_bot
                    if residual_bot >= 11:
                        point_bot = point_bot + 11
                    else:
                        point_bot = point_bot + residual_bot
                else:
                    point_bot = point_bot + int(cards_point[card])
            if point_bot >= 21 or point_bot == 21:
                bot_turn = 1
            if point_user == 21:
                if point_bot == 21:
                    embed_win = discord.Embed(title=f'Ничья, {user_in_game.name} выпустили из подземелья', color = 0x25dc84)
                    embed_win.add_field(name='ваши карты', value=f'{hand_user}', inline = False)
                    embed_win.add_field(name='Карты мастера', value=f'{hand_bot}', inline = False)
                    await channel.send(embed = embed_win)
                else:
                    embed_win = discord.Embed(title=f'{user_in_game.name} выиграл и стал мастером подземелья', color = 0x25dc84)
                    embed_win.add_field(name='ваши карты', value=f'{hand_user}', inline = False)
                    embed_win.add_field(name='Карты мастера', value=f'{hand_bot}', inline = False)
                    await channel.send(embed = embed_win)
                    if random.random() < 1/10:
                        await addgus(user_in_game,ctx)
                return
            elif point_user >= 21:
                if point_bot >= 21:
                    emb = discord.Embed(title=f'Ничья, {user_in_game.name} выпустили из подземелья', color = 0x25dc84)
                    emb.add_field(name='ваши карты', value=f'{hand_user}', inline = False)
                    emb.add_field(name='Карты мастера', value=f'{hand_bot}', inline = False)
                else:
                    emb = discord.Embed(title=f'{user_in_game.name} проиграл очко', color = 0x25dc84)
                    emb.add_field(name='ваши карты', value=f'{hand_user}', inline = False)
                    emb.add_field(name='Карты мастера', value=f'{hand_bot}', inline = False)
                await channel.send(embed = emb)
                return
            embed = discord.Embed(title='Играете на очко', color = 0x25dc84)
            embed.set_author(name=f'{user_in_game}\nВаш противник Ван Даркхолм')
            embed.add_field(name='ваши карты', value=f'{hand_user}', inline = True)
            embed.set_footer(text=f'Если хотите взять карту - нажмите на 🃏\nЕсли хотите вскрыться - нажмите на ❌')
            game_message = await channel.send(embed = embed)
            await game_message.add_reaction('🃏')
            await game_message.add_reaction('❌')
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            if reaction.emoji == '🃏' and user == user_in_game:
                player_move()
                bot_move(bot_turn)
            if reaction.emoji == '❌' and user == user_in_game:
                if point_user > point_bot:
                    embeds = discord.Embed(title=f'{user_in_game.name} выиграл и стал мастером подземелья', color = 0x25dc84)
                    embeds.add_field(name='ваши карты', value=f'{hand_user}', inline = False)
                    embeds.add_field(name='Карты мастера', value=f'{hand_bot}', inline = False)
                    await channel.send(embed = embeds)
                    if random.random() < 1/10:
                        await addgus(user_in_game,ctx)
                elif point_user == point_bot:
                    embeds = discord.Embed(title=f'Ничья, {user_in_game.name} выпустили из подземелья', color = 0x25dc84)
                    embeds.add_field(name='ваши карты', value=f'{hand_user}', inline = False)
                    embeds.add_field(name='Карты мастера', value=f'{hand_bot}', inline = False)
                    await channel.send(embed = embeds)
                elif point_bot == 21:
                    embeds = discord.Embed(title=f'{user_in_game.name} проиграл очко', color = 0x25dc84)
                    embeds.add_field(name='ваши карты', value=f'{hand_user}', inline = False)
                    embeds.add_field(name='Карты мастера', value=f'{hand_bot}', inline = False)
                    await channel.send(embed = embeds)
                elif point_bot > 21:
                    embeds = discord.Embed(title=f'{user_in_game.name} выиграл и стал мастером подземелья', color = 0x25dc84)
                    embeds.add_field(name='ваши карты', value=f'{hand_user}', inline = False)
                    embeds.add_field(name='Карты мастера', value=f'{hand_bot}', inline = False)
                    await channel.send(embed = embeds)
                    if random.random() < 1/10:
                        await addgus(user_in_game,ctx)
                else:
                    embeds = discord.Embed(title=f'{user_in_game.name} проиграл очко', color = 0x25dc84)
                    embeds.add_field(name='ваши карты', value=f'{hand_user}', inline = False)
                    embeds.add_field(name='Карты мастера', value=f'{hand_bot}', inline = False)
                    await channel.send(embed = embeds)
                return

async def setup(bot):
    await bot.add_cog(Point(bot))