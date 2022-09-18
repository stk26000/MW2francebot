import asyncio
import datetime
import json
import random

import discord
from discord.ext import commands

from creation import create_warns, get_warn_data


class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, *, amount):
        await ctx.channel.purge(limit=int(amount))
        await ctx.send(f"Vous avez supprimé {amount} messages!", delete_after=3)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.User, *, reason=None):
        await create_warns(member)

        user = str(member.id)

        data = await get_warn_data()

        if member == ctx.message.author:
            await ctx.send("Vous ne pouvez pas vous avertir!")
            return

        if member == None and reason == None:
            await ctx.send("Vous ne pouvez avertir personne!")
            return

        if reason == None:
            await ctx.send("Vous devez mettre une raison!")
            return

        if member != None and reason != None:
            data[user]["Warns"] += 1

            with open('reports.json', 'w') as f:
                json.dump(data, f)

            if data[user]["Warns"] == 3:
                await member.kick(reason=None)

            if data[user]["Warns"] == 1:
                await ctx.send(f"<@{member.id}> a été prévenu pour ``{reason}``. Ils ont maintenant {data[user]['Warns']} avertissements!")

        with open('warns.json', 'w') as f:
            json.dump(data, f)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warnings(self, ctx, member: discord.User):

        await create_warns(member)

        user = str(member.id)

        data = await get_warn_data()

        embed = discord.Embed(
            title=f'{member}',
            colour=discord.Colour.green()
        )
        embed.add_field(name=f'Warnings',
                        value=f'{data[user]["Warns"]}')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="Made by palm#0923")
        embed.set_author(name=f'{member}', icon_url=member.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.User, *, reason=None):
        if member == ctx.message.author:
            await ctx.channel.send("Vous ne pouvez pas vous interdire")
            return

        if member == None:
            await ctx.send("Vous ne pouvez bannir personne!")
            return

        if reason == None:
            reason = "Bannir!"
            await member.ban(reason=reason)

        if reason != None:
            await member.ban(reason=reason)

        message = f"Vous avez été banni de {ctx.guild.name} pour {reason}!"

        await member.send(message)
        # await ctx.guild.ban(member, reason=reason)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.User, *, reason=None):
        if member == None or member == ctx.message.author:
            await ctx.channel.send("Vous ne pouvez pas vous expulsez")
            return
        if reason == None:
            reason = "L"
            await member.kick(reason=reason)
        message = f"Vous avez été expulsé de {ctx.guild.name} pour {reason}!"

        if reason != None:
            await member.kick(reason=reason)

        await ctx.channel.send(f"{member} a été frappé!")
        await member.send(message)


def setup(bot):
    bot.add_cog(moderation(bot))
