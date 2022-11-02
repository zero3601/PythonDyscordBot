import discord
import random
import pymongo
import time
import datetime
import numpy as np
from discord.ext import commands
from discord.utils import get

client = pymongo.MongoClient("mongodb+srv://zero3601:chbsHruosuFhv6XJ@cluster0-1igvs.mongodb.net/test?retryWrites=true&w=majority")
db = client.test
users = db.users
goose = db.goose
goose_disc = db.goose_description



class GusSistem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def bonus(self, ctx):
        async def add_bonus_goose():
            users.update_one({'user_id':ctx.author.id}, { '$set': {'time_open_bonus': datetime.datetime.today()}})
            goose_array = user['гуси']
            check_goose = False
            goose_index = -1
            for goose_user in goose_array:
                goose_index += 1
                if goose_name in goose_user:
                    check_goose = True
                    break
            if check_goose:
                goose_v = goose_array[goose_index]
                goose_value = goose_v[goose_name]
                users.update_one({'user_id': ctx.author.id, f'гуси.{goose_name}': goose_value}, {'$inc': {f"гуси.$.{goose_name}": 1}})
            else:
                users.update_one({'user_id': ctx.author.id}, {'$addToSet':{'гуси':{goose_name: 1}}})
            disc = goose_disc.find_one({})[goose_name]
            goose_url = goose.find_one({})[goose_name]
            embed = discord.Embed(title=f'{ctx.author.name} ваш сегодняшний гусь - {goose_name}', description=f'{disc}')
            embed.set_image(url=goose_url)
            await ctx.send(embed=embed)
        if ctx.channel.id not in [700338583525130370, 500114602093445120]:
            await ctx.send('нельзя писать эту команду здесь')
            return
        rarity = ['common', 'rare', 'epic', 'legendary', 'mystic']
        dict_goose = {
            'common':['белый гусь', 'розовый гусь', 'зелёный гусь', 'синий гусь'], 
            'rare':['огненный гусь', 'пляжный гусь', 'полый гусь'], 
            'epic':['неоновый гусь', 'рейден гусь'], 
            'legendary':['жпепег гусь', 'гусь клетка', 'сэм гусь'], 
            'mystic':['гуррен гусь']
        }
        goose_random = dict_goose[np.random.choice(rarity, p=[0.5, 0.25, 0.135, 0.075, 0.04])]
        goose_name = random.choice(goose_random)
        user = users.find_one({'user_id':ctx.author.id})
        if user == None:
            await ctx.send('Вы не зарегистрировались\nЧтобы зарегистрироваться напишите команду !reg')
            return
        if 'time_open_bonus' not in user:
            await add_bonus_goose()
            return
        time_user = user['time_open_bonus'] + datetime.timedelta(days=1)
        time_today = datetime.datetime.today() 
        if time_user.date() > time_today.date():
            await ctx.send('вы уже получали гуся сегодня')
        else:
            await add_bonus_goose()
        

    @commands.command(aliases=['reg', 'register'])
    async def registration(self, ctx):
        if ctx.channel.id != 700338583525130370:
            await ctx.message.delete()
            message = await ctx.send('нельзя писать эту команду здесь')
            time.sleep(20)
            await message.delete()
            return
        goose_list = ["белый гусь", "розовый гусь", "зелёный гусь", "синий гусь"]
        selected_goose = random.choice(goose_list)
        user = users.find_one({'user_id':ctx.author.id})
        if user == None:
            user = users.insert_one({'user_id': ctx.author.id, 'гуси':[{f'{selected_goose}': 1}]})
            disc = goose_disc.find_one({})[selected_goose]
            goose_url = goose.find_one({})[selected_goose]
            embed = discord.Embed(title=f'{ctx.author.name} за регистрацию вам выдан {selected_goose}', description=f'{disc}')
            embed.set_image(url=goose_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("вы уже зарегестрированы")
    
    @commands.command()
    async def goose(self, ctx, *words):
        if ctx.channel.id not in [700338583525130370, 500114602093445120]:
            await ctx.message.delete()
            mes = await ctx.send('нельзя писать эту команду здесь')
            time.sleep(10)
            await mes.delete()
            return
        user = users.find_one({'user_id': ctx.author.id})
        if user == None:
            await ctx.send('Вы не зарегестрировались\nЧтобы зарегистрироваться напишите команду !reg')
            return
        goose_name = ' '.join(words)
        goose_array = user['гуси']
        check_goose = False
        g = goose.find_one({})
        if goose_name not in g:
            await ctx.send('Такого гуся нет')
            return
        for goose_user in goose_array:
            if goose_name in goose_user:
                check_goose = True
                break
        if check_goose:
            goose_d = goose_disc.find_one({})[goose_name]
            goose_url = goose.find_one({})[goose_name]
            embed = discord.Embed(title=goose_name, description=f'{goose_d}\nКоличество - {goose_user[goose_name]}')
            embed.set_image(url=goose_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send('У вас нет этого гуся')
    
    @commands.command()
    async def allgoose(self, ctx):
        if ctx.channel.id not in [700338583525130370, 500114602093445120]:
            await ctx.message.delete()
            mes = await ctx.send('нельзя писать эту команду здесь')
            time.sleep(10)
            await mes.delete()
            return
        user = users.find_one({'user_id': ctx.author.id})
        if user == None:
            await ctx.send('Вы не зарегестрировались\nЧтобы зарегистрироваться напишите команду !reg')
            return
        goose_user_list = ''
        for goose in user['гуси']:
            for g in goose:
                goose_user_list += f'{g} : {goose[g]}\n'
        embed = discord.Embed(title = f'Гуси пользователя {ctx.author.name}')
        embed.add_field(name = 'гуси:', value = goose_user_list)
        await ctx.send(embed = embed)
    
    @commands.command()
    async def getbonus(self, ctx):
        if ctx.channel.id not in [700338583525130370, 500114602093445120]:
            await ctx.message.delete()
            m = await ctx.send('Нельзя писать эту команду здесь')
            time.sleep(5)
            await m.delete()
            return
        role = get(ctx.guild.roles, id = 674087516755853322)
        if role not in ctx.author.roles:
            await ctx.send('У вас не выполнены условия для выполнения этой команды')
            return
        user = users.find_one({'user_id': ctx.author.id})
        if user == None:
            await ctx.send('Вы не зарегестрировались\nЧтобы зарегистрироваться напишите команду !reg')
            return
        cheek = False
        for g in user['гуси']:
            if 'гей гусь' in g:
                cheek = True
        if cheek:
            await ctx.send('У вас есть этот гусь')
            return
        users.update_one({'user_id': ctx.author.id}, {'$addToSet':{'гуси':{'гей гусь': 1}}})
        goose_image = goose.find_one({})['гей гусь']
        goose_d = goose_disc.find_one({})['гей гусь']
        embed = discord.Embed(title = f'{ctx.author.name} вам выдан гей гусь', description=goose_d)
        embed.set_image(url=goose_image)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GusSistem(bot))