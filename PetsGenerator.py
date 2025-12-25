import pandas as pd
from sqlalchemy import create_engine, text
import useful_data
import json

engine = create_engine("mysql+pymysql://root:kozak123@localhost:3306/rpg_database")

pets = useful_data.pets

elements_bonuses = {
    "Fire": "attack_speed",
    "Water": "magic_damage",
    "Ice": "magic_crit_damage",
    "Plant": "thorns",
    "Earth": "physical_damage",
    "Electric": "crit_chance",
    "Wind": "crit_damage",
    "Shadow": ["crit_damage","crit_chance"],
    "light": ["attack_speed","physical_damage"]
}
BONUS_MULTIPLIERS = {
    "attack_speed": 0.25,
    "magic_damage": 4,
    "magic_crit_damage": 0.30,
    "thorns": 5,
    "physical_damage": 4,
    "crit_chance": 0.15,
    "crit_damage": 0.75,
}

def grant_pet_bonus():
    result = []
    for pet in pets:
        if pet["element"] in elements_bonuses.keys():
            pet["bonus"] = elements_bonuses[pet["element"]]
            result.append(pet)
    return result

def bonus_per_level():
    all_pets_with_bonuses = grant_pet_bonus()
    result = []
    for pet in all_pets_with_bonuses:
        bonuses = pet["bonus"]
        if not isinstance(bonuses, list):
            bonuses = [bonuses]

        pet["ratio"] = {}
        for bonus in bonuses:
            if bonus in BONUS_MULTIPLIERS:
                pet["ratio"][bonus] = round(BONUS_MULTIPLIERS[bonus] * pet["level"],2)
        result.append(pet)
    return result


pets = bonus_per_level()
print(pets)


with engine.connect() as conn:
    for pet in pets:
        pet["bonus"] = json.dumps(pet["bonus"])
        pet["ratio"] = json.dumps(pet["ratio"])
        conn.execute(
            text("insert into pets(name,element,level,bonus,ratio)"
                 "VALUES(:name, :element, :level, :bonus, :ratio)"),
            pet
        )
    conn.commit()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        df = pd.read_sql(text("select * from pets"), conn)

        print(df)
