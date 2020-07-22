from raymond.constants import Commands, COMMAND_PREFIX, NATIVE_FRUITS, NATIVE_FLOWERS, HEMISPHERES
from raymond.info.util import build_usage_string
import re

PROFILE_FIELDS = {
    # cmd :  (attr name stored, validation func, err msg)
    'friendcode': ('FriendCode', lambda x: bool(re.match(r'SW-\d{4}-\d{4}-\d{4}', x)),
                   'Friend code must follow format: "SW-XXXX-XXXX-XXXX".'),
    'island': ('Island', lambda x: len(x) < 20, 'Island name is too long.'),
    'islander': ('Islander', lambda x: len(x) < 100, 'Island name is too long.'),
    'hemisphere': ('Hemisphere', lambda x: x.lower() in HEMISPHERES,
                   '**Valid hemispheres:** {}.'.format(', '.join(HEMISPHERES))),
    'fruit': ('NativeFruit', lambda x: x.lower() in NATIVE_FRUITS,
              '**Valid fruits:** {}.'.format(', '.join(NATIVE_FRUITS))),
    'flower': ('NativeFlower', lambda x: x.lower() in NATIVE_FLOWERS,
               '**Valid flowers:** {}.'.format(', '.join(NATIVE_FLOWERS))),
}

FULL_PROFILE_COMMAND = COMMAND_PREFIX + Commands.profile.value
PROFILE_USAGE = {
    f'{FULL_PROFILE_COMMAND} update <field> <value>': 'Update your profile. Valid fields: {}.'.format(', '.join(PROFILE_FIELDS.keys())),
    f'{FULL_PROFILE_COMMAND} show': 'Show your profile details.',
    f'{FULL_PROFILE_COMMAND} show <tagged discord user>': 'Show profile of tagged discord user.',
    f'{FULL_PROFILE_COMMAND} delete': 'Delete your profile details.',
}


def handle(raymond, message):
    args = message.content.split()
    if len(args) <= 1:
        return message.channel.send(build_usage_string(PROFILE_USAGE))
    member = message.author
    server_id = message.guild.id
    print(f'Guild: {message.guild}, Server Id: {server_id}')
    if args[1] == 'update':
        if len(args) <= 2:
            return message.channel.send(build_usage_string(PROFILE_USAGE))
        if args[2] in PROFILE_FIELDS:
            if len(args) <= 3:
                return message.channel.send(f'❗️Missing input, please add value for {args[2]}')
            attr_name_validator = PROFILE_FIELDS[args[2]]
            attr_value = ' '.join(args[3:])
            if not attr_name_validator[1](attr_value):
                return message.channel.send(f'❗️Input "{attr_value}" invalid. {attr_name_validator[2]}')
            result = raymond.set_user(f'{server_id}#{member.id}', {attr_name_validator[0]: attr_value})
            return message.channel.send('Profile {}. Use `{} show` to view'.format(result, FULL_PROFILE_COMMAND))
        else:
            return message.channel.send(build_usage_string(PROFILE_USAGE))
    if args[1] == 'show':
        if len(args) == 2:
            profile = member
        elif message.mentions:
            profile = message.mentions[0]
        else:
            return message.channel.send(f'Uh-oh, profile for {args[2]} cannot be found. 🤯 '
                                        f'To view a user profile please use `{FULL_PROFILE_COMMAND} show <tagged user>`.')
        result = raymond.get_user(f'{server_id}#{profile.id}')
        if not result:
            return message.channel.send(f'Uh-oh, profile for {profile} cannot be found. 🤯')
        profile_data = result['_source']
        profile_attrs = {
            '🏝‍ Island': 'Island',
            '🙋‍ Islander': 'Islander',
            '🌎 Hemisphere': 'Hemisphere',
            '👫 Friend Code': 'FriendCode',
            '🌷 Native Flower': 'NativeFlower',
            '🍇 Native Fruit': 'NativeFruit'
        }
        message_text = '**Profile data for {}:**\n'.format(profile)
        for display_attr, stored_attr in profile_attrs.items():
            if stored_attr in profile_data:
                message_text += '**{}**: {}\n'.format(display_attr, profile_data[stored_attr])
            else:
                message_text += '**{}**: {}\n'.format(display_attr, "N/A")
        return message.channel.send(message_text)
    if args[1] == 'delete':
        result = raymond.delete_user(f'{server_id}#{member.id}')
        if not result:
            return message.channel.send(f'Uh-oh, profile for {member} cannot be found. 🤯')
        return message.channel.send(f'Profile {result["result"]}.')
