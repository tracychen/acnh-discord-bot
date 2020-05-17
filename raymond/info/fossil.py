from raymond.es.data import get_by_name
from raymond.constants import Commands, COMMAND_PREFIX
from raymond.info.util import build_info_embed

FOSSIL_ATTRIBUTES = [
    'Sell',
    'Museum',
    'Size',
    'Interact'
]
FULL_FOSSIL_COMMAND = COMMAND_PREFIX + Commands.fossil.value
FOSSIL_USAGE = '{} <fossil name>'.format(FULL_FOSSIL_COMMAND)

def handle(message):
    fossil_name = message.content.replace(FULL_FOSSIL_COMMAND, '').strip().lower()
    if not fossil_name:
        return message.channel.send('❗️Fossil name not provided, usage is **{}**.'.format(FOSSIL_USAGE))
    fossil = get_by_name('fossils', fossil_name, return_attributes=FOSSIL_ATTRIBUTES, image_attribute='Image')
    if not fossil:
        return message.channel.send('Uh-oh, fossil "{}" cannot be found. 🐛'.format(fossil_name))
    else:
        return message.channel.send(embed=build_info_embed(fossil['Name'], fossil['Attributes'], thumbnail=fossil['Image Link']))
