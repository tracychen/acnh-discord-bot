from raymond.es.data import get_by_fields, get_by_wildcard
from raymond.constants import Commands, COMMAND_PREFIX
from raymond.info.util import build_usage_string
import discord

ART_ATTRIBUTES = [
    'Buy',
    'Sell',
    'Category',
    'Size',
    'Real Artwork Title',
    'Artist',
    'Museum Description',
    'Fake If'
]
FULL_ART_COMMAND = COMMAND_PREFIX + Commands.art.value
ART_USAGE = {
    '{} statues'.format(FULL_ART_COMMAND): 'Get list of all statues.',
    '{} paintings'.format(FULL_ART_COMMAND): 'Get list of all paintings.',
    '{} <statue name>'.format(FULL_ART_COMMAND): 'Get details on specific statue.',
    '{} <painting name>'.format(FULL_ART_COMMAND): 'Get details on specific painting.'
}


def build_art_embed(title, data, image=None):
    embed = discord.Embed(title=title.title(), colour=discord.Colour.greyple())
    embed.set_thumbnail(url=image)
    for attr in ART_ATTRIBUTES[:4]:
        embed.add_field(name=attr, value=data[attr], inline=True)
    for attr in ART_ATTRIBUTES[4:]:
        embed.add_field(name=attr, value=data[attr], inline=False)
    # embed.set_image(url='./resources/art/FtrSculptureDavidFake.png')
    return embed


def handle(message):
    args = message.content.split()
    # Show command usage
    if len(args) <= 1:
        return message.channel.send(build_usage_string(ART_USAGE))
    if len(args) >= 2:
        # List of all paintings
        if args[1] == 'paintings':
            records = get_by_wildcard('art', 'Name', 'painting', return_attributes=['Name'])
            list_of_paintings = "🎨 **LIST OF PAINTINGS** 🖼 \n"
            painting_names = set([record['Name'] for record in records])
            for painting_name in painting_names:
                list_of_paintings += '    ∙ {}\n'.format(painting_name)
            list_of_paintings += 'Try `!art <name of painting>` to learn more about each one!'
            return message.channel.send(list_of_paintings)

        # List of all statues
        elif args[1] == 'statues':
            records = get_by_wildcard('art', 'Name', 'statue', return_attributes=['Name'])
            list_of_statues = "🗿 **LIST OF STATUES** 🗽 \n"
            statue_names = set([record['Name'] for record in records])
            for statue_name in statue_names:
                list_of_statues += '    ∙ {}\n'.format(statue_name)
            list_of_statues += 'Try `!art <name of statue>` to learn more about each one!'
            return message.channel.send(list_of_statues)
    item_name = message.content.replace(FULL_ART_COMMAND, '').strip().lower()
    if not item_name:
        return message.channel.send(build_usage_string(ART_USAGE))
    fields = {
        "Name.keyword": item_name,
        "Genuine": "yes"
    }
    results = get_by_fields('art', fields, return_attributes=ART_ATTRIBUTES, image_attribute='Image')
    if not results:
        return message.channel.send('Uh-oh, art named "{}" cannot be found. 🧺'.format(item_name))
    else:
        item = results[0]
        return message.channel.send(embed=build_art_embed(item['Name'], item['Attributes'], image=item['Image Link']))
