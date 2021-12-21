import discord
from discord.ext import commands, tasks
import os
import datetime
from pytz import timezone
import json
import asyncio
import coinmarketcap

# put your discord token in discord_tokens.py    
from discord_tokens import cryptobot_token

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def crypto(ctx, *args):
    out = await coinmarketcap.getquotes(args)
    await ctx.send(out)


bot.run(cryptobot_token)

