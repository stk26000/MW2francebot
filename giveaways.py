import asyncio
import datetime
import random

import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions


class giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role("Giveaway Hoster")
    async def gstart(self, ctx, mins: int, *, prize: str):
        em = discord.Embed(
            title="Giveaway",
            description=f"{prize}",
            color=0x2fc300
        )

        secs = mins * 60

        end = datetime.datetime.now() + datetime.timedelta(seconds=secs)

        if end.minute < 10:
            em.add_field(
                name="Ends At:",
                value=f"{end.hour}:0{end.minute}"
            )
        else:
            em.add_field(
                name="Ends At:",
                value=f"{end.hour}:{end.minute}"
            )

        em.set_footer(
            text=f"Se termine {mins} minutes après l'envoi de ce message"
        )
        msg = await ctx.send(embed=em)

        await msg.add_reaction("🎉")

        await asyncio.sleep(secs)

        nmsg = await ctx.channel.fetch_message(msg.id)

        usrs = await nmsg.reactions[0].users().flatten()
        usrs.pop(usrs.index(self.bot.user))

        if not usrs:
            await ctx.send("Personne n'a gagné parce que personne n'a réagi!")
        else:
            winner = random.choice(usrs)

            await ctx.send(f"GG! {winner.mention} a gagné {prize}")

    @gstart.error
    async def gstart_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            error_role = discord.Embed(
                description="Le rôle Giveaway Hoster est requis pour utiliser cette commande ! Veuillez écrire !createrole pour créer ce rôle", color=0x2fc300)
            await ctx.message.channel.send(embed=error_role)
        if isinstance(error, commands.MissingRequiredArgument):
            error_usage = discord.Embed(
                description="Usage correct: !gstart (temps en minutes) (prix)", color=0x2fc300)
            await ctx.send(embed=error_usage)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def createrole(self, ctx):
        await ctx.guild.create_role(name="Giveaway Hoster")
        role_msg = discord.Embed(
            description="Giveaway Hoster role a été réalisé avec succès", color=0x2fc300)
        await ctx.send(embed=role_msg)

    @commands.command()
    @commands.has_any_role("Giveaway Hoster")
    async def gend(self, ctx, id: int):
        try:
            message = await ctx.channel.fetch_message(id)
        except:
            await ctx.send("Giveaway pas trouvé")
            return

        usrs = await message.reactions[0].users().flatten()
        usrs.pop(usrs.index(self.bot.user))

        if not usrs:
            await ctx.send("Personne n'a gagné parce que personne n'a réagi!")
        else:
            winner = random.choice(usrs)

            await message.reply(f"GG! {winner.mention} a gagné!")


def setup(bot):
    bot.add_cog(giveaways(bot))
