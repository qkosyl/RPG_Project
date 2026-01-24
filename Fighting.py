# Symulacja walki Player < - > (Monster, Dungeon)
import time
import pandas as pd
from sqlalchemy import create_engine, text
import ast
import random
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import traceback
from datetime import timedelta, datetime
from marketplace import list_items_on_market, evaluate_inventory

engine = create_engine("mysql+pymysql://root:qwe123@localhost:3306/rpg_database")

with engine.connect() as conn:
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        df1 = pd.read_sql(text("select level, round(avg(exp_reward)) from monsters group by level order by level"), conn)

        df_player = pd.read_sql(text("select * from players"), conn)
        df_monster = pd.read_sql(text("select * from monsters"), conn)
        df_level = pd.read_sql(text("select level, avg(exp_reward) as exp_reward from monsters group by level order by level"), conn)
        df_item = pd.read_sql(text("SELECT * FROM items"), conn)
        records = df1.rename(columns={'round(avg(exp_reward))': 'exp_reward'}).set_index('level')['exp_reward'].to_dict()
        exp_needed_table = []
        i = 1
        for record, value in records.items():
            exp_needed_table.append({"level": record, "exp_needed": value*10*i})
            i += 1
        #exp_needed_table = {'level': 1, 'exp_needed': 120.0}...

#name,level,experience,gold,hp_current,hp_max,"
#"potions,dodge,strenght,intelligence,agility,defence,inventory, inventory_capacity, pet_id, guild_id
class Player:
    def __init__(self,id, name, level, hp, hp_max, exp, inventory, defence, player_class):
        self.id = id
        self.name = name
        self.level = level
        self.hp = hp
        self.hp_max = hp_max
        self.exp = exp
        self.inventory = str(inventory)
        self.defence = defence
        self.player_class = player_class
#(name,level,hp_max,exp_reward,gold_reward,item_drop,attack)
class Monster:
    def __init__(self, name, level, exp_reward, hp_max, gold_reward, item_drop, attack):
        self.name = name
        self.level = level
        self.hp_max = hp_max
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.item_drop = item_drop
        self.attack = attack
class ItemWeapon:
    def __init__(self, name, bonuses, attack, level_req, type_of_weapon):
        self.name = name
        self.bonuses = bonuses
        self.attack = attack
        self.level_req = level_req
        self.type_of_weapon = type_of_weapon
items_cache = {
    row["name"]: row
    for index, row in df_item.iterrows()
} #

def weapon_requirements(player):
    player_inv = player.inventory.split(",")
    fit_items = []
    allowed_types = {
        "Warrior": ["sword"],
        "Mage": ["staff"],
        "Rogue": ["bow"]
    }

    for item_name in player_inv:
        item_data = items_cache[item_name]
        if player.player_class == "Adventurer":
            fit_items.append(item_data)
        else:
            if item_data['type'] in allowed_types[player.player_class] and player.level >= item_data['level_req']:
                fit_items.append(item_data)
    if fit_items:
        active_weapon = max(fit_items, key=lambda x: x['attack'])

    else:
        fallback_item_name = player_inv[0]
        active_weapon = items_cache[fallback_item_name]

    player.active_weapon = active_weapon
    return active_weapon

def load_players(df_player_data):
    players_list = []
    for _ ,pdata in df_player_data.iterrows():
        player_obj = Player(
        id=pdata["id"],
        name = pdata['name'],
        level = pdata['level'],
        hp = pdata['hp_current'],
        hp_max = pdata['hp_max'],
        exp = pdata['experience'],
        inventory = str(pdata['inventory']),
        defence = pdata['defence'],
        player_class = pdata['class'])
        players_list.append(player_obj)
    return players_list

players = load_players(df_player) #moment wejscia wszystkich danych o playerach

class Leveling:
    def __init__(self, level, exp_reward):
        self.level = level
        self.exp_reward = exp_reward

level_data = Leveling(
    level=df_level['level'],
    exp_reward=df_level['exp_reward']
)

def exp_needed_by_level():
    list_of_requirements = []
    for level, monster_xp in zip(level_data.level, level_data.exp_reward):
        requirment_of_level = monster_xp * (level ** 1.5)
        pairs = {"level" : level, "requirement": requirment_of_level}
        list_of_requirements.append(pairs)
    return list_of_requirements

def scalar(player):

    weapon = player.active_weapon
    if weapon.type_of_weapon == 'sword':
        damage = (weapon.attack * int(weapon.bonuses["strength"]) * 2
        + weapon.attack * int(weapon.bonuses["agility"]))
    elif weapon.type_of_weapon == 'bow':
        damage = (weapon.attack * int(weapon.bonuses["strength"])
        + weapon.attack * int(weapon.bonuses["agility"])) * 2.5
    else:
        damage = weapon.attack * int(weapon.bonuses["intelligence"]) * 3.5
    return damage

def dropItem():
    chance = round(random.random(),3)
    return chance


