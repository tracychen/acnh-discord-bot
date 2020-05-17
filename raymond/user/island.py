from raymond.constants import Commands, COMMAND_PREFIX
from raymond.info.util import build_usage_string
import discord

FULL_ISLAND_COMMAND = COMMAND_PREFIX + Commands.island.value
PROFILE_USAGE = {
    '{} open <dodo code>'.format(FULL_ISLAND_COMMAND): 'Update your profile. Valid fields: {}.',
    '{} close'.format(FULL_ISLAND_COMMAND): 'Mark your island as closed',
    '{} status <tagged discord user>'.format(FULL_ISLAND_COMMAND): 'Show status of your island.',
    '{} visit <npc>'.format(FULL_ISLAND_COMMAND): 'Delete your profile details.',
}