import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://root:kozak123@localhost:3306/rpg_database")



with engine.connect() as conn:
    conn.execute(
        text("insert into players(name,level,experience,gold,hp_current,hp_max,"
             "potions,dodge,strenght,intelligence,agility,defence) VALUES(:name, :level, :experience, :gold, :hp_current, :hp_max, "
             ":potions, :dodge, :strenght, :intelligence, :agility, :defence)"),
            {"name":"Krzysztof","level": 2,"experience": 1,"gold": 52,"hp_current": 100,
                "hp_max": 100, "potions": 3, "dodge": 0.10, "strenght": 4, "intelligence": 2, "agility": 5, "defence":5}
            )

    conn.commit()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        df = pd.read_sql(text("select * from players"), conn)

        print(df)
