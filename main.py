import os
import discord
from discord.ext import commands

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

ROLES = ['R5','R4','War Team','Veteran','Member','Recruit']
STRUCTURE = {
    '📌 INFORMATION':['📢・announcements','📜・rules','📅・event-calendar'],
    '💬 COMMUNITY':['💬・general-chat','😂・memes','📸・screenshots'],
    '❄️ WHITEOUT SURVIVAL':['⚔️・war-planning','🏰・fortress','🚚・truck','🧊・winter-siege','👑・svs'],
    '🔒 LEADERS':['👑・r5-room','🛡️・r4-room','📋・strategy'],
    '🔊 VOICE':['🔊・General','⚔️・War-Room','💤・AFK']}
LEADER_CHANNELS = {'👑・r5-room','🛡️・r4-room','📋・strategy'}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} ({bot.user.id})')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    guild = ctx.guild
    role_map = {}
    for name in ROLES:
        role = discord.utils.get(guild.roles, name=name)
        if role is None:
            role = await guild.create_role(name=name, reason='GAL server setup')
        role_map[name] = role
    r5, r4 = role_map['R5'], role_map['R4']
    for category_name, channels in STRUCTURE.items():
        category = discord.utils.get(guild.categories, name=category_name)
        if category is None:
            kwargs = {}
            if category_name == '🔒 LEADERS':
                kwargs['overwrites'] = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    r5: discord.PermissionOverwrite(view_channel=True),
                    r4: discord.PermissionOverwrite(view_channel=True)}
            category = await guild.create_category(category_name, reason='GAL server setup', **kwargs)
        for channel_name in channels:
            if discord.utils.get(guild.channels, name=channel_name):
                continue
            if channel_name in LEADER_CHANNELS:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    r5: discord.PermissionOverwrite(view_channel=True),
                    r4: discord.PermissionOverwrite(view_channel=True)}
                await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
            elif category_name == '🔊 VOICE':
                await guild.create_voice_channel(channel_name, category=category)
            else:
                await guild.create_text_channel(channel_name, category=category)
    await ctx.send('✅ Struktur server [GAL] berhasil dibuat!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ Hanya Administrator yang dapat menjalankan `!setup`.')
    elif not isinstance(error, commands.CommandNotFound):
        print(f'Command error: {error}')

if not TOKEN:
    raise RuntimeError('DISCORD_BOT_TOKEN belum diatur sebagai environment variable.')
bot.run(TOKEN)
