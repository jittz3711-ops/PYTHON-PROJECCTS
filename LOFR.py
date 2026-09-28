import random

SAVE_FILE = "savegame.txt"
FULL = 999999          

#-----------------------------------
#GAME DATA
#-----------------------------------

CLASSES = {
    "Warrior":  {"hp": 120, "mana": 30,  "attack": 12, "defense": 8, "crit": 5},
    "Mage":     {"hp": 90,  "mana": 100, "attack": 14, "defense": 3, "crit": 10},
    "Archer":   {"hp": 100, "mana": 60,  "attack": 10, "defense": 5, "crit": 20},
    "Assassin": {"hp": 80,  "mana": 50,  "attack": 13, "defense": 3, "crit": 30},
}


SKILLS = {
    "Warrior": [("Slash", 5, 1.5, 1, ""),
                ("Shield Bash", 10, 1.2, 5, "stun"),
                ("Rage", 15, 0, 10, "rage"),
                ("Earthquake", 30, 3.0, 15, "")],
    "Mage": [("Fireball", 8, 1.6, 1, ""),
             ("Ice Blast", 15, 1.8, 5, "stun"),
             ("Thunder Strike", 25, 2.5, 10, ""),
             ("Meteor", 45, 4.0, 15, "")],
    "Archer": [("Multi Shot", 8, 1.6, 1, ""),
               ("Poison Arrow", 12, 1.0, 5, "poison"),
               ("Explosive Arrow", 25, 2.5, 10, ""),
               ("Sniper Shot", 35, 3.5, 15, "")],
    "Assassin": [("Backstab", 8, 1.8, 1, ""),
                 ("Smoke Bomb", 10, 0.8, 5, "stun"),
                 ("Shadow Strike", 25, 2.8, 10, ""),
                 ("Instant Kill", 40, 0, 15, "instakill")],
}


RANKS = ["Common", "Uncommon", "Rare", "Super Rare", "Epic", "Mythical", "Legendary"]

RARE_OR_BETTER = {"Rare", "Super Rare", "Epic", "Mythical", "Legendary"}

RANK_INFO = {
    "Common":     {"mult": 1.0, "crit": 0,  "price": 50,    "drop": 50},
    "Uncommon":   {"mult": 1.1, "crit": 2,  "price": 120,   "drop": 25},
    "Rare":       {"mult": 1.3, "crit": 5,  "price": 300,   "drop": 15},
    "Super Rare": {"mult": 1.5, "crit": 8,  "price": 700,   "drop": 6},
    "Epic":       {"mult": 1.8, "crit": 12, "price": 1500,  "drop": 3},
    "Mythical":   {"mult": 2.2, "crit": 18, "price": 4000,  "drop": 0.9},
    "Legendary":  {"mult": 2.8, "crit": 25, "price": 10000, "drop": 0.1},
}

#WEAPON LIST
WEAPON_LIST = [
    ("Wooden Sword", "Common", 5, 1),
    ("Rusty Axe", "Common", 6, 1),
    ("Training Bow", "Common", 5, 1),
    ("Bronze Sword", "Uncommon", 10, 5),
    ("Hunter Bow", "Uncommon", 11, 5),
    ("Iron Dagger", "Uncommon", 10, 5),
    ("Iron Sword", "Rare", 16, 10),
    ("Steel Axe", "Rare", 18, 12),
    ("Long Bow", "Rare", 17, 12),
    ("Crystal Blade", "Super Rare", 26, 20),
    ("Shadow Dagger", "Super Rare", 27, 22),
    ("Lightning Bow", "Super Rare", 28, 25),
    ("Flame Sword", "Epic", 40, 35),
    ("Ice Spear", "Epic", 42, 38),
    ("Thunder Hammer", "Epic", 45, 40),
    ("Phoenix Blade", "Mythical", 60, 50),
    ("Demon Slayer", "Mythical", 65, 60),
    ("Celestial Staff", "Mythical", 70, 65),
    ("Dragon King's Sword", "Legendary", 90, 80),
    ("Blade of Eternity", "Legendary", 95, 90),
    ("Bow of the Gods", "Legendary", 100, 95),
]

#ARMOR LIST
ARMOR_LIST = [
    ("Cloth Tunic", "Common", 2, 10, 5, 0, 1),
    ("Leather Armor", "Common", 4, 20, 0, 1, 1),
    ("Studded Vest", "Uncommon", 8, 35, 5, 2, 5),
    ("Chainmail", "Rare", 15, 60, 10, 3, 10),
    ("Iron Plate", "Rare", 20, 80, 0, 4, 15),
    ("Crystal Armor", "Super Rare", 30, 120, 40, 6, 25),
    ("Shadow Cloak", "Super Rare", 28, 100, 30, 8, 28),
    ("Flame Plate", "Epic", 50, 200, 50, 10, 40),
    ("Frost Mail", "Epic", 55, 220, 60, 10, 45),
    ("Phoenix Armor", "Mythical", 80, 350, 100, 15, 55),
    ("Demon Guard", "Mythical", 90, 400, 80, 15, 65),
    ("Dragon Scale Armor", "Legendary", 130, 600, 150, 20, 80),
    ("Celestial Armor", "Legendary", 150, 700, 200, 25, 90),
]


WEAPONS = {}
for name, rank, base, level in WEAPON_LIST:
    WEAPONS[name] = {
        "name": name,
        "rank": rank,
        "damage": int(base * RANK_INFO[rank]["mult"]),   # rank multiplier
        "crit": RANK_INFO[rank]["crit"],                 # rank critical bonus
        "price": RANK_INFO[rank]["price"] + level * 10,
        "level": level,
    }


