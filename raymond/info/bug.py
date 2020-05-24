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

BUG_ATTRIBUTES = [
    'Sell',
    'Where/How',
    'Weather',
    'Total Catches to Unlock',
    'Northern Months',
    'Southern Months',
    'Time'
]

BUG_THUMBNAIL_URL = 'https://acnhcdn.com/latest/MenuIcon/Ins0.png'

FULL_BUG_COMMAND = COMMAND_PREFIX + Commands.bug.value
BUG_USAGE = {
    '{} {}'.format(FULL_BUG_COMMAND, THISMONTH_ARG): 'Check which bugs are available this month.',
    '{} {}'.format(FULL_BUG_COMMAND, NEXTMONTH_ARG): 'Check which bugs are available in the next month.',
    '{} {}'.format(FULL_BUG_COMMAND, PREVMONTH_ARG): 'Check which bugs are available in the previous month.',
    '{} <bug name>'.format(FULL_BUG_COMMAND): 'Get details on specific bug.',
}

def get_and_send_available_bugs_message(title, month_abbr):
    nh_attr, sh_attr, value = ' '.join(['NH', month_abbr]), ' '.join(['SH', month_abbr]), 'NA'
    nh_records = get_not_matching(IndexNames.bugs, nh_attr, value, return_attributes=['Name'])
    sh_records = get_not_matching(IndexNames.bugs, sh_attr, value, return_attributes=['Name'])
    embed = discord.Embed(colour=discord.Colour.dark_blue())
    embed.set_author(name=title, icon_url=BUG_THUMBNAIL_URL)
    nh_names = [nh_record['Name'] for nh_record in nh_records]
    sh_names = [sh_record['Name'] for sh_record in sh_records]
    embed.add_field(name='Northern Hemisphere', value=', '.join(nh_names), inline=False)
    embed.add_field(name='Southern Hemisphere', value=', '.join(sh_names), inline=False)
    embed.set_footer(text='💡 Try `{}bug <bug name>` to learn more!'.format(COMMAND_PREFIX))
    return embed


def handle(message):
    bug_name = message.content.replace(FULL_BUG_COMMAND, '').strip().lower()
    if not bug_name:
        return message.channel.send(build_usage_string(BUG_USAGE))

    if bug_name == THISMONTH_ARG:
        curr_month = datetime.now().month
        month_abbr = calendar.month_abbr[curr_month]
        return message.channel.send(embed=get_and_send_available_bugs_message('Available Bugs This Month ({})'.format(
            calendar.month_name[curr_month]), month_abbr))

    if bug_name == PREVMONTH_ARG:
        curr_month = datetime.now().month
        prev_month = curr_month - 1 if curr_month > 1 else 12
        month_abbr = calendar.month_abbr[prev_month]
        return message.channel.send(embed=get_and_send_available_bugs_message('Available Bugs in {}'.format(
            calendar.month_name[prev_month]), month_abbr))

    if bug_name == NEXTMONTH_ARG:
        curr_month = datetime.now().month
        next_month = curr_month + 1 if curr_month < 12 else 1
        month_abbr = calendar.month_abbr[next_month]
        return message.channel.send(embed=get_and_send_available_bugs_message('Available Bugs in {}'.format(
            calendar.month_name[next_month]), month_abbr))

    bug = get_by_name(IndexNames.bugs, bug_name, return_attributes=BUG_ATTRIBUTES, image_attribute='Icon Image')
    if not bug:
        return message.channel.send('Uh-oh, bug name "{}" cannot be found. 🐛'.format(bug_name))
    else:
        return message.channel.send(embed=build_info_embed(bug['Name'], bug['Attributes'], thumbnail=bug['Image Link']))
