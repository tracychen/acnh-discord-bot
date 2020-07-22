from raymond.es.data import get_by_name
from raymond.constants import Commands, COMMAND_PREFIX
from raymond.info.util import build_info_embed

CLOTHING_ATTRIBUTES = [
    'Type',
    'Buy',
    'Sell',
    'Catalog',
    'Source',
    'DIY',
    'Seasonal Availability',
    'Style',
    'Label Themes',
]

FULL_CLOTHING_COMMAND = COMMAND_PREFIX + Commands.clothing.value
CLOTHING_USAGE = '{} <clothing name>'.format(FULL_CLOTHING_COMMAND)


def handle(message):
    clothing_name = message.content.replace(FULL_CLOTHING_COMMAND, '').strip().lower()
    if not clothing_name:
        return message.channel.send('❗Clothing name not provided, usage is **{}**.'.format(CLOTHING_USAGE))
    clothing = get_by_name('clothing', clothing_name, return_attributes=CLOTHING_ATTRIBUTES, image_attribute='Closet Image')
    if not clothing:
        return message.channel.send('Uh-oh, item "{}" cannot be found. 👔'.format(clothing_name))
    else:
        return message.channel.send(embed=build_info_embed(clothing['Name'], clothing['Attributes'], thumbnail=clothing['Image Link']))
