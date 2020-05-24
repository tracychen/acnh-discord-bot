import gspread
from oauth2client.service_account import ServiceAccountCredentials
from elasticsearch import Elasticsearch

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('ACNH Discord Bot-02b3728f3414.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('ACNH_data')
es = Elasticsearch()


def get_time_and_months(mapping):
    northern_months, southern_months = [], []
    time = 'NA'
    for k, v in mapping.items():
        if k.startswith('NH') and v != 'NA':
            northern_months.append(k.replace('NH ', '')),
            new_value = v.replace(u'\u2013', '-')
            mapping[k], time = new_value, new_value
        elif k.startswith('SH') and v != 'NA':
            southern_months.append(k.replace('SH ', ''))
            new_value = v.replace(u'\u2013', '-')
            mapping[k], time = new_value, new_value
    if len(northern_months) == 12 and len(southern_months) == 12:
        northern_months = ['All Year']
        southern_months = ['All Year']
    return ', '.join(northern_months), ', '.join(southern_months), time


def index_fish():
    sheet = spreadsheet.worksheet('Fish')
    list_of_lists = sheet.get_all_values()
    column_names = list_of_lists[0]
    for sub_list in list_of_lists[1:]:
        mapping = dict(zip(column_names, sub_list))
        northern_months, southern_months, time = get_time_and_months(mapping)
        mapping['Icon Image'] = 'https://acnhcdn.com/latest/MenuIcon/{}.png'.format(mapping['Icon Filename'])
        mapping['Critterpedia Image'] = 'https://acnhcdn.com/latest/BookFishIcon/{}.png'.format(mapping['Critterpedia Filename'])
        mapping['Furniture Image'] = 'https://acnhcdn.com/latest/FtrIcon/{}.png'.format(mapping['Furniture Filename'])
        mapping['Northern Months'] = northern_months
        mapping['Southern Months'] = southern_months
        mapping['Time'] = time
        res = es.index(index="fish", id=mapping['#'], body=mapping)
        print(res['result'])


def index_bugs():
    sheet = spreadsheet.worksheet('Bugs')
    list_of_lists = sheet.get_all_values()
    column_names = list_of_lists[0]
    for sub_list in list_of_lists[1:]:
        mapping = dict(zip(column_names, sub_list))
        northern_months, southern_months, time = get_time_and_months(mapping)
        mapping['Icon Image'] = 'https://acnhcdn.com/latest/MenuIcon/{}.png'.format(mapping['Icon Filename'])
        mapping['Critterpedia Image'] = 'https://acnhcdn.com/latest/BookInsectIcon/{}.png'.format(mapping['Critterpedia Filename'])
        mapping['Furniture Image'] = 'https://acnhcdn.com/latest/FtrIcon/{}.png'.format(mapping['Furniture Filename'])
        mapping['Northern Months'] = northern_months
        mapping['Southern Months'] = southern_months
        mapping['Time'] = time
        res = es.index(index="bugs", id=mapping['#'], body=mapping)
        print(res['result'])


def index_villagers():
    sheet = spreadsheet.worksheet('Villagers')
    list_of_lists = sheet.get_all_values()
    column_names = list_of_lists[0]
    for sub_list in list_of_lists[1:]:
        mapping = dict(zip(column_names, sub_list))
        mapping['Icon Image'] = 'https://acnhcdn.com/latest/NpcIcon/{}.png'.format(mapping['Filename'])
        res = es.index(index="villagers", id=mapping['Unique Entry ID'], body=mapping)
        print(res['result'])


def index_clothing(type=None):
    sheet_names = ['Tops', 'Bottoms', 'Headwear', 'Dress-Up', 'Accessories', 'Socks', 'Shoes', 'Bags', 'Umbrellas']
    if type and type in sheet_names:
        sheet_names = [type]
    for sheet_name in sheet_names:
        sheet = spreadsheet.worksheet(sheet_name)
        list_of_lists = sheet.get_all_values()
        column_names = list_of_lists[0]
        for sub_list in list_of_lists[1:]:
            mapping = dict(zip(column_names, sub_list))
            if sheet_name == 'Umbrellas':
                mapping['Closet Image'] = 'https://acnhcdn.com/latest/ClosetIcon/{}Cropped.png'.format(mapping['Filename'])
                mapping['Seasonal Availability'] = 'Not applicable'
                mapping['Label Themes'] = 'Not applicable'
                mapping['Style'] = 'Not applicable'
            else:
                mapping['Closet Image'] = 'https://acnhcdn.com/latest/ClosetIcon/{}.png'.format(mapping['Filename'])
            mapping['Type'] = sheet_name
            res = es.index(index="clothing", id=mapping['Unique Entry ID'], body=mapping)
            print(res['result'])


def index_fossils():
    sheet = spreadsheet.worksheet('Fossils')
    list_of_lists = sheet.get_all_values()
    column_names = list_of_lists[0]
    for sub_list in list_of_lists[1:]:
        mapping = dict(zip(column_names, sub_list))
        mapping['Image'] = 'https://acnhcdn.com/latest/FtrIcon/{}.png'.format(mapping['Filename'])
        res = es.index(index="fossils", id=mapping['Unique Entry ID'], body=mapping)
        print(res['result'])


def index_music():
    sheet = spreadsheet.worksheet('Music')
    list_of_lists = sheet.get_all_values()
    column_names = list_of_lists[0]
    for sub_list in list_of_lists[1:]:
        mapping = dict(zip(column_names, sub_list))
        mapping['Framed Image'] = 'https://acnhcdn.com/latest/FtrIcon/{}.png'.format(mapping['Filename'])
        mapping['Album Image'] = 'https://acnhcdn.com/latest/Audio/{}.png'.format(mapping['Filename'])
        res = es.index(index="music", id=mapping['Unique Entry ID'], body=mapping)
        print(res['result'])


def index_furniture(type=None):
    sheet_names = ['Housewares', 'Miscellaneous', 'Wall-mounted', 'Rugs']
    if type and type in sheet_names:
        sheet_names = [type]
    for sheet_name in sheet_names:
        sheet = spreadsheet.worksheet(sheet_name)
        list_of_lists = sheet.get_all_values()
        column_names = list_of_lists[0]
        for sub_list in list_of_lists[1:]:
            mapping = dict(zip(column_names, sub_list))
            if sheet_name == 'Rugs':
                mapping['Variation'] = 'Not applicable'
                mapping['Body Title'] = 'Not applicable'
                mapping['Pattern'] = 'Not applicable'
                mapping['Pattern Title'] = 'Not applicable'
                mapping['Pattern Customize'] = 'Not applicable'
                mapping['Body Customize'] = 'Not applicable'
                mapping['Kit Cost'] = 'Not applicable'
            mapping['Image'] = 'https://acnhcdn.com/latest/FtrIcon/{}.png'.format(mapping['Filename'])
            mapping['Type'] = sheet_name
            res = es.index(index="furniture", id=mapping['Unique Entry ID'], body=mapping)
            print(res['result'])


def index_wallpapers():
    sheet = spreadsheet.worksheet('Wallpapers')
    list_of_lists = sheet.get_all_values()
    column_names = list_of_lists[0]
    for sub_list in list_of_lists[1:]:
        mapping = dict(zip(column_names, sub_list))
        mapping['Image'] = 'https://acnhcdn.com/latest/FtrIcon/{}.png'.format(mapping['Filename'])
        res = es.index(index="wallpapers", id=mapping['Unique Entry ID'], body=mapping)
        print(res['result'])


def index_flooring():
    sheet = spreadsheet.worksheet('Floors')
    list_of_lists = sheet.get_all_values()
    column_names = list_of_lists[0]
    for sub_list in list_of_lists[1:]:
        mapping = dict(zip(column_names, sub_list))
        mapping['Image'] = 'https://acnhcdn.com/latest/FtrIcon/{}.png'.format(mapping['Filename'])
        res = es.index(index="flooring", id=mapping['Unique Entry ID'], body=mapping)
        print(res['result'])


def index_tools():
    sheet = spreadsheet.worksheet('Tools')
    list_of_lists = sheet.get_all_values()
    column_names = list_of_lists[0]
    for sub_list in list_of_lists[1:]:
        mapping = dict(zip(column_names, sub_list))
        mapping['Image'] = 'https://acnhcdn.com/latest/FtrIcon/{}.png'.format(mapping['Filename'])
        res = es.index(index="tools", id=mapping['Unique Entry ID'], body=mapping)
        print(res['result'])


def index_other():
    sheet = spreadsheet.worksheet('Other')
    list_of_lists = sheet.get_all_values()
    column_names = list_of_lists[0]
    for sub_list in list_of_lists[1:]:
        mapping = dict(zip(column_names, sub_list))
        mapping['Inventory Image'] = 'https://acnhcdn.com/latest/MenuIcon/{}.png'.format(mapping['Filename'])
        mapping['Storage Image'] = 'https://acnhcdn.com/latest/FtrIcon/{}.png'.format(mapping['Filename'])
        res = es.index(index='other', id=mapping['Unique Entry ID'], body=mapping)
        print(res['result'])

art_fake_reasons = {
    'academic painting': "There's a circular stain from a mug in the top corner.",
    'amazing painting': "The character in black is missing his hat.",
    'basic painting': "The boy will have longer hair in the back and over his forehead, instead of a more visible forehead.",
    'calm painting': "This painting is reported to always be genuine.",
    'common painting': "This painting is reported to always be genuine.",
    'detailed painting': "The hydrangeas displayed are purple in color, not blue.",
    'dynamic painting': "This painting is reported to always be genuine.",
    'famous painting': "	The character has very pronounced eyebrows.",
    'flowery painting': "This painting is reported to always be genuine.",
    'glowing painting': "This painting is reported to always be genuine.",
    'graceful painting': "The woman is almost the entire height of the portrait, and has no white tag near her hair. Or woman is looking left.",
    'jolly painting': "There is no artichoke pinned on the shirt.",
    'moody painting': "This painting is reported to always be genuine.",
    'moving painting': "There are no trees on the right side of the painting.",
    'mysterious painting': "This painting is reported to always be genuine.",
    'nice painting': "This painting is reported to always be genuine.",
    'perfect painting': "This painting is reported to always be genuine.",
    'proper painting': "This painting is reported to always be genuine.",
    'quaint painting': "There will be a lot of milk pouring from the jug instead of just a trickle.	",
    'scary painting': "The eyebrows will be arched up, making him look sad rather than arching down to make him look scary.",
    'scenic painting': "There is only one hunter instead of three, and only 12 dogs instead of 14 (2 are missing at the top of the group).",
    'serene painting': "The ermine has dark grey fur patches.",
    'sinking painting': "This painting is reported to always be genuine.",
    'solemn painting': "The character in the far doorway is raising his hand up instead of holding it to the left.",
    'twinkling painting': "This painting is reported to always be genuine.",
    'warm painting': "This painting is reported to always be genuine.",
    'wild painting left half': "The god on the left side is green, not white.",
    'wild painting right half': "The god on the right side is white, not green.",
    'wistful painting': "The pearl earring is star-shaped, not round.",
    'worthy painting': "This painting is reported to always be genuine.",
    'ancient statue': "The figure has antenna on its ears.",
    'beautiful statue': "The statue is wearing a necklace.",
    'familiar statue': "This statue is reported to always be genuine.",
    'gallant statue': "The statue is holding a book under its arm.",
    'great statue': "This statue is reported to always be genuine.",
    'informative statue': "The stone is blue when it should be black.",
    'motherly statue': "There's only one child. Or, the wolf has its tongue out.",
    'mystic statue': "The bust is wearing an earring on the right side.",
    'robust statue': "The statue is wearing a wristwatch on its disc-throwing arm.",
    'rock-head statue': "The statue head is smiling.",
    'tremendous statue': "The bronze box has a lid with handles in them middle, instead of handles only on the sides.",
    'valiant statue': "The statue’s left leg is forward, instead of right leg.",
    'warrior statue': "	The statue's hands are resting on a spade-like object"
}

def index_art():
    sheet = spreadsheet.worksheet('Art')
    list_of_lists = sheet.get_all_values()
    column_names = list_of_lists[0]
    for sub_list in list_of_lists[1:]:
        mapping = dict(zip(column_names, sub_list))
        mapping['Image'] = 'https://acnhcdn.com/latest/FtrIcon/{}.png'.format(mapping['Filename'])
        if mapping['Name'] not in art_fake_reasons:
            print(mapping['Name'] + 'not in art_fake_reasons')
        else:
            mapping['Fake If'] = art_fake_reasons.get(mapping['Name'])
        res = es.index(index="art", id=mapping['Unique Entry ID'], body=mapping)
        print(res['result'])


index_other()
#
# def index_recipes():
#     sheet = spreadsheet.worksheet('Recipes')
#     list_of_lists = sheet.get_all_values()
#     column_names = list_of_lists[0]
#     for sub_list in list_of_lists[1:]:
#         mapping = dict(zip(column_names, sub_list))
#         mapping['Icon Image'] = 'https://acnhcdn.com/latest/FtrIcon/{}.png'.format(mapping['Filename'])
#         mapping['Album Image'] = 'https://acnhcdn.com/latest/Audio/{}.png'.format(mapping['Filename'])
#         res = es.index(index="recipes", id=mapping['Unique Entry ID'], body=mapping)
#         print(res['result'])

