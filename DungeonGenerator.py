import pandas as pd
from sqlalchemy import create_engine, text
import useful_data
import json

engine = create_engine("mysql+pymysql://root:qwe123@localhost:3306/rpg_database")

dungeons = useful_data.Dungeons

def assign_data():
    dungeon_data = []
    for k, x in dungeons.items():
        min_level = x[0]
        max_level = x[1]
        name = k
        dungeon_data.append({
        "name": name,
        "min_level": min_level,
        "max_level": max_level
        })
    return dungeon_data
list_of_dungeons = assign_data()


with engine.connect() as conn:
    for dungeon in list_of_dungeons:
        conn.execute(
            text("insert into dungeons(name, min_level, max_level)"
                 "VALUES(:name, :min_level, :max_level)"),
            dungeon
        )
    conn.commit()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        df = pd.read_sql(text("select * from dungeons"), conn)
        print(df)

