from discord.ext import commands
import discord


class embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send('Titre: ')
        title = await self.bot.wait_for('message', check=check)

        await ctx.send('La description: ')
        desc = await self.bot.wait_for('message', check=check)

        await ctx.send('Channel: ')
        chan = await self.bot.wait_for('message', check=check)

        channel = self.bot.get_channel(int(chan.content))

        embed = discord.Embed(
            title=title.content, description=desc.content, color=0x72d345)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(embed(bot))
