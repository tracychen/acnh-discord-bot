import discord
from raymond.constants import BOT_THUMBNAIL_URL

CHANGE_LOG = {
    "7/22/2020": [
        "Add command for sea creatures.",
        "Add command for change log.",
        "Add new wedding and summer items.",
        "Remove notice of back-end change when user profile cannot be found.",
        "Update discord.py library to version 1.3.4"
    ]
}

def handle(client, message):
    embed = discord.Embed(colour=discord.Colour.teal())
    embed.set_author(name=f'{client.user.name} Bot Change Log', icon_url=BOT_THUMBNAIL_URL)
    for date in CHANGE_LOG.keys():
        notes_string = ''
        for note in CHANGE_LOG[date]:
            notes_string += f' ∙  {note}\n'
        embed.add_field(name=date, value=notes_string, inline=False)
    embed.set_footer(text='Contact tracy#6666 for feature requests.', icon_url='https://acnhcdn.com/latest/NpcIcon/cat23.png')
    return message.channel.send(embed=embed)
