import asyncio
import datetime
import json
import random

import discord
from discord.ext import commands


class ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def delchannel(self, ctx):
        print(ctx.channel.name)
        if 'ticketnum-' in ctx.channel.name:
            await ctx.channel.delete()
        else:
            return

    @commands.command()
    async def create_message(self, ctx):

        embed = discord.Embed(
            title="Réagissez à ce message avec le ticket pour créer un nouveau ticket!",
            colour=discord.Colour.gold()
        )

        msg = await ctx.send(embed=embed)
        channel = ctx.channel
        guild = ctx.guild

        with open('info.txt', 'w') as f:
            f.flush()
            f.write(str(channel.id))
            f.write('\n')
            f.write(str(msg.id))
            f.write('\n')
            f.write(str(guild.id))

        await msg.add_reaction("🎫")
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        with open('info.txt', 'r') as f:
            data = f.read().split('\n')

        if payload.member == self.bot.user:
            return
        ran = random.randint(1, 10001)
        message = await self.bot.get_channel(int(data[0])).fetch_message(int(data[1]))

        if payload.emoji.name == "🎫":
            guild = self.bot.get_guild(int(data[2]))
            await message.remove_reaction("🎫", payload.member)
            new_channel = await guild.create_text_channel(f'ticketnum-{ran}', type=discord.ChannelType.text)
            await new_channel.set_permissions(guild.default_role, view_channel=False)
            await new_channel.set_permissions(payload.member, view_channel=True)


def setup(bot):
    bot.add_cog(ticket(bot))
