import discord, time, datetime
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import asyncio
import nekos
import time
import colorsys
import sys
import subprocess
from pymongo import MongoClient
import os
import pymongo
import json
import traceback
import requests
import datetime
import random

from random import choice





url = os.environ.get('URL')
mongo = MongoClient(url)

prefix = ['-', 'a!', 'A!', 'a-']

artix = commands.Bot(prefix, owner_id=497518244165320734)
print (discord.__version__)
artix.remove_command("help")
start = time.time()

artix.launch_time = datetime.datetime.utcnow()
COLOUR = 0xFFFF00
COR = 0x00ff00
amounts = {}
n = "O Motivo Não Foi Definido."


@artix.event
async def on_ready():
	print(artix.user.name)
	while True:
		await artix.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{str(len(set(artix.get_all_members())))} Jogadores! 👥"))
		await asyncio.sleep(20)
		await artix.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{str(len(set(artix.guilds)))} Partidas! ⚔"))
		await asyncio.sleep(20)
		await artix.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="Evento: Nenhum Evento Acontecendo ⚙"))
		await asyncio.sleep(20)
		await artix.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a!invite - Me Adicione Em Seu Servidor a!vote - me ajude dando um upvote 📈"))
		await asyncio.sleep(20)
		await artix.change_presence(activity=discord.Activity(name="Minha versão: 1.0 📡"))
		await asyncio.sleep(20)



		



    
@artix.event

async def on_message(message):
	await artix.process_commands(message)
	if message.content.lower().startswith(f'<@{artix.user.id}>'):
		await message.channel.send('Olá {} Meu prefixo é ``a!`` para ver meus comandos digite ``a!ajuda`` ou ``a!help``!'.format(message.author.mention))



		
@artix.listen("on_command_error")
async def error_handler(ctx, error):
    error = getattr(error, 'original', error)
    cmd_name = ctx.message.content.split()[0]  #pegar nome do cmd com prefixo

    if isinstance(error, commands.CommandOnCooldown):
        s = error.retry_after
        s = round(s, 2)
        h, r = divmod(int(s), 3600)
        m, s = divmod(r, 60)
        return await ctx.send(
            f'{ctx.author.mention} Você terá que aguardar **{str(h) + "h: " if h != 0 else ""}{str(m) + "m: " if m != 0 else ""}{str(s) + "s" if s != 0 else ""}** para usar este comando novamente.')

    if isinstance(error, commands.MissingPermissions):
        perms = "\n".join(error.missing_perms)
        return await ctx.send(f"**{ctx.message.author.mention} Você precisa das permissões:\n{perms}\n para usar esse comando**")

    if isinstance(error, commands.BotMissingPermissions):
        perms = "\n".join(error.missing_perms)
        return await ctx.send(f"**Não tenho as seguintes permissões:\n{perms}**")

    if isinstance(error, commands.CommandNotFound):
        return await ctx.send(f"**{ctx.message.author.mention} O comanando `{cmd_name}` não foi encontrado em meu sistema. para ver meus comandos digite `a!ajuda`.**")



    # Demais erros vão aparecer apenas no console
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)




    
@artix.command(pass_context=True, aliases=['latency', 'pong'])
@commands.cooldown(1, 2.0, commands.BucketType.user)
async def ping(ctx):
    '''Find the response time in milliseconds.\n`latency` `pong`'''
    ptime = time.time()
    embed = discord.Embed(Title='Ping', color=0x00FF00, description='Calculando...')


    ping3 = await ctx.send(embed=embed)
    ping2 = time.time() - ptime
    ping1 = discord.Embed(Title='Ping', color=0x00FF00, timestamp = datetime.datetime.utcnow())
    ping1.add_field(name='Pong!', value='⌚ `BOT` **{} ms.**\n📡 `API` **{} ms.**'.format(int((round(ping2 * 1000))), int(artix.latency * 1000)))
    ping1.set_footer(text=f'Comando usado pelo {ctx.author}', icon_url=f'{ctx.author.avatar_url}')
    await ping3.edit(embed=ping1)
