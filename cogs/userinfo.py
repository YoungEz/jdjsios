from discord.ext import commands
import discord

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def userinfo(self, ctx,user: discord.Member=None):
        try:
            user = ctx.message.mentions[0]
        except Exception:
            m = ctx.message.author
        roles = []
        for r in member.roles:
            roles.append(r.name)
            bb = "\n".join(roles)

        embed = discord.Embed(color=0xff00ab, description="Informações de: {} !".format(user.name))
        embed.title = "{}".format(user)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="🆔ID:",value=user.id,inline=False)
        embed.add_field(name="📶Menção:",value=user.mention,inline=False)
        embed.add_field(name="🔢Tag:",value=user.discriminator,inline=False)
        embed.add_field(name="📆Criação da Conta:",value=user.created_at.strftime("**%H:%M:%S - %d/%m/20%y**"),inline=False)
        embed.add_field(name="☑️Entrada no Servidor:",value=user.joined_at.strftime("**%H:%M:%S - %d/%m/20%y**"),inline=False)
        embed.add_field(name="📱Atividade:",value=str(user.activity).replace("None", "Nada"))
        embed.add_field(name="📷Avatar Link:",value="[Link](" + user.avatar_url + ")\n",inline=False)
        try:
            embed.add_field(name="Jogando", value=user.game.name, inline=True)
        except:
            pass
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(info(bot))
    print(f'[Comando userinfo] carregado.')
