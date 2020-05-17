import discord


def build_info_embed(title, data, thumbnail=None):
    embed = discord.Embed(title=title.title(), colour=discord.Colour.greyple())
    # embed.set_image(url=image)
    embed.set_thumbnail(url=thumbnail)
    for k, v in data.items():
        embed.add_field(name=k, value=v, inline=True)
    return embed


def build_usage_string(usage_map):
    usage_string = '❗Invalid argument, usage is: \n'
    for k, v in usage_map.items():
        usage_string += '    ∙ `{}`: {}\n'.format(k, v)
    return usage_string