ARMORS = {}
for name, rank, defense, hp, mana, crit_res, level in ARMOR_LIST:
    ARMORS[name] = {
        "name": name,
        "rank": rank,
        "defense": defense,
        "hp": hp,
        "mana": mana,
        "crit_res": crit_res,
        "price": RANK_INFO[rank]["price"] + level * 10,
        "level": level,
    }

POTIONS = {
    "Small Health Potion":    {"hp": 50,   "mana": 0,    "price": 20},
    "Medium Health Potion":   {"hp": 100,  "mana": 0,    "price": 40},
    "Large Health Potion":    {"hp": 250,  "mana": 0,    "price": 100},
    "Giant Health Potion":    {"hp": 500,  "mana": 0,    "price": 250},
    "Ultimate Health Potion": {"hp": FULL, "mana": 0,    "price": 600},
    "Small Mana Potion":      {"hp": 0, "mana": 30,   "price": 20},
    "Medium Mana Potion":     {"hp": 0, "mana": 75,   "price": 45},
    "Large Mana Potion":      {"hp": 0, "mana": 150,  "price": 110},
    "Giant Mana Potion":      {"hp": 0, "mana": 300,  "price": 260},
    "Ultimate Mana Potion":   {"hp": 0, "mana": FULL, "price": 600},
    "Small Mixed Potion":     {"hp": 50,   "mana": 30,   "price": 45},
    "Large Mixed Potion":     {"hp": 250,  "mana": 150,  "price": 220},
    "Ultimate Mixed Potion":  {"hp": FULL, "mana": FULL, "price": 1200},
    "Attack Potion":   {"hp": 0, "mana": 0, "buff": "attack",  "amount": 30, "price": 60},
    "Defense Potion":  {"hp": 0, "mana": 0, "buff": "defense", "amount": 30, "price": 60},
    "Critical Potion": {"hp": 0, "mana": 0, "buff": "crit",    "amount": 20, "price": 80},
}

POTIONS_BY_PRICE = sorted(POTIONS, key=lambda n: POTIONS[n]["price"])

MATERIALS = ["Iron Ore", "Magic Crystal", "Wolf Fang", "Ancient Bone", "Dragon Scale"]
MATERIAL_PRICE = 15
 
# REGIONS
REGIONS = [
    ("Forest", ["Goblin", "Wolf", "Slime", "Zombie", "Skeleton"]),
    ("Cave", ["Orc", "Bandit", "Troll", "Dark Archer", "Giant Spider"]),
    ("Desert", ["Vampire", "Werewolf", "Necromancer", "Ice Golem", "Fire Demon"]),
    ("Ruins", ["Cursed Knight", "Stone Gargoyle", "Mummy"]),
    ("Castle", ["Dark Knight", "Royal Ghost", "Battle Mage"]),
    ("Volcano", ["Lava Beast", "Fire Drake", "Magma Golem"]),
    ("Frozen Mountain", ["Frost Wolf", "Yeti", "Ice Witch"]),
    ("Sky Temple", ["Wind Elemental", "Storm Harpy", "Sky Guardian"]),
    ("Demon Realm", ["Imp", "Hell Hound", "Demon Lord"]),
]
 
# BOSSES IN EVERY 10 LEVELS
BOSSES = ["Goblin King", "Forest Guardian", "Ancient Golem", "Vampire Lord",
          "Dragon Rider", "Demon General", "Ice Titan", "Shadow Emperor",
          "Celestial Dragon", "Ancient Demon King"]


BOSS_SKILLS = [("Dark Slash", 1.3), ("Crushing Blow", 1.6), ("Roar of Fury", 1.0)]
 

INT_KEYS = ["level", "exp", "hp", "max_hp", "mana", "max_mana", "attack", "defense",
            "gold", "crit_chance", "bosses_defeated", "enemies_defeated",
            "rare_found", "turns_played"]
LIST_KEYS = ["weapons", "armors", "weapons_collected", "quest_items"]
DICT_KEYS = ["potions", "materials"]

#--------------------------------------------------
# 2. HELPER FUNCTIONS
#-------------------------------------------------

def get_number(prompt, low, high):
    """Keep asking until the player types a whole number between low and high."""
    while True:
        try:
            value = int(input(prompt))
            if low <= value <= high:
                return value
            print(f"Please enter a number between {low} and {high}.")
        except ValueError:
            print("That is not a number. Try again.")
 
 
def make_player(name, class_name):
    """Create a new player (a dictionary) using the chosen class's stats."""
    base = CLASSES[class_name]
    return {
        "name": name,
        "class": class_name,
        "level": 1,
        "exp": 0,
        "hp": base["hp"],
        "max_hp": base["hp"],
        "mana": base["mana"],
        "max_mana": base["mana"],
        "attack": base["attack"],
        "defense": base["defense"],
        "gold": 100,
        "crit_chance": base["crit"],
        "crit_damage": 1.5,
        "weapon": "Wooden Sword",       
        "armor": None,                  
        "weapons": ["Wooden Sword"],    
        "armors": [],                   
        "potions": {"Small Health Potion": 3, "Small Mana Potion": 2},
        "materials": {},
        "quest_items": [],
        "bosses_defeated": 0,
        "enemies_defeated": 0,
        "weapons_collected": ["Wooden Sword"],
        "rare_found": 0,
        "turns_played": 0,              
        "buff": None,                   
        "defending": False,
    }
 
