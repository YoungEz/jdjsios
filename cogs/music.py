import discord
import asyncio
import itertools
import json
import math
import random
import youtube_dl

from discord.ext import commands
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from discord import opus
from resources.utility import parse_duration
from collections import Counter



cont = Counter()
color = 0xff00ab
opus_libs_dll = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']
youtube_dl.utils.bug_reports_message = lambda: ' '
last_search = {}


def load_opus_lib(opus_libs=None):
    if opus_libs is None:
        opus_libs = opus_libs_dll
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass

    raise RuntimeError('Could not load an opus lib. Tried %s' %
                       (', '.join(opus_libs)))


load_opus_lib()

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')
        self.duration = int(data.get('duration'))

    def __str__(self):
        return f'**{self.title}** *[Duration: {parse_duration(self.duration)}]*'

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            data = data['entries'][0]
            embed= discord.Embed(title='Musica Adicionada',description=f'**🎤 | A Musica Adicionada:**`{data["title"]}`** foi adicionada na fila \n**Por:** `{ctx.author}`\n**Duração:** `{parse_duration(int(data.get("duration")))}`', color=0xff0000)

        await ctx.send(embed=embed)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title'],
                    'duration': data['duration']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=True)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class SongQueue(asyncio.Queue):
    def __iter__(self):
        return self._queue.__iter__()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, value: int):
        self._queue.rotate(-value)
        self._queue.pop()
        self._queue.rotate(value - 1)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return list(itertools.islice(self._queue, index.start, index.stop, index.step))
        else:
            return self._queue[index]

    def __len__(self):
        return len(self._queue)

    @property
    def queue(self):
        return self._queue


class MusicPlayer:
    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume', 'repeat',
                 'search', 'cont_')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = SongQueue()
        self.next = asyncio.Event()

        self.np = None
        self.volume = .5
        self.current = None
        self.repeat = False
        self.search = None
        self.cont_ = {}

        ctx.bot.loop.create_task(self.player_loop(ctx))

    async def player_loop(self, ctx):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                async with timeout(300):
                    if self.repeat and last_search[ctx.guild.id] is not None:
                        if ctx.guild.id not in self.cont_:
                            self.cont_[ctx.guild.id] = 0
                        if self.cont_[ctx.guild.id] == len(last_search[ctx.guild.id]):
                            self.cont_[ctx.guild.id] = 0
                        self.search = str(last_search[ctx.guild.id][self.cont_[ctx.guild.id]])
                        self.cont_[ctx.guild.id] += 1
                        source = await YTDLSource.create_source(ctx, self.search, loop=self.bot.loop, download=False)
                        await self.queue.put(source)
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)
            except IndexError:
                continue

            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except IndexError as e:
                    await self._channel.send(f'Ocorreu um erro ao processar sua música.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source
            try:
                self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            except AttributeError:
                pass
            except discord.errors.ClientException:
                pass

            if self.queue is not None:
            	embed = discord.Embed(title="infoemações Musica", color=0xff00ab)
            	embed.add_field(name="**🎤|Tocando agora:**", value=f'`{source.title}`')
            	embed.add_field(name="**🕐|Duração:**", value=f'`{parse_duration(int(data.get("duration")))}`')
            	embed.add_field(name="Pedido Por",value=f"{source.requester}")
            	self.np = await self._channel.send(embed=embed)
            await self.next.wait()

            if not self.repeat:
                self.cont_[ctx.guild.id] = 0
                last_search[ctx.guild.id] = list()

            source.cleanup()
            self.current = None

            try:
                await self.np.delete()
            except discord.HTTPException:
                pass

            if len(self.queue) == 0 and not self.repeat:
                await ctx.send('<:erro:581791491467378699>│``As músicas acabaram!')

    def destroy(self, guild):
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class GuildState:

    def __init__(self):
        self.skip_votes = set()

    @staticmethod
    def is_requester(ctx):
        return ctx.voice_client.source.requester == ctx.author


class MusicDefault(commands.Cog):
    __slots__ = ('bot', 'players', 'states')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.states = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def _vote_skip(self, channel, member):
        state = self.get_state(channel.guild)
        state.skip_votes.add(member)
        users_in_channel = len([member for member in channel.members if not member.bot])
        if (float(len(state.skip_votes)) / users_in_channel) >= 0.5:
            channel.guild.voice_client.stop()

    def get_state(self, guild):
        if guild.id in self.states:
            return self.states[guild.id]
        else:
            self.states[guild.id] = GuildState()
            return self.states[guild.id]

    @staticmethod
    async def __local_check(ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    
    @commands.command(name='connect', aliases=['join', 'entrar'])
    async def _connect(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise commands.CheckFailure('<:erro:581791491467378699>│``Nenhum canal para participar. '
                                            'Por favor, especifique um canal válido ou entre em um!``')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise commands.CheckFailure(f'<:oc_status:519896814225457152>│Mover para o canal: '
                                            f'<{channel}> tempo esgotado.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise commands.CheckFailure(f'<:oc_status:519896814225457152>│Conectando ao canal: '
                                            f'<{channel}> tempo esgotado.')

        await ctx.send(f'<:on_status:519896814799945728>│Conectado a: **{channel}**', delete_after=20)
    @commands.command(name='play', aliases=['sing', 'tocar'])
    async def play_(self, ctx, *, search: str = "Ashley escape the fate"):
        await ctx.trigger_typing()
        vc = ctx.voice_client

        try:
            channel = ctx.author.voice.channel
            if channel:
                pass
        except AttributeError:
            raise commands.CheckFailure('<:oc_status:519896814225457152>│``Entre num canal de voz!``')

        if not vc:
            last_search[ctx.guild.id] = list()
            await ctx.invoke(self._connect)

        player = self.get_player(ctx)

        if ctx.guild.id not in last_search:
            last_search[ctx.guild.id] = list()
        last_search[ctx.guild.id].append(search)
        if last_search[ctx.guild.id] is not None:
        	source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
        	await player.queue.put(source)
            
def setup(bot):
    bot.add_cog(MusicDefault(bot))
    print('\033[1;32mOs comandos de \033[1;34mMUSICAS\033[1;32m foram carregados com sucesso!\33[m')
            