def fight_single_player(player_data):
    player_data.hp = player_data.hp_max
    list_of_Items = player_data.inventory.split(",")

    weapon = weapon_requirements(player_data)

    min_level = max(player_data.level - 3, 1)
    max_level = player_data.level + 3

    eligible_monsters = df_monster[
        (df_monster['level'] >= min_level) &
        (df_monster['level'] <= max_level)
    ]

    monster_data = eligible_monsters.sample(n=1).iloc[0]
    monster_item_drop = json.loads(monster_data['item_drop'])

    monster = Monster(
        name=monster_data['name'],
        level=monster_data['level'],
        hp_max=monster_data['hp_max'],
        exp_reward=monster_data['exp_reward'],
        gold_reward=monster_data['gold_reward'],
        item_drop=monster_item_drop,
        attack=monster_data['attack']
    )


    item_row = weapon

    bonuses_dict = ast.literal_eval(item_row['bonuses'])

    player_data.active_weapon = ItemWeapon(
        name=item_row['name'],
        bonuses=bonuses_dict,
        attack=item_row['attack'],
        level_req=item_row['level_req'],
        type_of_weapon=item_row['type']
    )


    monster.hp = monster.hp_max

    while player_data.hp > 0 and monster.hp > 0:
        player_damage = scalar(player_data)
        monster_damage = max(monster.attack - player_data.defence, 0)

        monster.hp -= player_damage
        player_data.hp -= monster_damage

        if monster.hp <= 0:
            handle_win(player_data, monster, list_of_Items)
        if player_data.hp <= 0:
            break

def handle_win(player_data, monster_data, list_of_items_data):
    player_data.exp += monster_data.exp_reward

    with engine.connect() as connection:
        connection.execute(
            text("UPDATE players SET experience = :exp WHERE id = :id"),
            {"exp": player_data.exp, "id": player_data.id}
        )
        connection.commit()

    requirements = exp_needed_by_level()
    next_level = next(
        (r["requirement"] for r in requirements if r["level"] == player_data.level + 1),
        None
    )

    if next_level and player_data.exp >= next_level:
        player_data.level += 1
        with engine.connect() as connection:
            connection.execute(
                text("UPDATE players SET level = level + 1, hp_max = hp_max + 100, "
                     "strenght = strenght + CASE class "
                            "WHEN 'warrior' THEN 10 "
                            "WHEN 'mage' THEN 1 "
                            "WHEN 'rogue' THEN 5 "
                            "ELSE 5 "
                          "END, agility = agility + CASE class "
                          "WHEN 'warrior' THEN 5 "
                          "WHEN 'mage' THEN 1 "
                          "WHEN 'rogue' THEN 10 "
                          "ELSE 5 "
                        "END,intelligence = intelligence + CASE class "
                                     "WHEN 'warrior' THEN 1 "
                                     "WHEN 'mage' THEN 10 "
                                     "WHEN 'rogue' THEN 1 "
                                     "ELSE 5 "
                                  "END, hp_current = hp_max WHERE id = :id"),

                {"id": player_data.id}
            )
            connection.commit()

    chance = dropItem()
    if chance > 0.80 and monster_data.item_drop:
        item = random.choice(monster_data.item_drop)
        list_of_items_data.append(item)
        player_data.inventory = ",".join(list_of_items_data)

        with engine.connect() as connection:
            connection.execute(
                text("UPDATE players SET inventory = :inv WHERE id = :id"),
                {"inv": player_data.inventory, "id": player_data.id}
            )
            connection.commit()



def fight_all(players_data, fights_per_player=1):
    max_workers = min(32, os.cpu_count() * 2)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        for player in players_data:
            for _ in range(fights_per_player):
                # każda walka w osobnym wątku
                futures.append(executor.submit(fight_single_player, player))

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print("=== Błąd w wątku ===")
                print("Typ błędu:", type(e))
                print("Treść błędu:", e)
                print("Traceback:")
                traceback.print_exc()
                print("=====================")

vote = ""

player_data = load_players(df_player)

def time_gooner(player_data, items_cache, engine):

    current_date = datetime(year=1000, month=1, day=1)

    while True:
        try:
            vote = int(input("How many days has to be skipped? (1-50): "))
            if 1 <= vote <= 1000:
                break
            else:
                print("Podaj wartość od 1 do 1000!")
        except ValueError:
            print("Musisz wpisać liczbę całkowitą!")

    for day in range(1, vote + 1):
        print(f"\n--- Day {day} ---")
        start = time.perf_counter()
        fight_all(player_data, fights_per_player=1)
        if day % 10 == 0:
            for player in player_data:
                inventory_kept, items_for_market = evaluate_inventory(player, items_cache)

                list_items_on_market(player, items_for_market, engine, items_cache, current_date)

        current_date += timedelta(days=1)

        end = time.perf_counter()
        print(f"Day {day} finished in {end - start:.2f} seconds")



time_gooner(player_data, items_cache, engine)


