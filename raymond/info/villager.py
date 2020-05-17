from raymond.es.data import get_by_name, get_by_fields
from raymond.constants import Commands, COMMAND_PREFIX, IndexNames
from raymond.info.util import build_info_embed, build_usage_string
from datetime import date

BIRTHDAY_ARG = 'birthday'

VILLAGER_ATTRIBUTES = [
    'Species',
    'Gender',
    'Personality',
    'Hobby',
    'Birthday',
    'Catchphrase',
    'Style 1',
    'Style 2',
    'Color 1',
    'Color 2'
]
FULL_VILLAGER_COMMAND = COMMAND_PREFIX + Commands.villager.value
VILLAGER_USAGE = {
    '{} birthday'.format(FULL_VILLAGER_COMMAND): 'Check which villagers have birthdays today (based on UTC date/time).',
    '{} <villager name>'.format(FULL_VILLAGER_COMMAND): 'Get details on specific village.r',
}


def handle(message):
    villager_arg = message.content.replace(FULL_VILLAGER_COMMAND, '').strip().lower()
    if not villager_arg:
        return message.channel.send(build_usage_string(VILLAGER_USAGE))
    if villager_arg == BIRTHDAY_ARG:
        today = date.today()
        date_string = today.strftime("%-m/%-d")
        fields = {
            "Birthday.keyword": date_string
        }
        records = get_by_fields(IndexNames.villagers, fields, return_attributes=['Name'])
        if not records:
            birthdays_message = "No villager has a birthday today ({} UTC date). 😿".format(date_string)
        else:
            birthdays_message = "**TODAY'S BIRTHDAYS** 🧁 🎊 \n Date: {} (UTC) \n Villagers: \n".format(date_string)
            villager_names = set([record['Name'] for record in records])
            for villager_name in villager_names:
                birthdays_message += '    ∙ {}\n'.format(villager_name)
            birthdays_message += 'Try `!villager <villager name>` to learn more!'
        return message.channel.send(birthdays_message)

    villager = get_by_name(IndexNames.villagers, villager_arg, return_attributes=VILLAGER_ATTRIBUTES, image_attribute='Icon Image')
    if not villager:
        return message.channel.send('Uh-oh, villager "{}" cannot be found. 😿'.format(villager_arg))
    else:
        return message.channel.send(embed=build_info_embed(villager['Name'], villager['Attributes'], thumbnail=villager['Image Link']))
