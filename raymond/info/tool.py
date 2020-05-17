from raymond.es.data import get_by_name
from raymond.constants import Commands, COMMAND_PREFIX
from raymond.info.util import build_info_embed

TOOL_ATTRIBUTES = [
    'Buy',
    'Sell',
    'Source',
    'Uses',
    'Customize',
    'Kit Cost'
]
FULL_TOOL_COMMAND = COMMAND_PREFIX + Commands.tool.value
TOOL_USAGE = '{} <item name>'.format(FULL_TOOL_COMMAND)


def handle(message):
    item_name = message.content.replace(FULL_TOOL_COMMAND, '').strip().lower()
    if not item_name:
        return message.channel.send('❗Item name not provided, usage is **{}**.'.format(TOOL_USAGE))
    item = get_by_name('tools', item_name, return_attributes=TOOL_ATTRIBUTES, image_attribute='Image')
    if not item:
        return message.channel.send('Uh-oh, item "{}" cannot be found. 🛠'.format(item_name))
    else:
        return message.channel.send(embed=build_info_embed(item['Name'], item['Attributes'], thumbnail=item['Image Link']))
