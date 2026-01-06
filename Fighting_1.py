# Symulacja walki Player < - > (Monster, Dungeon)

import pandas as pd
from sqlalchemy import create_engine, text
import ast

engine = create_engine("mysql+pymysql://root:qwe123@localhost:3306/rpg_database")

with engine.connect() as conn:
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        df1 = pd.read_sql(text("select level, round(avg(exp_reward)) from monsters group by level order by level"), conn)

        df_player = pd.read_sql(text("select * from players limit 10"), conn)
        df_monster = pd.read_sql(text("select * from monsters"), conn)
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
    def __init__(self, name, level, hp, hp_max, exp, inventory, defence):
        self.name = name
        self.level = level
        self.hp = hp
        self.hp_max = hp_max
        self.exp = exp
        self.inventory = inventory
        self.defence = defence

#(name,level,hp_max,exp_reward,gold_reward,item_drop,attack
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




monster_data = df_monster.iloc[0]
monster = Monster(
    name = monster_data['name'],
    level = monster_data['level'],
    hp_max = monster_data['hp_max'],
    exp_reward = monster_data['exp_reward'],
    gold_reward = monster_data['gold_reward'],
    item_drop = monster_data['item_drop'],
    attack = monster_data['attack']
)

player_data = df_player.iloc[0]
player = Player(
    name=player_data['name'],
    level=player_data['level'],
    hp=player_data['hp_current'],
    hp_max=player_data['hp_max'],
    exp=player_data['experience'],
    inventory=player_data['inventory'],
    defence=player_data['defence']
)

inventory_str = player_data['inventory']
active_item_name = inventory_str
with engine.connect() as conn:
    df_item = pd.read_sql(
        text("SELECT * FROM items WHERE name = :name"),
        conn,
        params={"name": active_item_name}
    )

item_row = df_item.iloc[0]
bonuses_dict = ast.literal_eval(item_row['bonuses'])
active_weapon = ItemWeapon(
    name=item_row['name'],
    bonuses=bonuses_dict,
    attack=item_row['attack'],
    level_req=item_row['level_req'],
    type_of_weapon = item_row['type']
)



def scalar():
    if active_weapon.type_of_weapon == 'Sword':
        damage = active_weapon.attack * int(active_weapon.bonuses["strength"]) * 2
        + active_weapon.attack * int(active_weapon.bonuses["agility"])
    elif active_weapon.type_of_weapon == 'Bow':
        damage = active_weapon.attack * int(active_weapon.bonuses["strength"])
        + active_weapon.attack * int(active_weapon.bonuses["agility"]) * 2.5
    else:
        damage = int(active_weapon.bonuses["intelligence"]) * 3.5
    return damage
def fight():
    monster.hp = monster.hp_max
    while player.hp > 0 and monster.hp_max > 0:
        player_damage = scalar()
        monster_damage = monster.attack - player.defence
        monster.hp -= player_damage
        player.hp -= max(monster_damage, 0)
        if monster.hp_max <= 0:
            player.exp += monster.exp_reward
            print(f"{player.name} zajebał {monster.name} i zakurwił na dziąsło {monster.exp_reward} exp")
        elif player.hp <= 0:
            print(f"{player.name} wyjebał sie na {monster.name}")


fight()