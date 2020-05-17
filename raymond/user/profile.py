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
    '{} update <field> <value>'.format(FULL_PROFILE_COMMAND): 'Update your profile. Valid fields: {}.'.format(', '.join(PROFILE_FIELDS.keys())),
    '{} show'.format(FULL_PROFILE_COMMAND): 'Show your profile details.',
    '{} show <tagged discord user>'.format(FULL_PROFILE_COMMAND): 'Show profile of tagged discord user.',
    '{} delete'.format(FULL_PROFILE_COMMAND): 'Delete your profile details.',
}


def handle(raymond, message):
    args = message.content.split()
    if len(args) <= 1:
        return message.channel.send(build_usage_string(PROFILE_USAGE))
    member = message.author
    if args[1] == 'update':
        if len(args) <= 2:
            return message.channel.send(build_usage_string(PROFILE_USAGE))
        if args[2] in PROFILE_FIELDS:
            if len(args) <= 3:
                return message.channel.send('❗️Missing input, please add value for {}'.format(args[2]))
            attr_name_validator = PROFILE_FIELDS[args[2]]
            attr_value = ' '.join(args[3:])
            if not attr_name_validator[1](attr_value):
                return message.channel.send('❗️Input "{}" invalid. {}'.format(attr_value, attr_name_validator[2]))
            result = raymond.set_user(member.id, {attr_name_validator[0]: attr_value})
            return message.channel.send('Profile {}. Use `{} show` to view'.format(result, FULL_PROFILE_COMMAND))
        else:
            return message.channel.send(build_usage_string(PROFILE_USAGE))
    if args[1] == 'show':
        if len(args) == 2:
            profile = member
        elif message.mentions:
            profile = message.mentions[0]
        else:
            return message.channel.send('Uh-oh, profile for {} cannot be found. 🤯'.format(args[2]))
        result = raymond.get_user(profile.id)
        if not result:
            return message.channel.send('Uh-oh, profile for {} cannot be found. 🤯'.format(profile))
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
        result = raymond.delete_user(member.id)
        if not result:
            return message.channel.send('Uh-oh, profile for {} cannot be found. 🤯'.format(member))
        return message.channel.send('Profile {}.'.format(result['result']))
