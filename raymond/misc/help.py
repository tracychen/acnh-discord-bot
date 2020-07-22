from raymond.constants import COMMAND_PREFIX, Commands
import discord

MUSEUM_COLLECTION_COMMANDS = [
        Commands.art,
        Commands.bug,
        Commands.fish,
        Commands.fossil,
        Commands.sea_creature
]

INFO_COMMANDS = [
        Commands.clothing,
        Commands.flooring,
        Commands.flower,
        Commands.furniture,
        Commands.music,
        Commands.tool,
        Commands.villager,
        Commands.wallpaper
    ]

USER_COMMANDS = [
        Commands.profile,
        Commands.island
    ]

MISC_COMMANDS = [
        Commands.about,
        Commands.changelog,
        Commands.crisp,
        Commands.help,
        Commands.invite
    ]


def build_help_embed():

    def build_field_description(commands):
        field_desc = ''
        for command in commands:
            field_desc += '  ∙  `{}{}`: {}\n'.format(COMMAND_PREFIX, command.value, command.description)
        return field_desc

    embed = discord.Embed(title='RAYMOND BOT HELP')
    embed.add_field(name='INFO COMMANDS', value=build_field_description(INFO_COMMANDS), inline=False)
    embed.add_field(name='\u200B', value='\u200B')
    embed.add_field(name='MUSEUM COLLECTION COMMANDS', value=build_field_description(MUSEUM_COLLECTION_COMMANDS), inline=False)
    embed.add_field(name='\u200B', value='\u200B')
    embed.add_field(name='USER COMMANDS', value=build_field_description(USER_COMMANDS), inline=False)
    embed.add_field(name='\u200B', value='\u200B')
    embed.add_field(name='MISC COMMANDS', value=build_field_description(MISC_COMMANDS), inline=False)
    embed.add_field(name='\u200B', value='\u200B')
    embed.set_footer(text='RAYMOND bot created by tracy#6666. Last updated 7/22/2020.', icon_url='https://acnhcdn.com/latest/NpcIcon/cat23.png')
    return embed


def handle(message):
    return message.channel.send(embed=build_help_embed())
