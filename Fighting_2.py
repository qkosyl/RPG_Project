# Symulacja walki Player < - > (Monster, Dungeon)

import pandas as pd
from sqlalchemy import create_engine, text
import ast
import random
import json

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
    def __init__(self,id, name, level, hp, hp_max, exp, inventory, defence):
        self.id = id
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

players = []
for _ ,pdata in df_player.iterrows():
    player_obj = Player(
    id=pdata["id"],
    name = pdata['name'],
    level = pdata['level'],
    hp = pdata['hp_current'],
    hp_max = pdata['hp_max'],
    exp = pdata['experience'],
    inventory = pdata['inventory'],
    defence = pdata['defence'])
    players.append(player_obj)

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
        requirment_of_level = monster_xp * level * level * 2
        pairs = {"level" : level, "requirement": requirment_of_level}
        list_of_requirements.append(pairs)
    print(list_of_requirements)
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
        damage = int(weapon.bonuses["intelligence"]) * 3.5
    return damage



def dropItem():
    chance = round(random.random(),3)
    return chance




def fight_all(players):

    for player in players:
        List_of_Items = player.inventory.split(",")
        min_level = max(player.level - 3, 1)
        max_level = player.level + 3
        eligible_monsters = df_monster[(df_monster['level'] >= min_level) & (df_monster['level'] <= max_level)]
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


        player_invetory = player.inventory.split(",")
        active_item_name = player_invetory[0]

        with engine.connect() as conn:
            df_item = pd.read_sql(
                text("SELECT * FROM items WHERE name = :name"),
                conn,
                params={"name": active_item_name}
            )

        if not df_item.empty:
            item_row = df_item.iloc[0]
            bonuses_dict = ast.literal_eval(item_row['bonuses'])
            player.active_weapon = ItemWeapon(
                name=item_row['name'],
                bonuses=bonuses_dict,
                attack=item_row['attack'],
                level_req=item_row['level_req'],
                type_of_weapon=item_row['type']
            )
        else:
            raise ValueError(f"Item '{active_item_name}' nie istnieje w bazie danych")

        monster.hp = monster.hp_max
        while player.hp > 0 and monster.hp_max > 0:
            player_damage = scalar(player)
            monster_damage = monster.attack - player.defence
            monster.hp -= player_damage
            print(f"Gracz{player.name} zakurwił {player_damage} frajerowi {monster.name} i zostało mu {monster.hp}hp")
            player.hp -= max(monster_damage, 0)
            print(f"Monster {monster.name} zajebał lepe {player.name} i zostało mu {player.hp} hp")
            if monster.hp <= 0:
                player.exp += monster.exp_reward
                print(f"{player.name} zajebał {monster.name} i zakurwił na dziąsło {monster.exp_reward} exp")
                new_exp = player.exp
                with engine.connect() as conn:
                    conn.execute(
                        text("UPDATE players SET experience = :new_exp WHERE id = :player_id"),
                        {"new_exp": new_exp, "player_id": player.id}
                    )
                    conn.commit()
                requirements = exp_needed_by_level()
                next_level_req_list = [r["requirement"] for r in requirements if r["level"] == player.level + 1]
                if next_level_req_list:
                    next_level_req = next_level_req_list[0]
                    if player.exp >= next_level_req:
                        player.level += 1
                        print(f"{player.name} awansował na level {player.level}!")
                        with engine.connect() as conn:
                            conn.execute(
                                text("UPDATE players SET level = level + 1 WHERE id = :player_id"),
                                {"player_id": player.id}
                            )
                            conn.commit()
                            pass
                chance = dropItem()
                item = random.choice(monster.item_drop) if monster.item_drop else None
                if chance > 0.40 and item is not None:
                    List_of_Items.append(item)
                    player.inventory = ",".join(List_of_Items)
                    print(player.inventory)
                    with engine.connect() as conn:
                        conn.execute(
                            text("UPDATE players SET inventory = :inventory WHERE id = :player_id"),
                            {"inventory": player.inventory,"player_id": player.id}
                        )
                        conn.commit()
                        pass
                    print(f"{player.name} zajebał jak żyd: {item} i spierdala na chate świętować")
                else:
                    print("ale chuja dostał")

                break
            elif player.hp <= 0:
                print(f"{player.name} wyjebał sie na {monster.name} jebany debil")
                print(f"{monster.name} zostało {monster.hp} hp")
                break

fight_all(players)