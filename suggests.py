from discord.ext import commands
import discord


class suggests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def suggest(self, ctx, *, idea):
        suggestion = discord.Embed(
            description=f"{idea}", color=0x2fc300)
        suggestion.set_footer(
            text="Suggestion de {}".format(ctx.message.author.name))

        reactions = ['👍', '👎']

        message = await ctx.send(embed=suggestion)
        for i in reactions:
            await message.add_reaction(i)

        await ctx.message.delete()


def setup(bot):
    bot.add_cog(suggests(bot))
