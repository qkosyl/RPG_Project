# Symulacja walki Player < - > (Monster, Dungeon)

import pandas as pd
from sqlalchemy import create_engine, text

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
    def __init__(self, name, level, hp, hp_max, exp, inventory):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp_max
        self.exp = exp
        self.inventory = inventory

#(name,level,hp_max,exp_reward,gold_reward,item_drop,attack
class Monster:
    def __init__(self, name, level, exp_reward, hp_max, gold_reward, item_drop, attack):
        self.name = name
        self.level = level
        self.max_hp = hp_max
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.item_drop = item_drop
        self.attack = attack

class ItemWeapon:
    def __init__(self, name, bonuses, attack, level_req):
        self.name = name
        self.bonuses = bonuses
        self.attack = attack
        self.level_req = level_req




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
    inventory=player_data['inventory']
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
active_weapon = ItemWeapon(
    name=item_row['name'],
    bonuses=item_row['bonuses'],
    attack=item_row['attack'],
    level_req=item_row['level_req']
)


print(str(player.inventory))