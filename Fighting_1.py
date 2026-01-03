# Symulacja walki Player < - > (Monster, Dungeon)

import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://root:qwe123@localhost:3306/rpg_database")

with engine.connect() as conn:
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        df1 = pd.read_sql(text("select * from monsters"), conn)
        print(df1)

        df2 = pd.read_sql(text("select * from players"), conn)
        print(df2)