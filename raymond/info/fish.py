from raymond.es.data import get_by_name
from raymond.constants import Commands, COMMAND_PREFIX
from raymond.info.util import build_info_embed

FISH_ATTRIBUTES = [
    'Sell',
    'Where/How',
    'Rain/Snow Catch Up',
    'Total Catches to Unlock',
    'Northern Months',
    'Southern Months',
    'Time',
    'Shadow',
    'Lighting Type'
]

FULL_FISH_COMMAND = COMMAND_PREFIX + Commands.fish.value
FISH_USAGE = '{} <fish name>'.format(FULL_FISH_COMMAND)


def handle(message):
    fish_name = message.content.replace(FULL_FISH_COMMAND, '').strip().lower()
    if not fish_name:
        return message.channel.send('❗️Fish name not provided, usage is **{}**.'.format(FISH_USAGE))
    fish = get_by_name('fish', fish_name, return_attributes=FISH_ATTRIBUTES, image_attribute='Icon Image')
    if not fish:
        return message.channel.send('Uh-oh, fish "{}" cannot be found. 🐡'.format(fish_name))
    else:
        return message.channel.send(embed=build_info_embed(fish['Name'], fish['Attributes'], thumbnail=fish['Image Link']))
