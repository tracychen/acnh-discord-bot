from raymond.es.data import get_by_name
from raymond.constants import Commands, COMMAND_PREFIX
from raymond.info.util import build_info_embed

MUSIC_ATTRIBUTES = [
    'Buy',
    'Sell',
    'Catalog',
    'Source',
    'Source Notes',
    'Color 1',
    'Color 2'
]
FULL_MUSIC_COMMAND = COMMAND_PREFIX + Commands.music.value
MUSIC_USAGE = '{} <k.k. slider song name>'.format(FULL_MUSIC_COMMAND)

def handle(message):
    music_name = message.content.replace(FULL_MUSIC_COMMAND, '').strip().lower()
    if not music_name:
        return message.channel.send('❗️Song name not provided, usage is **{}**.'.format(MUSIC_USAGE))
    music = get_by_name('music', music_name, return_attributes=MUSIC_ATTRIBUTES, image_attribute='Album Image')
    if not music:
        return message.channel.send('Uh-oh, "{}" cannot be found. 🔕'.format(music_name))
    else:
        return message.channel.send(embed=build_info_embed(music['Name'], music['Attributes'], thumbnail=music['Image Link']))
