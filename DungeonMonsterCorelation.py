import pandas as pd
from sqlalchemy import create_engine, text
import useful_data
import json

engine = create_engine("mysql+pymysql://root:kozak123@localhost:3306/rpg_database")

with engine.connect() as conn:
    dungeon_monster_table = conn.execute(text("INSERT INTO dungeonmonsters (dungeon_id, monster_id, quantity, drop_rate)"
                                              " SELECT dungeon.id, monster.id, FLOOR(1 + RAND()*5), monster.level*rand()*monster.level+1 FROM dungeons AS dungeon "
                                              "JOIN monsters AS monster ON monster.level BETWEEN dungeon.min_level AND dungeon.max_level;"))
    conn.commit()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        df = pd.read_sql(text("select * from dungeonmonsters"), conn)
        print(df)