def weapon_stat(player, key):
    weapon = WEAPONS.get(player["weapon"])
    if weapon:
        return weapon[key]
    return 0
 
 
def armor_stat(player, key):
    armor = ARMORS.get(player["armor"])
    if armor:
        return armor[key]
    return 0
 
 
def buff_bonus(player, stat):
    """How much the current buff adds to this stat (0 if none)."""
    if player["buff"] and player["buff"][0] == stat:
        return player["buff"][1]
    return 0
 
 
def total_attack(player):
    attack = player["attack"] + weapon_stat(player, "damage")
    return attack * (100 + buff_bonus(player, "attack")) // 100
 
 
def total_defense(player):
    defense = player["defense"] + armor_stat(player, "defense")
    return defense * (100 + buff_bonus(player, "defense")) // 100
 
 
def total_max_hp(player):
    return player["max_hp"] + armor_stat(player, "hp")
 
 
def total_max_mana(player):
    return player["max_mana"] + armor_stat(player, "mana")
 
 
def total_crit(player):
    chance = player["crit_chance"] + weapon_stat(player, "crit") + buff_bonus(player, "crit")
    return min(chance, 90)
 
 
def fix_hp_mana(player):
    """HP and Mana must never be above the maximum."""
    player["hp"] = min(player["hp"], total_max_hp(player))
    player["mana"] = min(player["mana"], total_max_mana(player))
 
 
def level_cap(player):
    """Highest level allowed right now (raised by beating a boss)."""
    return min(100, 10 * (player["bosses_defeated"] + 1))
 
 
def exp_needed(level):
    return level * 30
 
 
def show_stats(player):
    print("\n========== PLAYER STATS ==========")
    print(f"Name: {player['name']}    Class: {player['class']}")
    print(f"Level: {player['level']} (cap {level_cap(player)})    "
          f"EXP: {player['exp']}/{exp_needed(player['level'])}")
    print(f"HP: {player['hp']}/{total_max_hp(player)}    "
          f"Mana: {player['mana']}/{total_max_mana(player)}")
    print(f"Attack: {total_attack(player)}    Defense: {total_defense(player)}")
    print(f"Crit Chance: {total_crit(player)}%    Crit Damage: x{player['crit_damage']}")
    print(f"Gold: {player['gold']}")
    print(f"Weapon: {player['weapon']}    Armor: {player['armor']}")
    print(f"Bosses Defeated: {player['bosses_defeated']}    "
          f"Enemies Defeated: {player['enemies_defeated']}")
    print("==================================")
 
 
# =====================================================================
# 3. INVENTORY, POTIONS AND SHOP
# =====================================================================
 
def show_inventory(player):
    print("\n---------- INVENTORY ----------")
    print("Weapons:")
    for name in player["weapons"]:
        w = WEAPONS[name]
        mark = " (equipped)" if name == player["weapon"] else ""
        print(f"  {name} [{w['rank']}] damage {w['damage']}, crit +{w['crit']}%, "
              f"needs Lv{w['level']}{mark}")
    print("Armor:")
    for name in player["armors"]:
        a = ARMORS[name]
        mark = " (equipped)" if name == player["armor"] else ""
        print(f"  {name} [{a['rank']}] defense {a['defense']}, HP +{a['hp']}, "
              f"mana +{a['mana']}, crit resist {a['crit_res']}%, needs Lv{a['level']}{mark}")
    print("Potions:")
    for name in player["potions"]:
        print(f"  {name} x{player['potions'][name]}")
    print("Materials:", player["materials"])
    print("Quest items:", player["quest_items"])
    print("-------------------------------")
 
 
def add_item(player, kind, name):
    """Add one item. kind is 'weapon', 'armor', 'potion' or 'material'."""
    if kind == "weapon":
        player["weapons"].append(name)
        if name not in player["weapons_collected"]:
            player["weapons_collected"].append(name)
        if WEAPONS[name]["rank"] in RARE_OR_BETTER:
            player["rare_found"] += 1
    elif kind == "armor":
        player["armors"].append(name)
        if ARMORS[name]["rank"] in RARE_OR_BETTER:
            player["rare_found"] += 1
    elif kind == "potion":
        player["potions"][name] = player["potions"].get(name, 0) + 1
    elif kind == "material":
        player["materials"][name] = player["materials"].get(name, 0) + 1
 
 
def remove_item(player, kind, name):
    """Remove one item."""
    if kind == "weapon":
        player["weapons"].remove(name)
    elif kind == "armor":
        player["armors"].remove(name)
    elif kind == "potion":
        player["potions"][name] -= 1
        if player["potions"][name] == 0:
            del player["potions"][name]
    elif kind == "material":
        player["materials"][name] -= 1
        if player["materials"][name] == 0:
            del player["materials"][name]
 
 
def apply_potion(player, potion_name):
    """Drink a potion: heal HP, restore mana, or start a buff."""
    potion = POTIONS[potion_name]
    print(f"You drink a {potion_name}.")
    if "buff" in potion:
        player["buff"] = [potion["buff"], potion["amount"], 3]
        print(f"Your {potion['buff']} goes up by {potion['amount']} for 3 turns!")
        return
    old_hp = player["hp"]
    old_mana = player["mana"]
    player["hp"] = min(total_max_hp(player), player["hp"] + potion["hp"])
    player["mana"] = min(total_max_mana(player), player["mana"] + potion["mana"])
    if potion["hp"] > 0:
        print(f"Restored {player['hp'] - old_hp} HP.")
    if potion["mana"] > 0:
        print(f"Restored {player['mana'] - old_mana} Mana.")
 
 
