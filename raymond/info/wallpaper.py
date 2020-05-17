from raymond.es.data import get_by_name
from raymond.constants import Commands, COMMAND_PREFIX
from raymond.info.util import build_info_embed

WALLPAPER_ATTRIBUTES = [
    'Buy',
    'Sell',
    'Catalog',
    'Source',
    'Tag',
    'Ceiling Type',
    'Window Type',
    'Window Color',
    'Pane Type',
    'Curtain Type',
    'Curtain Color'
]
FULL_WALLPAPER_COMMAND = COMMAND_PREFIX + Commands.wallpaper.value
WALLPAPER_USAGE = '{} <item name>'.format(FULL_WALLPAPER_COMMAND)


def handle(message):
    item_name = message.content.replace(FULL_WALLPAPER_COMMAND, '').strip().lower()
    if not item_name:
        return message.channel.send('❗Item name not provided, usage is **{}**.'.format(WALLPAPER_USAGE))
    item = get_by_name('wallpapers', item_name, return_attributes=WALLPAPER_ATTRIBUTES, image_attribute='Image')
    if not item:
        return message.channel.send('Uh-oh, item "{}" cannot be found. 🤯'.format(item_name))
    else:
        return message.channel.send(embed=build_info_embed(item['Name'], item['Attributes'], thumbnail=item['Image Link']))
