from raymond.es.data import get_by_name
from raymond.constants import Commands, COMMAND_PREFIX
from raymond.info.util import build_info_embed

FLOORING_ATTRIBUTES = [
    'Buy',
    'Sell',
    'Catalog',
    'Source',
    'Tag'
]
FULL_FLOORING_COMMAND = COMMAND_PREFIX + Commands.flooring.value
FLOORING_USAGE = '{} <item name>'.format(FULL_FLOORING_COMMAND)


def handle(message):
    item_name = message.content.replace(FULL_FLOORING_COMMAND, '').strip().lower()
    if not item_name:
        return message.channel.send('❗Item name not provided, usage is **{}**.'.format(FLOORING_USAGE))
    item = get_by_name('flooring', item_name, return_attributes=FLOORING_ATTRIBUTES, image_attribute='Image')
    if not item:
        return message.channel.send('Uh-oh, item "{}" cannot be found. 🤯'.format(item_name))
    else:
        return message.channel.send(embed=build_info_embed(item['Name'], item['Attributes'], thumbnail=item['Image Link']))