def use_potion_menu(player):
    """Choose a potion to drink. Returns True if one was used."""
    names = list(player["potions"])
    if len(names) == 0:
        print("You have no potions!")
        return False
    print("\nYour potions:")
    for i in range(len(names)):
        print(f"{i + 1}. {names[i]} x{player['potions'][names[i]]}")
    choice = get_number("Choose a potion (0 to go back): ", 0, len(names))
    if choice == 0:
        return False
    name = names[choice - 1]
    apply_potion(player, name)
    remove_item(player, "potion", name)
    return True
 
 
def item_list(player):
    """A list of (kind, name) for items that can be sold or dropped.
    The item you are wearing is left out."""
    items = []
    for name in player["weapons"]:
        if name != player["weapon"]:
            items.append(("weapon", name))
    for name in player["armors"]:
        if name != player["armor"]:
            items.append(("armor", name))
    for name in player["potions"]:
        items.append(("potion", name))
    for name in player["materials"]:
        items.append(("material", name))
    return items
 
 
def sell_price(kind, name):
    """Everything sells for half of its buy price."""
    if kind == "weapon":
        return WEAPONS[name]["price"] // 2
    if kind == "armor":
        return ARMORS[name]["price"] // 2
    if kind == "potion":
        return POTIONS[name]["price"] // 2
    return MATERIAL_PRICE
 
 
def sell_menu(player):
    items = item_list(player)
    if len(items) == 0:
        print("You have nothing to sell.")
        return
    print(f"\nYour gold: {player['gold']}")
    for i in range(len(items)):
        kind, name = items[i]
        print(f"{i + 1}. {name} ({kind}) - sells for {sell_price(kind, name)} gold")
    choice = get_number("Item to sell (0 to go back): ", 0, len(items))
    if choice == 0:
        return
    kind, name = items[choice - 1]
    price = sell_price(kind, name)
    remove_item(player, kind, name)
    player["gold"] += price
    print(f"Sold {name} for {price} gold.")
 
 
def drop_menu(player):
    items = item_list(player)
    if len(items) == 0:
        print("Nothing to drop.")
        return
    for i in range(len(items)):
        print(f"{i + 1}. {items[i][1]} ({items[i][0]})")
    choice = get_number("Item to drop (0 to go back): ", 0, len(items))
    if choice == 0:
        return
    kind, name = items[choice - 1]
    remove_item(player, kind, name)
    print(f"You dropped {name}.")
 
 
def equip_menu(player):
    options = []
    for name in player["weapons"]:
        options.append(("weapon", name))
    for name in player["armors"]:
        options.append(("armor", name))
    if len(options) == 0:
        print("You have nothing to equip.")
        return
    for i in range(len(options)):
        kind, name = options[i]
        data = WEAPONS[name] if kind == "weapon" else ARMORS[name]
        print(f"{i + 1}. {name} ({kind}, {data['rank']}) - needs Lv{data['level']}")
    choice = get_number("Item to equip (0 to go back): ", 0, len(options))
    if choice == 0:
        return
    kind, name = options[choice - 1]
    data = WEAPONS[name] if kind == "weapon" else ARMORS[name]
    if data["level"] > player["level"]:
        print(f"You need level {data['level']} to use this!")
        return
    player[kind] = name        # sets player["weapon"] or player["armor"]
    print(f"You equipped {name}.")
 
 
def unequip_menu(player):
    print("1. Unequip weapon\n2. Unequip armor\n3. Back")
    choice = get_number("Choose: ", 1, 3)
    if choice == 1:
        player["weapon"] = None
        print("Weapon removed.")
    elif choice == 2:
        player["armor"] = None
        print("Armor removed.")
    fix_hp_mana(player)
 
 
def inventory_menu(player):
    while True:
        show_inventory(player)
        print("1. Equip  2. Unequip  3. Use Potion  4. Drop  5. Sell  6. Back")
        choice = get_number("Choose: ", 1, 6)
        if choice == 1:
            equip_menu(player)
        elif choice == 2:
            unequip_menu(player)
        elif choice == 3:
            use_potion_menu(player)
        elif choice == 4:
            drop_menu(player)
        elif choice == 5:
            sell_menu(player)
        else:
            return
 
 
def buy_gear(player, table, kind):
    """Buy a weapon or armor (only items up to the player's level are shown)."""
    available = []
    for item in table.values():
        if item["level"] <= player["level"]:
            available.append(item)
    available.sort(key=lambda item: item["price"])
    print(f"\nYour gold: {player['gold']}")
    for i in range(len(available)):
        item = available[i]
        if kind == "weapon":
            stats = f"damage {item['damage']}, crit +{item['crit']}%"
        else:
            stats = f"defense {item['defense']}, HP +{item['hp']}, mana +{item['mana']}"
        print(f"{i + 1}. {item['name']} [{item['rank']}] {stats} - {item['price']} gold")
    choice = get_number("Buy which item? (0 to go back): ", 0, len(available))
    if choice == 0:
        return
    item = available[choice - 1]
    if player["gold"] < item["price"]:
        print("Not enough gold!")
        return
    player["gold"] -= item["price"]
    add_item(player, kind, item["name"])
    print(f"You bought {item['name']}!")
 
 
