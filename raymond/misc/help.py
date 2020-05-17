from raymond.constants import COMMAND_PREFIX, Commands
import discord

INFO_COMMANDS = [
        Commands.art,
        Commands.bug,
        Commands.clothing,
        Commands.fish,
        Commands.flooring,
        Commands.fossil,
        Commands.furniture,
        Commands.music,
        Commands.tool,
        Commands.villager,
        Commands.wallpaper
    ]

USER_COMMANDS = [
        Commands.profile
    ]

MISC_COMMANDS = [
        Commands.about,
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
    embed.add_field(name='USER COMMANDS', value=build_field_description(USER_COMMANDS), inline=False)
    embed.add_field(name='\u200B', value='\u200B')
    embed.add_field(name='MISC COMMANDS', value=build_field_description(MISC_COMMANDS), inline=False)
    embed.add_field(name='\u200B', value='\u200B')
    embed.set_footer(text='RAYMOND bot created by tracy#9662. Last updated 5/12/2020.', icon_url='https://acnhcdn.com/latest/NpcIcon/cat23.png')
    return embed


def handle(message):
    return message.channel.send(embed=build_help_embed())
