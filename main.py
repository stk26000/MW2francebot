import json

import discord
import os
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='+', intents=intents)
bot.remove_command("help")

extensions = [
    'giveaways',
    'suggests',
    'embed',
    'ticket',
    'moderation'
]

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("MWII France"))

bot.run("MTAyMTEyMzE2ODkxMzYwMDUyMg.Gyqh5J.WQX46BkyflWdCAGy4GXYYc1DZpCg48WMd6qfG0")
