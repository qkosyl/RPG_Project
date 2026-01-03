import pandas as pd
from sqlalchemy import create_engine, text
import useful_data
import random

engine = create_engine("mysql+pymysql://root:qwe123@localhost:3306/rpg_database")

with engine.connect() as conn:
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        player_counter = pd.read_sql(text("select count(*) from players"), conn).iloc[0,0]

players_free = int(player_counter)
guilds = useful_data.guilds
guild_data = []

for guild in guilds:
    if players_free < 10:
        break
    guild_amount_of_players = random.randint(10,45)
    guild_data.append({
    "guild_name": guild,
    "guild_level": random.randint(1,3),
    "experience": random.randint(1,200),
    "members": guild_amount_of_players,
    "treasury": 0
    })
    players_free -= guild_amount_of_players
with engine.connect() as conn:
    for guild in guild_data:
        conn.execute(
            text("insert into guilds(guild_name,guild_level,experience,members,treasury)"
                 "VALUES(:guild_name, :guild_level, :experience, :members,:treasury)"),
            guild
        )
    conn.commit()