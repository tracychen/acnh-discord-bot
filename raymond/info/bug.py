from raymond.es.data import get_by_name
from raymond.constants import Commands, COMMAND_PREFIX
from raymond.info.util import build_info_embed

BUG_ATTRIBUTES = [
    'Sell',
    'Where/How',
    'Weather',
    'Total Catches to Unlock',
    'Northern Months',
    'Southern Months',
    'Time'
]

FULL_BUG_COMMAND = COMMAND_PREFIX + Commands.bug.value
BUG_USAGE = '{} <bug name>'.format(FULL_BUG_COMMAND)


def handle(message):
    bug_name = message.content.replace(FULL_BUG_COMMAND, '').strip().lower()
    if not bug_name:
        return message.channel.send('❗️Bug name not provided, usage is **{}**.'.format(BUG_USAGE))
    bug = get_by_name('bugs', bug_name, return_attributes=BUG_ATTRIBUTES, image_attribute='Icon Image')
    if not bug:
        return message.channel.send('Uh-oh, bug name "{}" cannot be found. 🐛'.format(bug_name))
    else:
        return message.channel.send(embed=build_info_embed(bug['Name'], bug['Attributes'], thumbnail=bug['Image Link']))
