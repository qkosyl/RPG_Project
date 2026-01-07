import pandas as pd
from sqlalchemy import create_engine, text
import random
import json
engine = create_engine("mysql+pymysql://root:qwe123@localhost:3306/rpg_database")

list_of_monsters = ["Goblin", "Kobold", "Ratman", "Bandit", "Thug", "Pickpocket", "Cutpurse",
                    "Footpad", "Brigand", "Outlaw", "Raider", "Marauder", "Highwayman",
                    "Scavenger", "Ruffian", "Poacher", "Smuggler", "Graverobber", "Urchin",
                    "Streetrat", "Brawler", "Enforcer", "Lookout", "Skirmisher", "Scout",
                    "Sentry", "Guard", "Mercenary", "Spearman", "Swordsman", "Axeman", "Bowman",
                    "Crossbowman", "Slingshotter", "Militiaman", "Footsoldier", "Grunt", "Orc",
                    "Orcling", "Hobgoblin", "Goblinling", "Wolfkin", "Dogman", "Lizardfolk", "Bogman",
                    "Swampkin", "Hillman", "Caveman", "Tunnelrat", "Cavecrawler", "Bonepicker", "Flesheater",
                    "Carrioner", "Ghoul", "LesserGhoul", "Feral", "Savage", "Beastman", "Goatman", "Boarman",
                    "Crowman", "Mudwalker", "Nightprowler", "Shadowlurker", "Sneak", "Stalker", "Spy",
                    "Assailant", "Backstabber", "Poisoner", "Trickster", "Hexer", "Cultist", "Acolyte",
                    "Initiate", "KiniaSwinia", "DarkFollower", "GraveServant", "BoneServant", "WarSlave",
                    "PitFighter", "ArenaFighter", "Veteran", "EliteGuard", "Champion", "Warmonger", "Warlord"]
list_of_adjective = ["Evil", "Elite", "Savage", "Feral", "Dark", "Corrupt", "Vicious", "Ruthless", "Cruel", "Bloody",
"Cursed", "Twisted", "Brutal", "Grim", "Sinister", "Malevolent", "Fiendish", "Wicked", "Vile", "Relentless"]

def level_curve(total_monsters, min_level=1, max_level=100):
    levels = []
    for index in range(total_monsters):
        if total_monsters <= 1:
            ratio = 0
        else:
            ratio = (index / (total_monsters - 1)) ** 1.2
        jump = random.randint(0,5)
        level = int(min_level + jump + ratio * (max_level - min_level))
        levels.append(level)
    return levels

def hp_curve(level, base=80, exp=1.1, bonus = 5):
    outcome = int(base * (level ** exp)) + bonus * (level ** 2.2) * random.uniform(0.80, 1)
    return int(outcome)


def exp_reward_curve(level, hp, base=0.04):
    hp_part = hp ** 1.13
    lvl_part = level * 2.07
    outcome = (hp_part * lvl_part) * base
    return int(outcome)


def gold_reward_curve(level, hp, base=0.01):
    hp_part = hp * 0.60
    lvl_part = level * 1.2
    outcome = ((hp_part * lvl_part) * base) + 1
    return int(outcome)

def attack_stat(level, hp, base=0.01):
    hp_part = hp * 0.45
    lvl_part = level * 2.2
    outcome = ((hp_part * lvl_part) * base) + 2
    return int(outcome)
def main_calculate(total_monsters):
    all_monsters = []
    levels = level_curve(total_monsters)
    for level in levels:
        hp = hp_curve(level)
        exp = exp_reward_curve(level, hp)
        gold = gold_reward_curve(level, hp)
        attack = attack_stat(level, hp)
        monster_stats = {
            "level": level,
            "hp": hp,
            "exp": exp,
            "gold": gold,
            "attack": attack
        }
        all_monsters.append(monster_stats)
    print(all_monsters)
    return all_monsters
total_monsters = 300


monsters = []
for unit in list_of_monsters:
    monsters.append(unit)
    for _ in range(3):
        adj = random.choice(list_of_adjective)
        monsters.append(f"{adj} {unit}")


statistics = main_calculate(total_monsters)
names = monsters
list_of_full_stats = []
for i in range(len(names)):
    name = names[i]
    index_stat = i % len(statistics)
    choose_index = statistics[index_stat]
    full_monster = {
        "name": name,
        "level":  choose_index["level"],
        "hp":  choose_index["hp"],
        "exp": choose_index["exp"],
        "gold": choose_index["gold"],
        "item_drop": None,
        "attack": choose_index["attack"]
    }
    list_of_full_stats.append(full_monster)
with engine.connect() as conn:
    for monster in list_of_full_stats:
        conn.execute(
            text("insert into monsters(name,level,hp_max,exp_reward,gold_reward,item_drop,attack)"
                  "VALUES(:name, :level, :hp, :exp, :gold,:item_drop, :attack)"),
            monster
        )
    conn.commit()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        df = pd.read_sql(text("select * from monsters"), conn)

        print(df)