i = "Você não possui nenhum token em seu inventario"
a = "Você não possui nenhuma espada em seu inventario"
b = "Você não possui nenhuma class em seu inventario"
c = "Você não possui nenhuma armadura em seu inventario"
d = "Você não possui nenhum pet em seu inventario"
e = "Você não possui nenhum booster em seu inventario"
f = "Você não possui badges"
arq = ['Arqueiro', 'arqueiro', 'ARQUEIRO']
cav = ['Cavaleiro', 'cavaleiro', 'CAVALEIRO']
gue = ['Guerreiro', 'guerreiro', 'GUERREIEO']
mag = ['Mago', 'mago', 'MAGO']
@artix.command(pass_context=True)
async def registrar(ctx, nick: str=None, grp: str=None):
	tutorial = mongo['tutorial']
	rpg = tutorial['rpg']
	rpg = tutorial.rpg.find_one({"_id":str(ctx.author.id)})
	if rpg is not None:
		await ctx.send(f'**{ctx.author.mention} Você ja é um guerreiro!**')
	else:
		if nick == None:
			return await ctx.send(f'**{ctx.author.mention}, Em nosso mundo você precisa de um nome!**\n**Use:** `a!registrar [nome] [grupo]`')
		if grp == None:
			return await ctx.send(f'**{ctx.author.mention}, Em nosso mundo você precisara de um grupo para sobreviver!**\n**Use:** `a!registrar [nome] [grupo]`')
		else:

			if grp == arq:
				group = "Arqueiro"

				usuario = {"_id":str(ctx.author.id),"usuario":str(ctx.author.name), "acs":0,"reps":0,"member":False,"life":100,"mana":100, "tokens":i, "espadas":a, "class":b, "armaduras":c, "pets":d, "boosters":e, "badges":f, "lvl":1, "xp": 0, "rankClass":1, "xpClass":0, "nick":nick, "grupo":group}
				tutorial.rpg.insert_one(usuario).inserted_id
			elif grp == gue:
				group = "Guerreiro"
				rpg = tutorial.rpg.find_one({"_id":str(ctx.author.id)})
				usuario = {"_id":str(ctx.author.id),"usuario":str(ctx.author.name), "acs":0,"reps":0,"member":False,"life":100,"mana":100, "tokens":i, "espadas":a, "class":b, "armaduras":c, "pets":d, "boosters":e, "badges":f, "lvl":1, "xp": 0, "rankClass":1, "xpClass":0, "nick":nick, "grupo":group}
				tutorial.rpg.insert_one(usuario).inserted_id
			elif grp == cav:
				group = "Cavaleiro"
				rpg = tutorial.rpg.find_one({"_id":str(ctx.author.id)})
				usuario = {"_id":str(ctx.author.id),"usuario":str(ctx.author.name), "acs":0,"reps":0,"member":False,"life":100,"mana":100, "tokens":i, "espadas":a, "class":b, "armaduras":c, "pets":d, "boosters":e, "badges":f, "lvl":1, "xp": 0, "rankClass":1, "xpClass":0, "nick":nick, "grupo":group}
				tutorial.rpg.insert_one(usuario).inserted_id				
			elif grp == mag:
				group = "Mago"
				rpg = tutorial.rpg.find_one({"_id":str(ctx.author.id)})
				usuario = {"_id":str(ctx.author.id),"usuario":str(ctx.author.name), "acs":0,"reps":0,"member":False,"life":100,"mana":100, "tokens":i, "espadas":a, "class":b, "armaduras":c, "pets":d, "boosters":e, "badges":f, "lvl":1, "xp": 0, "rankClass":1, "xpClass":0, "nick":nick, "grupo":group}
				tutorial.rpg.insert_one(usuario).inserted_id				
			else:
				return await ctx.send(f'**{ctx.author.mention} Este grupo não existe**\n**Grupos existentes:** `arqueiro`,`cavaleiro`,`mago` e `guerreiro`')

			
        
    
@artix.command(pass_context=True)
async def duelo(ctx, user: discord.User=None):
	if user is None:
		await ctx.send('Você não pode duelar com o vento, mecione um usuário.')
	else:
		await ctx.send(f'{ctx.author.mention} desafiou {user.mention} para um duelo!')
		 		 		 		 		 		 		 		 		 		 		 		
						
