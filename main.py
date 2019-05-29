import discord,time, datetime
import asyncio
from discord.ext import commands


bot = commands.Bot(command_prefix="sv!")
bot.remove_command("help")
bot.launch_time = datetime.datetime.utcnow()
startup_extensions = ["cogs.music"]


class Main_Commands():
    def __init__(self, bot):
        self.bot = bot



@bot.event
async def on_ready():
    print("=================================")
    print("Nome: %s" % bot.user.name)
    print("ID: %s" % bot.user.id)
    print("=================================")
    while True:
        delta_uptime = datetime.datetime.utcnow() - bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{str(len(set(bot.get_all_members())))} Seres Humanos No Servidor Do Shiryu!"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Estou online há: {days} dias {hours} Horas {minutes} Minutos {seconds} Segundos"))
        await asyncio.sleep(20)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="Sou Um Bot Especial Do Servidor Do Shiryu!"))
        await asyncio.sleep(10)


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}.{}'.format(type(e).__name__, e)
            print('falha ao carregar extensoes {} . {}'.format(extension, e))
            print(repr(e))
            
@bot.command(pass_context=True, aliases=['latency', 'pong'])
async def ping(ctx):
    '''Find the response time in milliseconds.\n`latency` `pong`'''
    ptime = time.time()
    embed = discord.Embed(Title='Ping', color=0x00FF00)
    embed.add_field(name='Pong!', value='Calculando...')
    embed.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    ping3 = await ctx.send(embed=embed)
    ping2 = time.time() - ptime
    ping1 = discord.Embed(Title='Ping', color=0x00FF00)
    ping1.add_field(name='Pong!', value='{} ms.'.format(int((round(ping2 * 1000)))))
    ping1.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    await ping3.edit(embed=ping1)            


                            
bot.run(str(os.environ.get('BOT_TOKEN')))
