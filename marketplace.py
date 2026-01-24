# marketplace.py
from datetime import datetime
from sqlalchemy import text

def evaluate_inventory(player, items_cache):
    """
    Sprawdza inventory gracza, wybiera aktywną broń i zwraca listę itemów do zostawienia
    oraz listę itemów do wystawienia na rynku.
    """
    active_weapon = None
    player_inv = [x.strip() for x in str(player.inventory).split(",") if x.strip()]

    # Wybór najlepszej broni (zakładamy, że obiekt ma player.active_weapon)
    fit_items = []
    allowed_types = {
        "Warrior": ["sword"],
        "Mage": ["staff"],
        "Rogue": ["bow"]
    }

    for item_name in player_inv:
        item_data = items_cache[item_name]
        if player.player_class == "Adventurer":
            fit_items.append(item_data)
        else:
            if item_data['type'] in allowed_types.get(player.player_class, []) and player.level >= item_data['level_req']:
                fit_items.append(item_data)

    if fit_items:
        active_weapon = max(fit_items, key=lambda x: x['attack'])
    else:
        active_weapon = items_cache[player_inv[0]]

    active_name = active_weapon['name'].strip().lower()

    # Podział inventory na aktywną broń i resztę
    inventory_after_market = []
    items_for_market = []
    active_count = 0

    for item_name in player_inv:
        name_lower = item_name.strip().lower()
        if name_lower == active_name:
            if active_count == 0:
                inventory_after_market.append(item_name)
                active_count += 1
            else:
                items_for_market.append(item_name)
        else:
            items_for_market.append(item_name)

    # Aktualizacja inventory gracza (tylko broń, która zostaje)
    player.inventory = ",".join(inventory_after_market) if inventory_after_market else active_weapon['name']
    player.active_weapon = active_weapon

    return inventory_after_market, items_for_market


def list_items_on_market(player, items_for_market, engine, items_cache, current_date):
    """
    Wystawia podane itemy gracza na Marketplace.
    """
    if not items_for_market:
        return

    with engine.connect() as conn:
        for item_name in items_for_market:
            item_data = items_cache[item_name]
            conn.execute(
                text("""
                    INSERT INTO market_place(player_id, item_id, date_added, price, item_name, item_type, quantity)
                    VALUES(:player_id, :item_id, :date_added, :price, :item_name, :item_type, :quantity)
                """),
                {
                    "player_id": player.id,
                    "item_id": item_data["id"],
                    "date_added": current_date,
                    "price": item_data["level_req"]*100,  # przykładowa cena
                    "item_name": item_name,
                    "item_type": item_data["type"],
                    "quantity": 1
                }
            )
        conn.commit()