@artix.command(pass_context=True,aliases=['ajuda','h'])
async def help(ctx):
	member = ctx.message.author
	help_p = discord.Embed(color=0xff00AB)
	help_p.add_field(name="Reaja Para Escolher Uma Categoria", value="👮 **Moderação**\n• comandos como `ban, kick...`\n✨ **Diversão**\n• comandos como `kiss, hug...`\nℹ **Informações**\n• comandos como `ping, avatar...`\n🚀 **Outros**\n• comandos como `pergunta, deathnote...`\n💸 **Economia**\n• comandos como `pagar, saldo...`")
	help_p.set_image(url = 'https://image.ibb.co/caM2BK/help.gif')
	await member.send(f'{member.mention}Duvidas? Entre em Meu Servidor De Suporte\nhttps://discord.gg/KabD5BC')
	await member.send(f'{member.mention} Quer Me Adicionar Em Seu Servidor? Digite `s!invite`')	
	msg = await member.send(embed=help_p)
	await msg.add_reaction('👮')
	await msg.add_reaction('✨')
	await msg.add_reaction('ℹ')
	await msg.add_reaction('🚀')
	await msg.add_reaction('💸')
	
	await ctx.send(f'{member.mention} Verifique Suas Mensagens Privadas.')
	try:
		while True:
			reaction, user = await artix.wait_for("reaction_add", timeout=360, check=lambda reaction, user: reaction.message.id == msg.id and user.id == ctx.author.id)
			emoji = str(reaction.emoji)
			if emoji == '👮':
				await msg.delete()
				embed_help = discord.Embed(description="📙┃Menu de ajuda Moderação")
				embed_help.add_field(name = 'ban ',value ='Como usar ``s!ban <@usuário> [motivo]`` - bane o usuário mencionado',inline = False)
				embed_help.add_field(name = 'kick',value ='Como usar ``s!kick <@usuário> [motivo]`` - Expulsa o usuário mencionado',inline = False)
				embed_help.add_field(name = 'setcargo',value ='Como usar ``s!setcargo <@cargo> <@usuário>`` - seta um cargo algo usuário mencionado',inline = False)
				embed_help.add_field(name = 'lock',value ='Como usar ``s!lock`` - bloqueia o canal para membros',inline = False)
				embed_help.add_field(name = 'unlock',value ='Como usar ``s!unlock`` - desbloqueia o canal para membros',inline = False)
				embed_help.add_field(name = 'mute',value ='Como usar ``s!mute <@usuário> [motivo]`` - Muta o usuário mencionado **DESATIVADO**',inline = False)
				embed_help.add_field(name = 'unmute',value ='Como usar ``s!unmute <@usuário>`` - Desmuta o usuário mencionado **DESATIVADO**',inline = False)	
				embed_help.add_field(name = 'removercargo',value ='Como usar ``s!removercargo <@cargo> <@usuário>`` - remove um cargo algo usuário mencionado',inline = False)
				embed_help.add_field(name = 'clear',value ='Como usar ``s!clear <quantidade>`` - limpa o canal de texto atual',inline = False)
				embed_help.add_field(name = 'avisar',value ='Como usar ``s!avisar <@usuário> [motivo]`` - avisa uma pessoa sobre algo',inline = False)								
				embed_help.set_image(url = 'https://image.ibb.co/caM2BK/help.gif')
				embed_help.add_field(name='-----------------------', value='***<arg> obrigatorio\n[arg] opicional***')												
				msg = await member.send(embed=embed_help)
				await msg.add_reaction('⬅')
			if emoji == '✨':
				await msg.delete()
				embed_help = discord.Embed(description="📙┃Menu de ajuda Ações", color = 0xff00AA)
				embed_help.add_field(name = 'dance ',value ='Como usar ``s!dance`` - dance com algum usuário',inline = False)
				embed_help.add_field(name = 'kiss',value ='Como usar ``s!kiss <@usuário>`` - O amor esta no ar! beije determinado usuário!',inline = False)
				embed_help.add_field(name = 'hug ',value ='Como usar ``s!hug <@usuário>``',inline = False)
				embed_help.add_field(name = 'suicidio ',value ='Como usar ``s!suicidio``',inline = False)
				embed_help.add_field(name = 'matar',value ='Como usar ``s!matar <@usuário>``',inline = False)
				embed_help.add_field(name = 'slap',value ='Como usar ``s!slap <@usuário>`` -  de uns tap cabuloso em alguem que esta te pertubando',inline = False)
				embed_help.add_field(name = 'chorar ',value ='Como usar ``s!chorar``',inline = False)
				embed_help.add_field(name = 'atack',value ='Como usar ``s!atack <@usuário> - ataque o usuário mencionado``',inline = False)
				embed_help.add_field(name = 'brigar',value ='Como usar ``s!brigar <@usuário>`` - brigue com seu amiguinho (não faça isso)',inline = False)
				embed_help.add_field(name = 'voadora',value ='Como usar ``s!voadora <@usuário>`` - de uma voadora no seu amiguinho (não faça isso)',inline = False)
				embed_help.add_field(name = 'meme',value ='Como usar ``s!meme`` - Mostra Um Meme',inline = False)															
				embed_help.set_image(url = 'https://image.ibb.co/caM2BK/help.gif')
				embed_help.add_field(name='-----------------------', value='***<arg> obrigatorio\n[arg] opicional***')				
				msg = await member.send(embed=embed_help)
				
				await msg.add_reaction('⬅')
			if emoji == 'ℹ':
				await msg.delete()
				embed_help = discord.Embed(description="📙┃Menu de ajuda Informações", color=0xff00ab)
				embed_help.add_field(name = 'serverinfo',value ='Como usar ``s!serverinfo`` - veja as informações do servidor atual',inline = False)
				embed_help.add_field(name = 'ping',value ='Como usar ``s!ping`` - Veja meu tempo de resposta',inline = False)
				embed_help.add_field(name = 'avatar',value ='Como usar ``s!avatar<@usuário>`` - Veja O Avatar Do Usuário Mencionado',inline = False)
				embed_help.add_field(name = 'ajuda ',value ='Como usar ``s!ajuda`` Meus comandos',inline = False)
				embed_help.add_field(name = 'userinfo',value ='Como usar ``s!userinfo [@usuário]`` Expulsa o usuário mencionado',inline = False)

				embed_help.add_field(name = 'invite',value ='Como usar ``s!invite`` - Meu convite para caso queira me adicionar em seu servidor',inline = False)
				embed_help.add_field(name = 'vote',value ='Como usar ``s!vote`` - Me Ajude Dando Um Upvote Na Discord Bot List',inline = False)
				embed_help.add_field(name="botinfo", value="Como Usar ``s!botinfo`` Veja minhas informações")
				embed_help.add_field(name="suporte", value="Como Usar ``s!suporte`` Veja meu servidor de suporte")					
				embed_help.add_field(name = 'google',value ='Como usar ``s!google <pesquisa>`` - Faça Uma Pesquisa',inline = False)
										
				embed_help.set_image(url = 'https://image.ibb.co/caM2BK/help.gif')
				embed_help.add_field(name='-----------------------', value='***<arg> obrigatorio\n[arg] opicional***')				
							
				msg = await member.send(embed=embed_help)
				await msg.add_reaction('⬅')
			if emoji == '🚀':
				await msg.delete()
				embed_help = discord.Embed(description="📙┃Menu de ajuda", color=0xff00ab)
				embed_help.add_field(name = 'dog ',value ='Como usar ``s!dog`` - foto aleatoria de um dogão',inline = False)
				embed_help.add_field(name = 'cat',value ='Como usar ``s!cat`` - foto aleatoria de um gato',inline = False)
				embed_help.add_field(name = 'votar',value ='Como usar ``s!votar <mensagem>`` - Inicie uma votação em seu servidor',inline = False)				
				embed_help.add_field(name = 'flipcoin',value ='Como usar ``s!flipcoin`` - Cara Ou Coroa',inline = False)																					
				embed_help.add_field(name='-----------------------', value='***<arg> obrigatorio\n[arg] opicional***')				
				msg = await member.send(embed=embed_help)
				await msg.add_reaction('⬅')
			if emoji == '💸':
					await msg.delete()
					embed_help = discord.Embed(description="📙┃Menu de Economia", color=0xff00ab)
					embed_help.add_field(name = 'pagar',value ='Como usar ``s!pagar <@usuário> <valor>`` - pague o seu amigo(a) usando minha econimia :)',inline = False)
					embed_help.add_field(name = 'saldo',value ='Como usar ``s!saldo`` - Veja quantos **ryucoins** Você tem!',inline = False)
					embed_help.add_field(name = 'rep',value ='Como usar ``s!rep <@usuário>`` - De um ponto de reputação a alguem',inline = False)
					embed_help.add_field(name = 'reps',value ='Como usar ``s!reps [@usuário]`` - Veja quantos pontos de reputação você (ou seu amigo) tem!',inline = False)
					embed_help.add_field(name = 'daily',value ='Como usar ``s!daily`` - Pegue Uma Recompensa Diaria',inline = False)				
					embed_help.add_field(name = 'Trabalhar',value ='Como usar ``s!trabalhar` - Trabalhe e ganhe ryucoins!',inline = False)
					embed_help.add_field(name="perfil", value="Como Usar ``s!perfil [@usuário]`` Veja seu perfil")
					embed_help.add_field(name="registro", value="Como Usar ``s!registro`` Registre-se em meu sistema")
					embed_help.add_field(name="frase", value="Como Usar ``s!frase <frase>`` Adicione Uma Frase A Seu Perfil")
					embed_help.add_field(name="sobre", value="Como Usar ``s!sobre <desc>` Adicione Uma Descrição a seu perfil")
					embed_help.add_field(name="loja", value="Como Usar ``s!loja`` Veja Meu Shop **(Ainda Não Adicionado)**")
					embed_help.add_field(name="casar", value="Como Usar ``s!casar <@usuário>`` Case com sua webnamorada! **(Ainda Não Adicionado)**")					
					embed_help.add_field(name='-----------------------', value='***<arg> obrigatorio\n[arg] opicional***')				
					msg = await member.send(embed=embed_help)
					await msg.add_reaction('⬅')							
			if emoji == '⬅':
				await msg.delete()
				msg = await member.send(embed=help_p)
				await msg.add_reaction('👮')
				await msg.add_reaction('✨')
				await msg.add_reaction('ℹ')
				await msg.add_reaction('🚀')
				await msg.add_reaction('💸')
	except asyncio.TimeoutError:
		await msg.delete() #deletar mensagem após um tempo sem resposta dos reactions
	except Exception as e:
		await msg.delete()
		print(repr(e))


artix.run(str(os.environ.get('BOT_TOKEN')))