def buy_potions(player):
    print(f"\nYour gold: {player['gold']}")
    for i in range(len(POTIONS_BY_PRICE)):
        name = POTIONS_BY_PRICE[i]
        print(f"{i + 1}. {name} - {POTIONS[name]['price']} gold")
    choice = get_number("Buy which potion? (0 to go back): ", 0, len(POTIONS_BY_PRICE))
    if choice == 0:
        return
    name = POTIONS_BY_PRICE[choice - 1]
    if player["gold"] < POTIONS[name]["price"]:
        print("Not enough gold!")
        return
    player["gold"] -= POTIONS[name]["price"]
    add_item(player, "potion", name)
    print(f"You bought a {name}!")
 
 
def shop(player):
    while True:
        print("\n===== VILLAGE SHOP =====")
        print("1. Buy Weapons\n2. Buy Armor\n3. Buy Potions\n4. Sell Items\n5. Exit")
        choice = get_number("Choose: ", 1, 5)
        if choice == 1:
            buy_gear(player, WEAPONS, "weapon")
        elif choice == 2:
            buy_gear(player, ARMORS, "armor")
        elif choice == 3:
            buy_potions(player)
        elif choice == 4:
            sell_menu(player)
        else:
            return
 
 
# =====================================================================
# 4. BATTLE SYSTEM
# =====================================================================
 
def make_enemy(name, level, is_boss=False):
    """Enemy stats grow with the player's level. Bosses are much stronger."""
    enemy = {
        "name": name,
        "level": level,
        "max_hp": 25 + 12 * level,
        "attack": 10 + 4 * level,
        "defense": level,
        "exp": 10 + 5 * level,
        "gold": 10 + 6 * level,
        "boss": is_boss,
        "turn": 0,
        "stunned": False,
        "poison": 0,
        "heals_left": 2,
    }
    if is_boss:
        enemy["max_hp"] = enemy["max_hp"] * 3
        enemy["defense"] = enemy["defense"] + 5
        enemy["exp"] = enemy["exp"] * 5
        enemy["gold"] = enemy["gold"] * 5
    enemy["hp"] = enemy["max_hp"]
    return enemy
 
 
def calc_damage(attack, defense, crit_chance, crit_multiplier, skill_mult=1.0):
    """
    Damage = Attack - Defense (never less than 1), with a small random change.
    If it is a critical hit, damage is multiplied by the critical multiplier.
    Returns (damage, is_critical).
    """
    damage = int(attack * skill_mult) - defense
    if damage < 1:
        damage = 1
    damage = damage * random.randint(90, 110) // 100
    is_critical = random.randint(1, 100) <= crit_chance
    if is_critical:
        damage = int(damage * crit_multiplier)
    if damage < 1:
        damage = 1
    return damage, is_critical
 
 
def player_attack(player, enemy, skill_mult=1.0, attack_name="attack"):
    damage, is_critical = calc_damage(total_attack(player), enemy["defense"],
                                      total_crit(player), player["crit_damage"], skill_mult)
    if is_critical:
        print("*** CRITICAL HIT! ***")
    print(f"Your {attack_name} deals {damage} damage to {enemy['name']}!")
    enemy["hp"] -= damage
 
 
def use_skill(player, enemy):
    """Pick a skill. Returns True if a turn was used."""
    skills = []
    for skill in SKILLS[player["class"]]:
        if skill[3] <= player["level"]:          # skill[3] = unlock level
            skills.append(skill)
    print("\nYour skills:")
    for i in range(len(skills)):
        print(f"{i + 1}. {skills[i][0]} (mana {skills[i][1]})")
    choice = get_number("Choose a skill (0 to go back): ", 0, len(skills))
    if choice == 0:
        return False
    skill_name, cost, multiplier, unlock, effect = skills[choice - 1]
    if player["mana"] < cost:
        print("Not enough mana!")
        return False
    player["mana"] -= cost
    print(f"You use {skill_name}!")
 
    if effect == "instakill":
        if enemy["boss"]:
            print("The boss is immune to Instant Kill!")
        elif random.randint(1, 100) <= 3:           # very low chance
            print("A perfect strike - the enemy falls instantly!")
            enemy["hp"] = 0
        else:
            print("The attack missed...")
    elif effect == "rage":
        player["buff"] = ["attack", 50, 3]
        print("You go into a rage! Attack +50% for 3 turns.")
    else:
        player_attack(player, enemy, multiplier, skill_name)
        if effect == "stun":
            enemy["stunned"] = True
            print(f"{enemy['name']} is stunned!")
        elif effect == "poison":
            enemy["poison"] = 3
            print(f"{enemy['name']} is poisoned!")
    return True
 
 
def player_turn(player, enemy):
    """Show the action menu. Returns 'done' (turn used) or 'run' (escaped)."""
    while True:
        print("\n====================")
        print("YOUR TURN")
        print("====================")
        print("1 Attack\n2 Skills\n3 Heal\n4 Use Potion\n5 Defend\n6 Inventory\n7 View Stats\n8 Run")
        choice = get_number("Choose an action: ", 1, 8)
 
        if choice == 1:
            player_attack(player, enemy)
            return "done"
        elif choice == 2:
            if use_skill(player, enemy):
                return "done"
        elif choice == 3:
            # Heal spell: costs 15 mana, restores 25% of max HP
            if player["mana"] < 15:
                print("You need 15 mana to heal!")
            else:
                player["mana"] -= 15
                amount = total_max_hp(player) // 4
                player["hp"] = min(total_max_hp(player), player["hp"] + amount)
                print(f"You cast Heal and recover {amount} HP.")
                return "done"
        elif choice == 4:
            if use_potion_menu(player):
                return "done"
        elif choice == 5:
            player["defending"] = True
            print("You guard! The next hit does 50% less damage.")
            return "done"
        elif choice == 6:
            show_inventory(player)          # does not use a turn
        elif choice == 7:
            show_stats(player)              # does not use a turn
        elif choice == 8:
            if enemy["boss"]:
                print("You cannot run from a boss!")
            elif random.randint(1, 100) <= 50:
                print("You escaped!")
                return "run"
            else:
                print("You couldn't escape!")
                return "done"
 
 
