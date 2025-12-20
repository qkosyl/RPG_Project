import pandas as pd
from sqlalchemy import create_engine, text
import items
import json

engine = create_engine("mysql+pymysql://root:kozak123@localhost:3306/rpg_database")


weapon_dict = items.weapon
swords = weapon_dict["sword"]
bows = weapon_dict["bow"]
staffs = weapon_dict["staff"]

def level_req(min_level = 1, max_level = 100, step=2):
    result = []

    for weapon_type, weapons in weapon_dict.items():
        for index, weapon in enumerate(weapons):
            level = min_level + index * step
            if level > max_level:
                break
            result.append({
                "weapon": weapon,
                "type": weapon_type,
                "level": level
            })
    return result


def assign_rarity(ItemList):
    rarity = items.Rarity
    for rarity_name, level_range in rarity.items():
        for item in ItemList:
            if level_range[0] <= item['level'] <= level_range[1]:
                item['rarity'] = rarity_name
    return ItemList

def global_calculation(items):
    for item in items:
        if item['type'] == 'sword':
            item['bonuses'] = {
                'strength': int(item['level']) * 2.75,
                'agility': int(item['level']) * 0.6,
                'intelligence': int(item['level']) * 0.15
            }
            multipliers = (4.0, 2.5, 1.05)
        elif item['type'] == 'staff':
            item['bonuses'] = {
                'strength': int(item['level']) * 0.1,
                'agility': int(item['level']) * 0.4,
                'intelligence': int(item['level']) * 3
            }
            multipliers = (1.1, 2.1213, 4.5)
        elif item['type'] == 'bow':
            item['bonuses'] = {
                'strength': int(item['level']) * 0.5,
                'agility': int(item['level']) * 2.5,
                'intelligence': int(item['level']) * 0.5
            }
            multipliers = (2.0, 3.0, 1.75)

        s = item['bonuses']['strength']
        a = item['bonuses']['agility']
        i = item['bonuses']['intelligence']

        item['attack'] = int(s * multipliers[0] + a * multipliers[1] + i * multipliers[2] + (item['level']**3.1)*0.2)
    return items

ItemList = level_req()
ItemList = assign_rarity(ItemList)
ItemList = global_calculation(ItemList)

with engine.connect() as conn:
    for item in ItemList:
        item['bonuses'] = json.dumps(item['bonuses'])
        conn.execute(
            text("insert into items(name,rarity,bonuses,attack,defense,type,level_req)"
            "VALUES(:weapon,:rarity,:bonuses,:attack,NULL,:type,:level)"),
            item
        )
    conn.commit()
    with pd.option_context('display.max_row', 0, 'display.max_columns', None):
        df = pd.read_sql(text("select * from items"), conn)
        print(df)