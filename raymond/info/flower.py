import discord
from raymond.es.data import get_by_name, get_multiple_by_name
from raymond.constants import Commands, COMMAND_PREFIX, IndexNames, FLOWER_COLORS
from raymond.info.util import build_info_embed, build_usage_string

COLOR_EMOJIS = {
    'red': '❤️',
    'yellow': '💛️',
    'white': '⚪️',
    'pink': '💞',
    'orange': '🧡',
    'blue': '💙',
    'green': '💚',
    'purple': '💜',
    'black': '⚫️',
    'gold': '⭐️'
}

HYBRID_ARG = 'hybrid'

FLOWER_ATTRIBUTES = [
    'Sell',
    'Source'
]

FLOWER_THUMBNAIL_URLS = {
    'cosmos': 'https://acnhcdn.com/latest/MenuIcon/Cosmos4.png',
    'rose': 'https://acnhcdn.com/latest/MenuIcon/Rose4.png',
    'hyacinth': 'https://acnhcdn.com/latest/MenuIcon/Hyacinth3.png',
    'mum': 'https://acnhcdn.com/latest/MenuIcon/Mum1.png',
    'pansy': 'https://acnhcdn.com/latest/MenuIcon/Pansi4.png',
    'tulip': 'https://acnhcdn.com/latest/MenuIcon/Turip6.png',
    'lily': 'https://acnhcdn.com/latest/MenuIcon/Yuri3.png',
    'windflower': 'https://acnhcdn.com/latest/MenuIcon/Anemone2.png'
}

FULL_FLOWER_COMMAND = COMMAND_PREFIX + Commands.flower.value
FLOWER_USAGE = {
    '{} <flower name> <color>'.format(FULL_FLOWER_COMMAND): 'Get details on/source of a specific flower.',
    '{} {} <flower name>'.format(FULL_FLOWER_COMMAND, HYBRID_ARG): 'Get all flower breeding pairings for a flower.'
}


def build_hybrid_embed(flower_name, records):
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.set_author(name='{} COLORS'.format(flower_name.upper()), icon_url=FLOWER_THUMBNAIL_URLS[flower_name])
    for record in records:
        color = record['Name'].split('-')[0]
        embed.add_field(name='{} {}'.format(color.upper(), flower_name.upper()), value=record['Source'], inline=False)
    embed.set_footer(text='💡 Try `{}flower <flower name> <color>` to learn more!'.format(COMMAND_PREFIX))
    return embed


def handle(message):
    args = message.content.replace(FULL_FLOWER_COMMAND, '').strip().lower()
    if not args:
        return message.channel.send(build_usage_string(FLOWER_USAGE))
    flower_args = args.split()
    if len(flower_args) < 2:
        return message.channel.send(build_usage_string(FLOWER_USAGE))

    if flower_args[0] == HYBRID_ARG:
        flower_name = flower_args[1]
        if flower_name not in FLOWER_COLORS.keys():
            return message.channel.send('❗️Input "{}" invalid. **Valid flowers:** {}.'.format(
                flower_name, ', '.join(FLOWER_COLORS.keys())))
        records = get_multiple_by_name(IndexNames.other, '{} plant'.format(flower_name), return_attributes=['Name', 'Source'])
        return message.channel.send(embed=build_hybrid_embed(flower_name, records))

    flower_name, color = flower_args[0], flower_args[1]

    if flower_name not in FLOWER_COLORS.keys():
        return message.channel.send('❗️Input "{}" invalid. **Valid flowers:** {}.'.format(
            flower_name, ', '.join(FLOWER_COLORS.keys())))
    if color not in FLOWER_COLORS[flower_name]:
        return message.channel.send('❗️Input "{}" invalid. **Valid {} colors are :** {}.'.format(
            color, flower_name, ', '.join(FLOWER_COLORS[flower_name])))

    full_plant_name = '{}-{} plant'.format(color, flower_name)

    flower = get_by_name(IndexNames.other, full_plant_name, return_attributes=FLOWER_ATTRIBUTES, image_attribute='Inventory Image')
    if not flower:
        return message.channel.send('Uh-oh, "{} {}" cannot be found. 💐'.format(color, flower_name))
    else:
        return message.channel.send(embed=build_info_embed(flower['Name'], flower['Attributes'], thumbnail=flower['Image Link']))