def enemy_turn(player, enemy):
    """The enemy's turn: poison, stun, boss healing, then attack."""
    enemy["turn"] += 1
 
    if enemy["poison"] > 0:
        poison_damage = 5 + player["level"] * 2
        enemy["hp"] -= poison_damage
        enemy["poison"] -= 1
        print(f"{enemy['name']} takes {poison_damage} poison damage!")
        if enemy["hp"] <= 0:
            return
 
    if enemy["stunned"]:
        print(f"{enemy['name']} is stunned and cannot move!")
        enemy["stunned"] = False
        return
 
    # Boss healing ability (when HP is below 40%)
    if enemy["boss"] and enemy["hp"] < enemy["max_hp"] * 0.4 and enemy["heals_left"] > 0:
        if random.randint(1, 100) <= 50:
            amount = enemy["max_hp"] // 5
            enemy["hp"] = min(enemy["max_hp"], enemy["hp"] + amount)
            enemy["heals_left"] -= 1
            print(f"{enemy['name']} heals itself for {amount} HP!")
            return
 
    # Pick an attack
    multiplier = 1.0
    if enemy["boss"] and enemy["turn"] % 3 == 0:
        multiplier = 2.0
        print(f"{enemy['name']} unleashes a SPECIAL ATTACK!")
    elif enemy["boss"]:
        skill_name, multiplier = random.choice(BOSS_SKILLS)
        print(f"{enemy['name']} uses {skill_name}!")
    elif random.randint(1, 100) <= 20:
        multiplier = 1.5
        print(f"{enemy['name']} uses Power Strike!")
    else:
        print(f"{enemy['name']} attacks!")
 
    crit_chance = 15 if enemy["boss"] else 5
    crit_chance = max(0, crit_chance - armor_stat(player, "crit_res"))
    damage, is_critical = calc_damage(enemy["attack"], total_defense(player),
                                      crit_chance, 1.5, multiplier)
    if is_critical:
        print("*** The enemy landed a CRITICAL HIT! ***")
    if player["defending"]:
        damage = max(1, damage // 2)
        print("You blocked half of the damage!")
    player["hp"] -= damage
    print(f"You take {damage} damage!")
 
 
def end_of_round(player):
    """After each round: buffs run out, mana regenerates, play time counts."""
    player["turns_played"] += 1
    player["defending"] = False
    if player["buff"]:
        player["buff"][2] -= 1
        if player["buff"][2] <= 0:
            print(f"Your {player['buff'][0]} buff wore off.")
            player["buff"] = None
    player["mana"] = min(total_max_mana(player), player["mana"] + 3)
 
 
def battle(player, enemy):
    """Fight until someone dies or the player runs. Returns 'win', 'lose' or 'run'."""
    print("\n" + "=" * 40)
    if enemy["boss"]:
        print(f"BOSS BATTLE! {enemy['name']} blocks your path!")
    else:
        print(f"A wild {enemy['name']} (Lv{enemy['level']}) appears!")
    print("=" * 40)
    player["buff"] = None
    player["defending"] = False
    result = ""
 
    while result == "":
        print(f"\n{player['name']}: HP {player['hp']}/{total_max_hp(player)}  "
              f"Mana {player['mana']}/{total_max_mana(player)}")
        print(f"{enemy['name']}: HP {max(enemy['hp'], 0)}/{enemy['max_hp']}")
 
        if player_turn(player, enemy) == "run":
            result = "run"
        elif enemy["hp"] <= 0:
            result = "win"
        else:
            enemy_turn(player, enemy)
            if enemy["hp"] <= 0:
                result = "win"
            elif player["hp"] <= 0:
                result = "lose"
            else:
                end_of_round(player)
 
    player["buff"] = None
    player["defending"] = False
    return result
 
 
# ---- Leveling and loot ----
 
def check_level_up(player):
    """Level up while we have enough EXP and are below the level cap."""
    cap = level_cap(player)
    while player["level"] < cap and player["exp"] >= exp_needed(player["level"]):
        player["exp"] -= exp_needed(player["level"])
        player["level"] += 1
        player["max_hp"] += 15
        player["max_mana"] += 5
        player["attack"] += 3
        player["defense"] += 1
        player["hp"] = total_max_hp(player)
        player["mana"] = total_max_mana(player)
        print(f"\n*** LEVEL UP! You are now level {player['level']}! ***")
        print("HP +15, Mana +5, Attack +3, Defense +1")
        if player["level"] % 5 == 0:                 # every 5 levels
            player["crit_chance"] += 1
            print("Passive bonus: Critical Chance +1%!")
            for skill in SKILLS[player["class"]]:
                if skill[3] == player["level"]:
                    print(f"New skill unlocked: {skill[0]}!")
    if player["level"] == cap and cap < 100:
        print(f"(Level cap reached! Defeat the {BOSSES[player['bosses_defeated']]} to continue.)")
 
 
def roll_rank():
    """Pick a rank using the drop chances (50, 25, 15, 6, 3, 0.9, 0.1)."""
    roll = random.random() * 100
    total = 0
    for rank in RANKS:
        total += RANK_INFO[rank]["drop"]
        if roll < total:
            return rank
    return "Common"
 
 
def drop_one_item(player, rare_only=False):
    """Drop a random weapon, armor, potion or material."""
    rank = roll_rank()
    while rare_only and rank not in RARE_OR_BETTER:
        rank = roll_rank()
    kind = random.choice(["weapon", "armor", "potion", "material"])
 
    if kind == "weapon":
        pool = [n for n in WEAPONS if WEAPONS[n]["rank"] == rank]
        name = random.choice(pool) if pool else "Wooden Sword"
    elif kind == "armor":
        pool = [n for n in ARMORS if ARMORS[n]["rank"] == rank]
        name = random.choice(pool) if pool else "Cloth Tunic"
    elif kind == "potion":
        # a better rank can drop more expensive potions
        name = random.choice(POTIONS_BY_PRICE[:RANKS.index(rank) * 2 + 3])
    else:
        name = random.choice(MATERIALS)
 
    add_item(player, kind, name)
    print(f"Loot dropped: {name}")
 
 
def give_rewards(player, enemy):
    print(f"\nYou defeated {enemy['name']}!")
    print(f"+{enemy['exp']} EXP, +{enemy['gold']} gold")
    player["exp"] += enemy["exp"]
    player["gold"] += enemy["gold"]
    player["enemies_defeated"] += 1
 
    if enemy["boss"]:
        drop_one_item(player, rare_only=True)        # bosses always drop rare+
        drop_one_item(player, rare_only=True)
    elif random.randint(1, 100) <= 50:               # normal enemies: 50% chance
        drop_one_item(player)
    check_level_up(player)
 
 
# =====================================================================
# 5. GAME FLOW
# =====================================================================
 
def hunt(player):
    """Choose a region and fight monsters. Returns 'dead' or 'ok'."""
    unlocked = min(player["bosses_defeated"] + 1, len(REGIONS))
    print("\n===== WORLD MAP =====")
    for i in range(len(REGIONS)):
        lock = "" if i < unlocked else "  [LOCKED - defeat the previous boss]"
        print(f"{i + 1}. {REGIONS[i][0]}{lock}")
    print("0. Back to village")
    choice = get_number("Where do you want to go? ", 0, len(REGIONS))
    if choice == 0:
        return "ok"
    if choice > unlocked:
        print("That region is still locked!")
        return "ok"
 
    region_name, enemy_names = REGIONS[choice - 1]
    print(f"\nYou travel to the {region_name}...")
    while True:
        enemy = make_enemy(random.choice(enemy_names), player["level"])
        result = battle(player, enemy)
        if result == "win":
            give_rewards(player, enemy)
        elif result == "lose":
            return "dead"
        print("\n1. Keep fighting\n2. Return to village")
        if get_number("Choose: ", 1, 2) == 2:
            return "ok"
 
 
def fight_boss(player):
    """Returns 'dead', 'victory' or 'ok'."""
    index = player["bosses_defeated"]
    if player["level"] < level_cap(player):
        print(f"Reach level {level_cap(player)} to challenge the {BOSSES[index]}!")
        return "ok"
    print(f"\nThe {BOSSES[index]} awaits. Are you prepared?")
    print("1. Fight!\n2. Not yet")
    if get_number("Choose: ", 1, 2) == 2:
        return "ok"
 
    boss = make_enemy(BOSSES[index], 10 * (index + 1), True)
    result = battle(player, boss)
    if result == "lose":
        return "dead"
    give_rewards(player, boss)
    player["bosses_defeated"] += 1
    player["quest_items"].append(boss["name"] + " Trophy")
    if player["bosses_defeated"] == 10:
        return "victory"
    print(f"\n*** {boss['name']} is defeated! A new region is unlocked! ***")
    check_level_up(player)          # the level cap just went up
    return "ok"
 
 
def inn(player):
    cost = player["level"] * 10
    print(f"Resting costs {cost} gold (restores all HP and Mana).")
    print("1. Rest\n2. Cancel")
    if get_number("Choose: ", 1, 2) == 1:
        if player["gold"] < cost:
            print("Not enough gold!")
        else:
            player["gold"] -= cost
            player["hp"] = total_max_hp(player)
            player["mana"] = total_max_mana(player)
            print("You feel fully rested.")
 
 
# ---- Save and load (plain text file, one "key=value" line per value) ----
 
def save_game(player):
    try:
        file = open(SAVE_FILE, "w")
        for key in player:
            if key == "buff" or key == "defending":      # temporary, not saved
                continue
            value = player[key]
            if type(value) == list:                      # a,b,c
                text = ",".join(value)
            elif type(value) == dict:                    # name:count,name:count
                pairs = []
                for item_name in value:
                    pairs.append(item_name + ":" + str(value[item_name]))
                text = ",".join(pairs)
            else:
                text = str(value)
            file.write(key + "=" + text + "\n")
        file.close()
        print("Game saved!")
    except OSError:
        print("Error: could not save the game.")
 
 
def load_game():
    """Returns the loaded player, or None if the file is missing or damaged."""
    try:
        player = make_player("Unknown", "Warrior")       # default values
        file = open(SAVE_FILE, "r")
        for line in file:
            line = line.strip()
            if "=" not in line:
                continue
            key, text = line.split("=", 1)
            if key in INT_KEYS:
                player[key] = int(text)
            elif key == "crit_damage":
                player[key] = float(text)
            elif key in LIST_KEYS:
                player[key] = text.split(",") if text != "" else []
            elif key in DICT_KEYS:
                items = {}
                if text != "":
                    for pair in text.split(","):
                        item_name, count = pair.rsplit(":", 1)
                        items[item_name] = int(count)
                player[key] = items
            elif key == "weapon" or key == "armor":
                player[key] = None if text == "None" else text
            else:
                player[key] = text                       # name and class
        file.close()
 
        # Check that the save makes sense
        if player["class"] not in CLASSES:
            raise ValueError("unknown class")
        for item_name in player["weapons"]:
            if item_name not in WEAPONS:
                raise ValueError("unknown weapon")
        for item_name in player["armors"]:
            if item_name not in ARMORS:
                raise ValueError("unknown armor")
        for item_name in player["potions"]:
            if item_name not in POTIONS:
                raise ValueError("unknown potion")
        print(f"Welcome back, {player['name']}!")
        return player
    except FileNotFoundError:
        print("No save file found.")
    except (ValueError, KeyError):
        print("The save file is damaged.")
    return None
 
 
# ---- Victory screen and score ----
 
def calculate_score(player):
    return (player["level"] * 100 + player["gold"] + player["bosses_defeated"] * 500
            + player["enemies_defeated"] * 10 + len(player["weapons_collected"]) * 50
            + player["rare_found"] * 100)
 
 
def victory_screen(player):
    print("\n" + "=" * 45)
    print("   VICTORY! THE ANCIENT DEMON KING IS DEAD!")
    print("   Peace returns to the kingdom of Eldoria.")
    print("=" * 45)
    print(f"Player Name:        {player['name']} the {player['class']}")
    print(f"Final Level:        {player['level']}")
    print(f"Total Gold:         {player['gold']}")
    print(f"Bosses Defeated:    {player['bosses_defeated']}")
    print(f"Enemies Defeated:   {player['enemies_defeated']}")
    print(f"Weapons Collected:  {len(player['weapons_collected'])}")
    print(f"Rare Items Found:   {player['rare_found']}")
    print(f"Total Play Time:    {player['turns_played']} battle turns")
    print(f"Final Score:        {calculate_score(player)}")
    print("=" * 45)
 
 
# ---- Village and menus ----
 
def village(player):
    """The main hub. Returns 'quit', 'dead' or 'victory'."""
    while True:
        print("\n========== VILLAGE ==========")
        print(f"{player['name']} the {player['class']}  Lv{player['level']}  "
              f"HP {player['hp']}/{total_max_hp(player)}  Gold {player['gold']}")
        print("1. Explore (fight monsters)")
        print("2. Challenge Boss")
        print("3. Shop")
        print("4. Inventory")
        print("5. View Stats")
        print("6. Inn (rest)")
        print("7. Save Game")
        print("8. Quit to Main Menu")
        choice = get_number("Choose: ", 1, 8)
 
        if choice == 1:
            if hunt(player) == "dead":
                return "dead"
        elif choice == 2:
            result = fight_boss(player)
            if result != "ok":
                return result
        elif choice == 3:
            shop(player)
        elif choice == 4:
            inventory_menu(player)
        elif choice == 5:
            show_stats(player)
        elif choice == 6:
            inn(player)
        elif choice == 7:
            save_game(player)
        else:
            return "quit"
 
 
def play(player):
    """Run the game until the player quits, wins, or exits from Game Over."""
    while True:
        result = village(player)
        if result == "quit":
            return
        if result == "victory":
            victory_screen(player)
            return
 
        # The player died -> Game Over screen
        print("\n==================")
        print("GAME OVER")
        print("==================")
        print("1 Retry\n2 Load Save\n3 Exit")
        choice = get_number("Choose: ", 1, 3)
        if choice == 1:
            player["hp"] = total_max_hp(player)
            player["mana"] = total_max_mana(player)
            player["gold"] = player["gold"] // 2
            print("You wake up in the village and lost half of your gold.")
        elif choice == 2:
            loaded = load_game()
            if loaded:
                player = loaded
        else:
            return
 
 
def new_game():
    name = ""
    while name == "":
        name = input("Enter Player Name: ").strip()
    print("\nChoose Your Class")
    class_names = list(CLASSES)
    for i in range(len(class_names)):
        c = CLASSES[class_names[i]]
        print(f"{i + 1}. {class_names[i]}  (HP {c['hp']}, Mana {c['mana']}, "
              f"Attack {c['attack']}, Defense {c['defense']}, Crit {c['crit']}%)")
    choice = get_number("Choose: ", 1, len(class_names))
    return make_player(name, class_names[choice - 1])
 
 
def instructions():
    print("""
INSTRUCTIONS
- Pick a class, then explore regions to fight monsters and win EXP, gold and loot.
- Every 10 levels you must defeat a boss before you can level up further.
- Beating a boss unlocks the next region on the world map.
- Buy weapons, armor and potions in the shop. Sell loot for gold.
- Skills cost mana. Mana comes back a little every turn.
- Defend halves the next hit. Heal costs 15 mana.
- Save often! Reach level 100 and beat the Ancient Demon King to win.
""")
 
 
def main():
    while True:
        print("LEGENDS OF THE FORGOTTEN REALM")
        print("=" * 33)
        print("1. New Game\n2. Continue\n3. Instructions\n4. Exit")
        choice = get_number("Choose: ", 1, 4)
        if choice == 1:
            play(new_game())
        elif choice == 2:
            player = load_game()
            if player:
                play(player)
        elif choice == 3:
            instructions()
        else:
            print("Goodbye, hero!")
            return
 
 
if __name__ == "__main__":
    main()
 
