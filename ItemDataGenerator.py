from email.errors import InvalidMultipartContentTransferEncodingDefect

import pandas as pd
from sqlalchemy import create_engine, text
import random
import items

#engine = create_engine("mysql+pymysql://root:kozak123@localhost:3306/rpg_database")


dict = items.weapon
swords = dict["sword"]
bows = dict["bow"]
staffs = dict["staff"]

def level_req(min_level = 1, max_level = 100, step=2):
    result = []

    for weapon_type, weapons in dict.items():
        for index, weapon in enumerate(weapons):
            level = min_level + index * step
            if level > max_level:
                break
            result.append({
                "weapon": weapon,
                "type": weapon_type,
                "level": level
            })
    print(result)
    return result


def assign_rarity(ItemList):
    rarity = items.Rarity
    for rarity_name, level_range in rarity.items():
        for item in ItemList:
            if level_range[0] <= item['level'] <= level_range[1]:
                item['rarity'] = rarity_name
    print(ItemList)
    return ItemList

def global_calculation(items):
    result = []
    for item in items:
        if item['type'] == 'sword':
            item['bonuses'] = {
            'strength': int(item['level'])*2.75,
            'agility': int(item['level'])*0.6,
            'intelligence': int(item['level'])*0.15
            } # 3.5
        if item['type'] == 'staff':
            item['bonuses'] = {
            'strength': int(item['level'])*0.1,
            'agility': int(item['level'])*0.4,
            'intelligence': int(item['level'])*3
            } # 3.5
        if item['type'] == 'bow':
            item['bonuses'] = {
                'strength': int(item['level']) * 0.5,
                'agility': int(item['level']) * 2.5,
                'intelligence': int(item['level']) * 0.5
            } # 3.5
        pass
    for item in items:
        strength = item['bonuses']['strength']
        agility = item['bonuses']['agility']
        intelligence = item['bonuses']['intelligence']
        if item['type'] == 'sword':
            item['attack'] = int((strength * 4.0) + (agility * 2.5) + (intelligence * 1.05))
        if item['type'] == 'staff':
            item['attack'] = int((strength * 1.1) + (agility * 2.1213) + (intelligence * 4.5))
        if item['type'] == 'bow':
            item['attack'] = int((strength * 2.0) + (agility * 3.0) + (intelligence * 1.75))
    return ItemList


ItemList = level_req()
ItemList = assign_rarity(ItemList)
ItemList = global_calculation(ItemList)
print(ItemList)
