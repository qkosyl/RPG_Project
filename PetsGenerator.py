import pandas as pd
from sqlalchemy import create_engine, text
import useful_data
import json

#engine = create_engine("mysql+pymysql://root:kozak123@localhost:3306/rpg_database")

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

def grant_pet_bonus():
    result = []
    for pet in pets:
        if pet["element"] in elements_bonuses.keys():
            pet["bonus"] = elements_bonuses[pet["element"]]
            result.append(pet)
        else:
            0
    print(result)
    return result

grant_pet_bonus()

def bonus_per_level():
    all_pets_with_bonuses = grant_pet_bonus()
    result = []
    for pet in all_pets_with_bonuses:
        if pet["bonus"] == 'attack_speed':
           pet["ratio"] = int(pet["level"]*0.35)
           result.append(pet)