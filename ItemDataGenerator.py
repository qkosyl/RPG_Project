import pandas as pd
from sqlalchemy import create_engine, text
import random
import items
#engine = create_engine("mysql+pymysql://root:kozak123@localhost:3306/rpg_database")
#id,name,rarity,bonuses,attack,defense,`type`, level_req


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



    return result


print(level_req())