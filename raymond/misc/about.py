import discord
import platform
from raymond.constants import BOT_THUMBNAIL_URL

def handle(client, message):
    embed = discord.Embed(colour=discord.Colour.teal())
    embed.set_author(name=client.user.name, icon_url=BOT_THUMBNAIL_URL)
    embed.add_field(name='Python', value=platform.python_version(), inline=False)
    embed.add_field(name='Library', value='[discord.py](https://discordpy.readthedocs.io/)', inline=False)
    embed.add_field(name='Servers', value=str(len(client.guilds)), inline=False)
    embed.add_field(name='Developer', value='[tracy#6666](https://discordapp.com/users/360717490013339669)', inline=False)
    embed.add_field(name='Invite Link', value='[Click Here](https://discord.com/oauth2/authorize?client_id=709555457186070629&scope=bot)', inline=False)
    embed.add_field(name='Vote for Bot', value='[Click Here](https://top.gg/bot/709555457186070629/vote)', inline=False)
    embed.set_footer(text='Bot last updated 7/22/2020.')
    # embed.set_thumbnail(url='https://acnhcdn.com/latest/NpcIcon/cat23.png')
    return message.channel.send(embed=embed)
