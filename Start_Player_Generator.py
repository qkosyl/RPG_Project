import pandas as pd
from kiwisolver import strength
from sqlalchemy import create_engine, text
import random
import json
import useful_data
engine = create_engine("mysql+pymysql://root:qwe123@localhost:3306/rpg_database")

rpg_names = [
    "Aranthor", "Lyriana", "Kaelith", "Draven", "Seraphine", "Thalorin", "Elowen", "Fenric", "Isolde", "Galadric",
    "Nymeria", "Dorian", "Zephyra", "Orin", "Selene", "Braxen", "Valeria", "Kaelen", "Morrigan", "Thorne",
    "Elysia", "Roderic", "Lunara", "Kaidan", "Sylvara", "Daeron", "Virell", "Arwen", "Calder", "Lysandra",
    "Fenrir", "Elara", "Toren", "Mirabel", "Kael", "Vespera", "Orlan", "Nyssa", "Raelan", "Selwyn",
    "Thalindra", "Drystan", "Amara", "Vaelin", "Isara", "Ronan", "Serilda", "Zephyr", "Alaric", "Elaria",
    "Kaedric", "Virelia", "Damaris", "Thorian", "Liora", "Corvin", "Nyxara", "Galen", "Selara", "Varric",
    "Aric", "Lyselle", "Fenwyn", "Elion", "Morwen", "Kaelis", "Vaelith", "Darion", "Sylith", "Toriel",
    "Raelith", "Althar", "Eryndor", "Lirien", "Dravenor", "Selindra", "Veyron", "Amaris", "Kaelor", "Thalorin",
    "Isilwen", "Corwyn", "Lyric", "Galadriel", "Nythera", "Vaelora", "Ronith", "Ardyn", "Sylvara", "Doreth",
    "Eloweth", "Thalric", "Isalyn", "Varric", "Lysanor", "Fenlith", "Mirith", "Kaedara", "Arion", "Selwynna"
]

weapon_dict = useful_data.weapon
start_sword = weapon_dict["sword"][0]
start_bow = weapon_dict["bow"][0]
start_staff = weapon_dict["staff"][0]



with engine.connect() as conn:
    for _ in range(1000):
        name = random.choice(rpg_names)
        strength = random.randint(1, 10)
        agility = random.randint(1, 10)
        intelligence = random.randint(1, 10)

        if intelligence > agility and intelligence > strength:
            inventory_item = start_staff
        elif agility > intelligence and agility > strength:
            inventory_item = start_bow
        else:
            inventory_item = start_sword

        player = {
            "name": name, "level": random.randint(1, 5), "experience": random.randint(1, 5),
            "gold": random.randint(30, 300), "hp_current": 100,
            "hp_max": 100, "potions": 3, "dodge": (random.randint(0, 10) / 9), "strenght": strength,
            "intelligence": intelligence, "agility": agility, "defence": random.randint(1, 25),
            "inventory": inventory_item, "inventory_capacity": 10, "pet_id": random.randint(1,9), "guild_id": random.randint(1,5)
                  }



        conn.execute(
            text("insert into players(name,level,experience,gold,hp_current,hp_max,"
                 "potions,dodge,strenght,intelligence,agility,defence,inventory, inventory_capacity, pet_id, guild_id) VALUES(:name, :level, :experience, :gold, :hp_current, :hp_max, "
                 ":potions, :dodge, :strenght, :intelligence, :agility, :defence, :inventory, :inventory_capacity, :pet_id, :guild_id)"),
                player
            )

    conn.commit()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        df = pd.read_sql(text("select * from players"), conn)

        print(df)
