from raymond.constants import Commands, COMMAND_PREFIX
from raymond.info.util import build_usage_string
import discord
import re


OPEN_ARG = 'open'
NOTE_ARG = 'note'
STATUS_ARG = 'status'
CLOSE_ARG = 'close'

OPEN_STATUS = 'Open'
CLOSED_STATUS = 'Closed'

OPEN_AUDIENCES = {
    'bestfriends': 'Best Friends',
    'friends': 'Friends',
    'all': 'All'
}

NOT_APPLICABLE_STRING = 'Not applicable'

FULL_ISLAND_COMMAND = COMMAND_PREFIX + Commands.island.value
ISLAND_USAGE = {
    '{} {} <friends|bestfriends|all>'.format(FULL_ISLAND_COMMAND, OPEN_ARG): 'Mark your island as open to specified audience.',
    '{} {} <friends|bestfriends|all> dm'.format(FULL_ISLAND_COMMAND, OPEN_ARG): 'Open your island to visitors to have them dm you for dodo.',
    '{} {} <friends|bestfriends|all> <dodo code>'.format(FULL_ISLAND_COMMAND, OPEN_ARG): 'Open your island to visitors using dodo code.',
    '{} {} "message inside double quotes"'.format(FULL_ISLAND_COMMAND, NOTE_ARG): 'Add a note to your island (e.g. "Sahara has cloud floor" or "turnips sell 700").',
    '{} {}'.format(FULL_ISLAND_COMMAND, CLOSE_ARG): 'Mark your island as closed. Also clears Dodo codes and notes.',
    '{} {} <tagged discord user>'.format(FULL_ISLAND_COMMAND, STATUS_ARG): 'Show status of your island.'
    # '{} visit <tagged discord user>'.format(FULL_ISLAND_COMMAND): 'Notify another user that you would like to visit.'
}

NOTE_DEFAULT = '{}. Add a note to your island using `{} {} "message"`. This can be used for anything, for example: npc alerts or turnip prices!'.format(NOT_APPLICABLE_STRING, FULL_ISLAND_COMMAND, NOTE_ARG)

def build_island_status_embed(island_attrs, island_data, profile):
    embed = discord.Embed(colour=discord.Colour.green())
    embed.set_footer(text='💡 Remember to mark your island as closed using `{} {}`!'.format(FULL_ISLAND_COMMAND, CLOSE_ARG))
    if island_data['Status'] == CLOSED_STATUS:
        embed = discord.Embed(colour=discord.Colour.red())
        embed.set_footer(text='💡 You can mark your island as open using `{} {}`!'.format(FULL_ISLAND_COMMAND, OPEN_ARG))
    embed.set_author(name='ISLAND STATUS FOR {}'.format(profile.display_name), icon_url=profile.avatar_url)
    for display_attr, stored_attr in island_attrs.items():
        if stored_attr in island_data:
            embed.add_field(name=display_attr, value=island_data[stored_attr], inline=False)
        else:
            embed.add_field(name=display_attr, value='Not available.', inline=False)
    return embed


def handle(raymond, message):
    args = message.content.lower().split()
    if len(args) <= 1:
        return message.channel.send(build_usage_string(ISLAND_USAGE))
    member = message.author
    server_id = message.guild.id
    if args[1] == OPEN_ARG:
        if len(args) <= 2:
            return message.channel.send(build_usage_string(ISLAND_USAGE))
        if args[2] not in OPEN_AUDIENCES.keys():
            return message.channel.send('❗️Input "{}" invalid. **Valid inputs:** {}.'.format(
                args[2], ', '.join(OPEN_AUDIENCES.keys())))
        if len(args) <= 3:
            # no dodo code, mark island as open for args[2]
            body = {
                "Audience": OPEN_AUDIENCES.get(args[2]),
                "HasDodoCode": False,
                "DodoCode": NOT_APPLICABLE_STRING,
                "Status": OPEN_STATUS
            }
            raymond.set_island('{}#{}'.format(server_id, member.id), body)
            return message.channel.send('🏝 Island opened for {}. Use `{} status` to view'.format(OPEN_AUDIENCES.get(args[2]), FULL_ISLAND_COMMAND))
        if args[3] == 'dm':
            body = {
                "Audience": OPEN_AUDIENCES.get(args[2]),
                "HasDodoCode": True,
                "DodoCode": "DM for code",
                "Status": OPEN_STATUS
            }
            raymond.set_island('{}#{}'.format(server_id, member.id), body)
            return message.channel.send(
                '🏝 Island opened for {}. Use `{} status` to view'.format(OPEN_AUDIENCES.get(args[2]), FULL_ISLAND_COMMAND))
        # validate args[3] as dodo code
        # if not re.match(r'\w{5}', args[3]):
        if len(args[3]) > 7:
            return message.channel.send('❗Dodo code "{}" invalid. '.format(args[3]))
        # mark island as open for args[2] with dodo code args[3]
        body = {
            "Audience": OPEN_AUDIENCES.get(args[2]),
            "HasDodoCode": True,
            "DodoCode": args[3],
            "Status": OPEN_STATUS
        }
        result = raymond.set_island('{}#{}'.format(server_id, member.id), body)
        return message.channel.send('🏝 Island opened for {} with Dodo Code "{}". Use `{} status` to view'.format(
            OPEN_AUDIENCES.get(args[2]), args[3], FULL_ISLAND_COMMAND))

    if args[1] == STATUS_ARG:
        if len(args) == 2:
            profile = member
        elif message.mentions:
            profile = message.mentions[0]
        else:
            return message.channel.send('Uh-oh, island status for {} cannot be found. 🤯'.format(args[2]))
        result = raymond.get_island('{}#{}'.format(server_id, profile.id))
        if not result or not result['_source']['Status']:
            return message.channel.send('Uh-oh, island status for {} cannot be found. 🤯'.format(profile))
        island_data = result['_source']
        status = result['_source']['Status']
        if status == OPEN_STATUS:
            island_attrs = {
                # '🏝‍ Island': 'Island',
                '🚦‍ Status': 'Status',
                '👫 Open For': 'Audience',
                '🌎 Dodo Code': 'DodoCode',
                '💬 Note': 'Note'
            }
        else:
            island_attrs = {
                # '🏝‍ Island': 'Island',
                '🚦‍ Status': 'Status'
            }
        return message.channel.send(embed=build_island_status_embed(island_attrs, island_data, profile))

    if args[1] == NOTE_ARG:
        notes = re.findall('"([^"]*)"', message.content)
        if len(notes) != 1:
            return message.channel.send('❗️Input invalid. Usage is `{} {} "message"`. '
                                        'Make sure you use double quotes around the message!.'.format(FULL_ISLAND_COMMAND, NOTE_ARG))
        if len(notes) > 1000:
            return message.channel.send('❗️Input invalid. Note is too long. ')
        body = {
            'Note': notes[0]
        }
        raymond.set_island('{}#{}'.format(server_id, member.id), body)
        return message.channel.send('Note "{}" has been added to your island. 🤯'.format(notes[0]))
    if args[1] == CLOSE_ARG:
        body = {
            "Audience": NOT_APPLICABLE_STRING,
            "HasDodoCode": False,
            "DodoCode": NOT_APPLICABLE_STRING,
            "Status": CLOSED_STATUS,
            'Note': NOTE_DEFAULT
        }
        result = raymond.set_island('{}#{}'.format(server_id, member.id), body)
        return message.channel.send('⛔ ️You have marked your island as closed. Use `{} status` to view'.format(FULL_ISLAND_COMMAND))

    return message.channel.send(build_usage_string(ISLAND_USAGE))