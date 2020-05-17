

COMMAND_PREFIX = '!'
BOT_THUMBNAIL_URL = 'https://acnhcdn.com/latest/NpcIcon/cat23.png'

class Command:
    def __init__(self, value, description):
        self.value = value
        self.description = description
        # self.children = []

    def get_description(self):
        return self.description


class Commands:
    # feature commands
    bug = Command('bug', "Get details on a specific bug")
    fish = Command('fish', "Get details on a specific fish")
    fossil = Command('fossil', "Get details on a specific fossil")
    clothing = Command('clothing', "Get details a specific clothing item (including umbrellas)")
    music = Command('music', "Get details on a specific K.K. Slider song")
    furniture = Command('furniture', "Get details a specific furniture item (including rugs)")
    flooring = Command('flooring', "Get details on a specific flooring item")
    wallpaper = Command('wallpaper', "Get details on a specific wallpaper item")
    tool = Command('tool', "Get details on a specific tool")
    art = Command('art', "Get list of paintings/statues and details for specific pieces, including how to check for fakes")
    villager = Command('villager', "Get villager information or check today's birthdays")


    # user
    profile = Command('profile', "View and edit your island profile, or view another user's profile")
    island = Command('island', "Setup island visits (in development)")

    # misc
    invite = Command('invite', "Get bot invite link")
    help = Command('help', "Get list of commands")
    about = Command('about', "Get bot development information")
    crisp = Command('crisp', "Raymond is cute")


class IndexNames:
    bugs = 'bugs'
    villagers = 'villagers'
    fish = 'fish'
    fossils = 'fossils'
    clothing = 'clothing'
    music = 'music'
    furniture = 'furniture'
    flooring = 'flooring'
    wallpapers = 'wallpapers'
    tools = 'tools'
    art = 'art'
    users = 'users'


NATIVE_FRUITS = ['apples', 'cherries', 'oranges', 'peaches', 'pears']
NATIVE_FLOWERS = ['roses', 'hyacinths', 'mums', 'cosmos', 'pansies', 'tulips', 'lilies', 'windflowers']
HEMISPHERES = ['northern', 'southern']