# Work with Python 3.6
import discord
from raymond.es.data import *
from raymond.constants import Commands, COMMAND_PREFIX
from raymond import info, misc, user
from elasticsearch import Elasticsearch
from raymond.raymond import Raymond

es = Elasticsearch()
TOKEN = ''

client = discord.Client()

def is_message_for(message, command):
    return message.content.startswith(COMMAND_PREFIX + command.value)

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    raymond = Raymond(client, es)
    if message.author == client.user:
        return

    if not message.content.startswith(COMMAND_PREFIX):
        return

    # misc commands
    if is_message_for(message, Commands.help):
        await misc.help.handle(message)
    elif is_message_for(message, Commands.about):
        await misc.about.handle(client, message)
    elif is_message_for(message, Commands.invite):
        await message.channel.send('**Invite Link:** https://discord.com/oauth2/authorize?client_id=709555457186070629&scope=bot')
    elif is_message_for(message, Commands.crisp):
        await misc.crisp.handle(raymond, message)

    # info commands
    elif is_message_for(message, Commands.fish):
        await info.fish.handle(message)
    elif is_message_for(message, Commands.bug):
        await info.bug.handle(message)
    elif is_message_for(message, Commands.villager):
        await info.villager.handle(message)
    elif is_message_for(message, Commands.clothing):
        await info.clothing.handle(message)
    elif is_message_for(message, Commands.fossil):
        await info.fossil.handle(message)
    elif is_message_for(message, Commands.music):
        await info.music.handle(message)
    elif is_message_for(message, Commands.furniture):
        await info.furniture.handle(message)
    elif is_message_for(message, Commands.flooring):
        await info.flooring.handle(message)
    elif is_message_for(message, Commands.wallpaper):
        await info.wallpaper.handle(message)
    elif is_message_for(message, Commands.tool):
        await info.tool.handle(message)
    elif is_message_for(message, Commands.art):
        await info.art.handle(message)

    # user commands
    elif is_message_for(message, Commands.profile):
        await user.profile.handle(raymond, message)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    activity = discord.Game(name="!help")
    await client.change_presence(status=discord.Status.online, activity=activity)

if __name__ == '__main__':
    client.run(TOKEN)
