import pandas as pd
from sqlalchemy import create_engine, text
import json

engine = create_engine("mysql+pymysql://root:qwe123@localhost:3306/rpg_database")
with engine.connect() as conn:
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
       list_of_loot_monster  = pd.read_sql(text("select * from monsters"), conn)
       list_of_items = pd.read_sql(text("select name, level_req from items"), conn)
    new_column_drop = {}

    dicts_of_monsters = list_of_loot_monster.to_dict(orient="records")
    dicts_of_items = list_of_items.to_dict(orient="records")
    new_monster_list = []
    for monster in dicts_of_monsters:
        drop_items = set()
        for item in dicts_of_items:
            if monster["level"] == item["level_req"]:
                drop_items.add(item["name"])
        monster["item_drop"] = list(drop_items)
        new_monster_list.append(monster)

    new_df = pd.DataFrame(new_monster_list)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(new_df)

    with engine.begin() as conn:
        for _, row in new_df.iterrows():
            monster_row = {"drop": json.dumps(row['item_drop'], ensure_ascii=False),
                           "id": row['id'] }
            conn.execute(
                text("update monsters "
                     "set item_drop = :drop "
                     "where id = :id"), monster_row
            )
