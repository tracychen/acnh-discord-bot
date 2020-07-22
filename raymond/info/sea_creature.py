import calendar
from datetime import datetime
import discord
from raymond.es.data import get_by_name, get_not_matching
from raymond.constants import Commands, COMMAND_PREFIX, IndexNames
from raymond.info.util import build_info_embed, build_usage_string

NOW_ARG = 'now'
THISMONTH_ARG = 'thismonth'
NEXTMONTH_ARG = 'nextmonth'
PREVMONTH_ARG = 'prevmonth'

SEA_CREATURE_ATTRIBUTES = [
    'Sell',
    'Movement Speed',
    'Spawn Rates',
    'Northern Months',
    'Southern Months',
    'Time',
    'Shadow',
    'Surface',
    'Lighting Type',
    'Total Catches to Unlock'
]

SEA_CREATURE_THUMBNAIL_URL = 'https://acnhcdn.com/latest/MenuIcon/Hitode.png'


FULL_SEA_CREATURE_COMMAND = COMMAND_PREFIX + Commands.sea_creature.value
SEA_CREATURE_USAGE = {
    '{} {}'.format(FULL_SEA_CREATURE_COMMAND, THISMONTH_ARG): 'Check which sea creatures are available this month.',
    '{} {}'.format(FULL_SEA_CREATURE_COMMAND, NEXTMONTH_ARG): 'Check which sea creatures are available in the next month.',
    '{} {}'.format(FULL_SEA_CREATURE_COMMAND, PREVMONTH_ARG): 'Check which sea creatures are available in the previous month.',
    '{} <sea creature name>'.format(FULL_SEA_CREATURE_COMMAND): 'Get details on specific sea creature.',
}


def get_and_send_available_sea_creature_message(title, month_abbr):
    nh_attr, sh_attr, value = ' '.join(['NH', month_abbr]), ' '.join(['SH', month_abbr]), 'NA'
    nh_records = get_not_matching(IndexNames.sea_creatures, nh_attr, value, return_attributes=['Name'])
    sh_records = get_not_matching(IndexNames.sea_creatures, sh_attr, value, return_attributes=['Name'])
    embed = discord.Embed(colour=discord.Colour.dark_blue())
    embed.set_author(name=title, icon_url=SEA_CREATURE_THUMBNAIL_URL)
    nh_names = [nh_record['Name'] for nh_record in nh_records]
    sh_names = [sh_record['Name'] for sh_record in sh_records]
    embed.add_field(name='Northern Hemisphere', value=', '.join(nh_names), inline=False)
    embed.add_field(name='Southern Hemisphere', value=', '.join(sh_names), inline=False)
    embed.set_footer(text='💡 Try `{} <sea creature name>` to learn more!'.format(FULL_SEA_CREATURE_COMMAND))
    return embed


def handle(message):
    sea_creature_name = message.content.replace(FULL_SEA_CREATURE_COMMAND, '').strip().lower()
    if not sea_creature_name:
        return message.channel.send(build_usage_string(SEA_CREATURE_USAGE))

    if sea_creature_name == THISMONTH_ARG:
        curr_month = datetime.now().month
        month_abbr = calendar.month_abbr[curr_month]
        return message.channel.send(embed=get_and_send_available_sea_creature_message('Available Sea Creatures This Month ({})'.format(
            calendar.month_name[curr_month]), month_abbr))

    if sea_creature_name == PREVMONTH_ARG:
        curr_month = datetime.now().month
        prev_month = curr_month - 1 if curr_month > 1 else 12
        month_abbr = calendar.month_abbr[prev_month]
        return message.channel.send(embed=get_and_send_available_sea_creature_message('Available Sea Creatures in {}'.format(
            calendar.month_name[prev_month]), month_abbr))

    if sea_creature_name == NEXTMONTH_ARG:
        curr_month = datetime.now().month
        next_month = curr_month + 1 if curr_month < 12 else 1
        month_abbr = calendar.month_abbr[next_month]
        return message.channel.send(embed=get_and_send_available_sea_creature_message('Available Sea Creatures in {}'.format(
            calendar.month_name[next_month]), month_abbr))

    sea_creature = get_by_name(IndexNames.sea_creatures, sea_creature_name, return_attributes=SEA_CREATURE_ATTRIBUTES, image_attribute='Icon Image')
    if not sea_creature:
        return message.channel.send('Uh-oh, sea creature "{}" cannot be found. 🐡'.format(sea_creature_name))
    else:
        return message.channel.send(embed=build_info_embed(sea_creature['Name'], sea_creature['Attributes'], thumbnail=sea_creature['Image Link']))
