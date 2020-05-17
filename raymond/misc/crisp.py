import discord
import random
from raymond.constants import BOT_THUMBNAIL_URL

IMAGE_URLS = [
    'https://cdn.vox-cdn.com/thumbor/ZT6R3ae2rA3U_v1oXvjDl1Ihz18=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/19915760/raymond.jpeg'
]


def handle(raymond, message):
    embed = discord.Embed(colour=discord.Colour.teal())
    embed.set_author(name=raymond.get_client().user.name, icon_url=BOT_THUMBNAIL_URL)
    i = random.randint(0, len(IMAGE_URLS)-1)
    embed.set_image(url=IMAGE_URLS[i])
    return message.channel.send(embed=embed)