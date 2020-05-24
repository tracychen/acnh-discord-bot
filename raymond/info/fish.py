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

FISH_THUMBNAIL_URL = 'https://acnhcdn.com/latest/MenuIcon/Fish79.png'


FULL_FISH_COMMAND = COMMAND_PREFIX + Commands.fish.value
FISH_USAGE = {
    '{} {}'.format(FULL_FISH_COMMAND, THISMONTH_ARG): 'Check which fish are available this month.',
    '{} {}'.format(FULL_FISH_COMMAND, NEXTMONTH_ARG): 'Check which fish are available in the next month.',
    '{} {}'.format(FULL_FISH_COMMAND, PREVMONTH_ARG): 'Check which fish are available in the previous month.',
    '{} <fish name>'.format(FULL_FISH_COMMAND): 'Get details on specific fish.',
}


def get_and_send_available_fish_message(title, month_abbr):
    nh_attr, sh_attr, value = ' '.join(['NH', month_abbr]), ' '.join(['SH', month_abbr]), 'NA'
    nh_records = get_not_matching(IndexNames.fish, nh_attr, value, return_attributes=['Name'])
    sh_records = get_not_matching(IndexNames.fish, sh_attr, value, return_attributes=['Name'])
    embed = discord.Embed(colour=discord.Colour.dark_blue())
    embed.set_author(name=title, icon_url=FISH_THUMBNAIL_URL)
    nh_names = [nh_record['Name'] for nh_record in nh_records]
    sh_names = [sh_record['Name'] for sh_record in sh_records]
    embed.add_field(name='Northern Hemisphere', value=', '.join(nh_names), inline=False)
    embed.add_field(name='Southern Hemisphere', value=', '.join(sh_names), inline=False)
    embed.set_footer(text='💡 Try `{}fish <fish name>` to learn more!'.format(COMMAND_PREFIX))
    return embed


def handle(message):
    fish_name = message.content.replace(FULL_FISH_COMMAND, '').strip().lower()
    if not fish_name:
        return message.channel.send(build_usage_string(FISH_USAGE))

    if fish_name == THISMONTH_ARG:
        curr_month = datetime.now().month
        month_abbr = calendar.month_abbr[curr_month]
        return message.channel.send(embed=get_and_send_available_fish_message('Available Fish This Month ({})'.format(
            calendar.month_name[curr_month]), month_abbr))

    if fish_name == PREVMONTH_ARG:
        curr_month = datetime.now().month
        prev_month = curr_month - 1 if curr_month > 1 else 12
        month_abbr = calendar.month_abbr[prev_month]
        return message.channel.send(embed=get_and_send_available_fish_message('Available Fish in {}'.format(
            calendar.month_name[prev_month]), month_abbr))

    if fish_name == NEXTMONTH_ARG:
        curr_month = datetime.now().month
        next_month = curr_month + 1 if curr_month < 12 else 1
        month_abbr = calendar.month_abbr[next_month]
        return message.channel.send(embed=get_and_send_available_fish_message('Available Fish in {}'.format(
            calendar.month_name[next_month]), month_abbr))

    fish = get_by_name(IndexNames.fish, fish_name, return_attributes=FISH_ATTRIBUTES, image_attribute='Icon Image')
    if not fish:
        return message.channel.send('Uh-oh, fish "{}" cannot be found. 🐡'.format(fish_name))
    else:
        return message.channel.send(embed=build_info_embed(fish['Name'], fish['Attributes'], thumbnail=fish['Image Link']))
