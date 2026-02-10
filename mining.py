import random
import time
import os

# ---------- DATA ----------
merchant_cooldown = 0
MERCHANT_COOLDOWN_DAYS = 3
merchant_qty_range = (1, 4)

enemies = {
    "Zombie":   {"power": 1.0, "lose": 25},
    "Skeleton": {"power": 2.0, "lose": 50},
    "Spider":   {"power": 0.7, "lose": 15},
    "Creeper":  {"power": 3.0, "lose": 100},
    "Wither":   {"power": 4.0, "lose": 0},
    "Boss":     {"power": 6.0, "lose": 0},
}

ores = {
    "Coal": 10,
    "Iron": 25,
    "Crystal": 50,
    "Emerald": 75,
    "Diamond": 100,
}

upgrade_cost = {
    "power": 100,
    "defense": 120,
    "speed": 80,
}

events = [
    "Mining...",
    "Digging straight...",
    "Break time...",
    "Going deeper...",
    "Almost there...",
    "I miss the sky...",
    "Spookyy...",
    "Mining nikel...",
    "one more block...",
    "This ore looks shiny...",
    "Im feeling lucky today...",
    "Did i see diamond?",
    "Give me 500 diamond pls...",
]

player = {
    "day": 1,
    "money": 100,
    "inventory": {},
    "power": 1,
    "defense": 1,
    "speed": 1,
    "bonus_speed": 0,
    "slow": 0,
    "avoid_lose_chance": 0.0,
    "instant_win_chance": 0.0,
    "fight_defense_boost_chance": 0.0,
    "fight_defense_boost_amount": 0,
}

boss_warning = 0
boss_alive = False
boss_defeated = False
boss_next_spawn_day = None
boss_cooldown_remaining = 0
BOSS_COOLDOWN_DAYS = 10
boss_encounter_count = 0

# Untuk chest merchant upgrade
merchant_extra_request_unlocked = False
bonus_speed_unlocked = False
merchant_timer = random.randint(3, 5)
merchant_request = None
merchant_active = False

# ---------- UTIL ----------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause(t=1):
    time.sleep(max(0.5, t))

def get_penalty_level():
    """
    Penalty level naik setelah hari 10, lalu setiap 5 hari lagi
    - Day 1-10   → Level 0
    - Day 11-15  → Level 1
    - Day 16-20  → Level 2
    - Day 21-25  → Level 3
    - dst.
    """
    if player["day"] < 11:
        return 0
    return 1 + max(0, (player["day"] - 16) // 5)

# ---------- CORE SYSTEM ----------
def generate_merchant():
    num_requests = 4 if merchant_extra_request_unlocked else 3
    wanted = random.sample(list(ores.keys()), num_requests)
    return {
        "wanted": {ore: random.randint(merchant_qty_range[0], merchant_qty_range[1]) for ore in wanted},
        "multiplier": round(random.uniform(1.4, 1.9), 2),
        "bonus": random.randint(50, 150),
        "sold": set()
    }

def get_phase():
    if player["day"] == 1:
        return 1
    elif player["day"] <= 5:
        return 2
    else:
        return 3

def enemy_level():
    return max(0, (player["day"] - 5) // 3)

def roll_enemy(phase):
    r = random.random()
    if phase == 1:
        return None
    if phase == 2:
        if r < 0.45:
            return None
        elif r < 0.75:
            return "Zombie"
        else:
            return random.choice(["Skeleton", "Spider"])
    # Phase 3
    if r < 0.35:
        return None
    elif r < 0.60:
        return "Zombie"
    elif r < 0.80:
        return random.choice(["Skeleton", "Spider"])
    elif r < 0.95:
        return "Creeper"
    else:
        return "Wither"

def fight(enemy):
    clear()
    print(f"⚔️ Encounter: {enemy}")
    
    level = get_penalty_level()
    if level > 0:
        print(f"⚠️ Penalty Level: {level}")
    
    pause()
    
    if random.random() < player["instant_win_chance"]:
        print(f"✨ Instant defeat! You crushed {enemy} instantly!")
        pause()
        return True
    
    temp_defense = player["defense"]
    if random.random() < player["fight_defense_boost_chance"]:
        temp_defense += player["fight_defense_boost_amount"]
        print(f"🛡️ Defense boosted by {player['fight_defense_boost_amount']} for this fight!")
        pause(1)
    
    base = enemies[enemy]["power"]
    
    if player["day"] <= 2:
        base *= 0.5
    elif player["day"] <= 4:
        base *= 0.75
    
    scale = 1 + enemy_level() * 0.25
    
    if enemy == "Boss":
        base *= 2.5
        scale *= 1.5
        print("🔥 THIS IS THE FINAL BATTLE 🔥")
        print("The Boss is overwhelmingly powerful!")
    
    enemy_power = base * scale
    chance = temp_defense / (temp_defense + enemy_power)
    
    print(f"Enemy strength: {enemy_power:.1f}")
    print(f"Your win chance: {chance*100:.1f}%")
    pause(2)
    
    if random.random() < chance:
        print(f"✅ You defeated {enemy}!")
        pause()
        return True
    else:
        print(f"💀 You were defeated by {enemy}...")
        pause()
        return False

def handle_lose(enemy):
    level = get_penalty_level()
    money_mult = 1 + 0.25 * level          # +25% per level
    stat_mult = 1 + 0.5 * (level // 2)     # stat loss naik lebih lambat
    
    if random.random() < player["avoid_lose_chance"]:
        print("🛡️ Lucky escape! You avoided the consequences!")
        pause(2)
        return
    
    if enemy in ["Zombie", "Skeleton", "Spider", "Creeper"]:
        lose_amount = int(enemies[enemy]["lose"] * money_mult)
        player["money"] = max(0, player["money"] - lose_amount)
        print(f"💸 Lost ${lose_amount} (x{money_mult:.1f} penalty)")
    
    elif enemy == "Wither":
        downgrade_amount = max(1, int(1 * stat_mult))
        stat = random.choice(["power", "defense", "speed"])
        if player[stat] > 1:
            old_stat = player[stat]
            player[stat] -= downgrade_amount
            player[stat] = max(1, player[stat])
            print(f"⬇️ Wither cursed you! {stat.capitalize()} downgraded by {downgrade_amount} (from {old_stat} to {player[stat]})")
        else:
            print(f"⬇️ Wither tried to curse you, but your {stat.capitalize()} is already at minimum!")
    
    elif enemy == "Boss":
        money_div = 2 + (level // 2)   # 2 → 2 → 3 → 3 → 4 ...
        stat_div = 2 + (level // 4)    # 2 → 2 → 2 → 3 ...
        
        player["money"] //= money_div
        for s in ["power", "defense", "speed"]:
            player[s] = max(1, player[s] // stat_div)
        
        print("💀 THE BOSS HAS CRUSHED YOU...")
        print(f"Money divided by {money_div}, stats by {stat_div} (Level {level})")
        print("But the fight isn't over yet...")
    
    pause(2)

def handle_win(enemy):
    if enemy == "Spider":
        babies = random.randint(1, 5)
        print(f"🕷️ {babies} baby spiders spawned")
        for _ in range(babies):
            print("👶 Baby spider defeated. Slowed.")
            player["slow"] += 1
            pause(0.5)
    
    if enemy == "Creeper":
        ore = random.choice(list(ores))
        qty = random.randint(1, 2)
        player["inventory"][ore] = player["inventory"].get(ore, 0) + qty
        print(f"💎 Creeper dropped {qty} {ore}")
    
    if enemy == "Boss":
        global boss_alive, boss_cooldown_remaining, boss_encounter_count
        boss_alive = False
        ore = random.choice(list(ores))
        qty = random.randint(5 + boss_encounter_count*2, 12 + boss_encounter_count*3)
        money_bonus = 500 + boss_encounter_count * 300
        
        player["inventory"][ore] = player["inventory"].get(ore, 0) + qty
        player["money"] += money_bonus
        
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"👑 BOSS DEFEATED! (Encounter #{boss_encounter_count}) 👑")
        print(f"+{qty} {ore}")
        print(f"+ ${money_bonus}")
        print("The mine trembles in relief...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        pause(4)
        
        boss_cooldown_remaining = BOSS_COOLDOWN_DAYS

# ---------- CHEST SYSTEM ----------
def open_chest():
    clear()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("   🛡️  YOU FOUND A MYSTERIOUS CHEST!  🛡️")
    print("   It opens with a glow...          ")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    pause(2)
    
    rewards = [
        "money",
        "merchant_extra",
        "avoid_lose",
        "bonus_speed",
        "instant_win",
        "double_money",
        "defense_boost"
    ]
    
    reward_type = random.choice(rewards)
    
    if reward_type == "money":
        amount = random.randint(250, 500)
        player["money"] += amount
        print(f"💰 You found {amount} money!")
    
    elif reward_type == "merchant_extra":
        global merchant_extra_request_unlocked
        if not merchant_extra_request_unlocked:
            merchant_extra_request_unlocked = True
            print("🧙‍♂️ Merchant now requests **4 different ores** permanently!")
        else:
            amount = random.randint(300, 600)
            player["money"] += amount
            print(f"💰 Extra ores already unlocked! You found {amount} money instead.")
    
    elif reward_type == "avoid_lose":
        chance = round(random.uniform(0.10, 0.35), 2)
        new_chance = min(player["avoid_lose_chance"] + chance, 0.35)
        gain = round(new_chance - player["avoid_lose_chance"], 2)
        player["avoid_lose_chance"] = new_chance
        if gain > 0:
            print(f"🛡️ Gained +{gain*100:.1f}% chance to avoid lose (total: {new_chance*100:.1f}%)")
        else:
            print(f"🛡️ Avoid lose chance sudah maksimal 35%! No increase.")
    
    elif reward_type == "bonus_speed":
        global bonus_speed_unlocked
        if not bonus_speed_unlocked:
            bonus_speed_unlocked = True
            player["bonus_speed"] += 10
            print("⚡ +10 bonus speed (free, upgrade cost unchanged)!")
        else:
            amount = random.randint(300, 600)
            player["money"] += amount
            print(f"⚡ Speed boost already unlocked! You found {amount} money instead.")
    
    elif reward_type == "instant_win":
        chance = round(random.uniform(0.01, 0.15), 2)
        new_chance = min(player["instant_win_chance"] + chance, 0.17)
        gain = round(new_chance - player["instant_win_chance"], 2)
        player["instant_win_chance"] = new_chance
        if gain > 0:
            print(f"✨ Gained +{gain*100:.2f}% instant win chance (total: {new_chance*100:.2f}%)")
        else:
            print(f"✨ Instant win chance sudah maksimal 17%! No increase.")
    
    elif reward_type == "double_money":
        player["money"] *= 2
        print("💰 Your money has been doubled!")
    
    elif reward_type == "defense_boost":
        chance = round(random.uniform(0.10, 0.20), 2)
        new_chance = min(player["fight_defense_boost_chance"] + chance, 0.35)
        gain_chance = round(new_chance - player["fight_defense_boost_chance"], 2)
        
        amounts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        weights = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        new_amount = random.choices(amounts, weights=weights)[0]
        final_amount = max(player["fight_defense_boost_amount"], new_amount)
        amount_gain = final_amount - player["fight_defense_boost_amount"]
        
        player["fight_defense_boost_chance"] = new_chance
        player["fight_defense_boost_amount"] = final_amount
        
        print(f"🛡️ Gained +{gain_chance*100:.1f}% chance to boost defense", end="")
        if amount_gain > 0:
            print(f" (amount now {final_amount})")
        else:
            print(f" (amount stays at {final_amount})")
        if gain_chance <= 0:
            print("   (chance sudah cap di 35%)")
    
    pause(3)

# ---------- GAMEPLAY ----------
def mine():
    global boss_warning, boss_alive, boss_defeated
    global boss_next_spawn_day, boss_cooldown_remaining, boss_encounter_count
    global merchant_active, merchant_request, merchant_timer, merchant_cooldown
    
    clear()
    phase = get_phase()
    print(f"📅 Day {player['day']}  | Phase {phase}\n")
    
    effective_speed = player["speed"] + player["bonus_speed"]
    duration = max(2, 6 - effective_speed + player["slow"])
    player["slow"] = 0
    
    for _ in range(random.randint(3, 5)):
        print(random.choice(events))
        pause(duration / 3)
    
    # ---------- BOSS LOGIC ----------
    if boss_next_spawn_day is None and player["day"] >= 12:
        boss_next_spawn_day = random.randint(12, 16)
    
    if boss_next_spawn_day is not None and player["day"] == boss_next_spawn_day:
        boss_warning = 3
        boss_alive = True
        boss_encounter_count += 1
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("   ⚠️  THE GROUND IS SHAKING...  ⚠️")
        print(f"   THE BOSS AWAKENS (Encounter #{boss_encounter_count})")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        pause(3)
        boss_next_spawn_day = None
    
    if boss_cooldown_remaining > 0:
        boss_cooldown_remaining -= 1
        if boss_cooldown_remaining == 0:
            boss_next_spawn_day = player["day"] + random.randint(1, 4)
    
    if boss_warning > 0:
        print(f"⚠️ BOSS WARNING {boss_warning}/3")
        boss_warning -= 1
        pause()
    
    if boss_warning == 0 and boss_alive and not boss_defeated:
        enemy = "Boss"
    else:
        enemy = roll_enemy(phase)
    
    # ---------- PERTARUNGAN ----------
    won_fight = False
    if enemy:
        win = fight(enemy)
        if not win:
            handle_lose(enemy)
            if enemy == "Boss":
                boss_alive = False
                boss_cooldown_remaining = random.randint(10, 16)
        else:
            won_fight = True
            handle_win(enemy)
            if enemy == "Boss":
                boss_alive = False
                boss_cooldown_remaining = random.randint(10, 16)
    
    # ---------- NORMAL ORE ----------
    if not enemy or won_fight:
        ore = random.choice(list(ores))
        power_level = player["power"]
        min_qty = (power_level // 5) + 1
        max_qty = 2 + player["power"]
        qty = random.randint(min_qty, max_qty)
        
        player["inventory"][ore] = player["inventory"].get(ore, 0) + qty
        print(f"\n🎉 Found {qty} {ore}")
        print("🏠 Going home...")
        pause(2)
    
    # ---------- AKHIR HARI ----------
    player["day"] += 1
    
    # ---------- MERCHANT LOGIC ----------
    if merchant_active:
        print("🧙‍♂️ The merchant has left for now...")
        pause(1.5)
        merchant_active = False
        merchant_request = None
        merchant_cooldown = MERCHANT_COOLDOWN_DAYS
    else:
        if merchant_cooldown > 0:
            merchant_cooldown -= 1
            if merchant_cooldown == 0:
                merchant_active = True
                merchant_request = generate_merchant()
                print("🧙‍♂️ A traveling merchant has arrived!")
                pause(1.5)
        else:
            merchant_timer -= 1
            if merchant_timer <= 0:
                merchant_active = True
                merchant_request = generate_merchant()
                print("🧙‍♂️ A traveling merchant has arrived!")
                pause(1.5)
    
    # ---------- CHEST LOGIC ----------
    if player["day"] >= 10 and (player["day"] - 10) % 5 == 0:
        open_chest()

# ---------- MENU ----------
def shop():
    clear()
    print("🛒 SHOP\n")
    if not player["inventory"]:
        print("Inventory kosong. Jangan bengong")
        pause()
        return
    for i, (o, q) in enumerate(player["inventory"].items(), 1):
        print(f"{i}. {o} x{q} (${ores[o]})")
    c = input("\nChoose ore (X to exit): ").lower()
    if c == "x":
        return
    try:
        idx = int(c) - 1
        ore = list(player["inventory"].keys())[idx]
        qty = player["inventory"][ore]
        gain = qty * ores[ore]
        player["money"] += gain
        del player["inventory"][ore]
        print(f"💰 Sold {ore} for ${gain}")
        pause()
    except:
        pass

def upgrade():
    clear()
    print("⚙️ UPGRADE\n")
    for i, s in enumerate(["power", "defense", "speed"], 1):
        print(f"{i}. {s.capitalize()} (${upgrade_cost[s] * player[s]})")
    print("X. Back")
    c = input("\n>> ").lower()
    if c not in ["1", "2", "3", "x"]:
        return
    if c == "x":
        return
    stat = ["power", "defense", "speed"][int(c)-1]
    cost = upgrade_cost[stat] * player[stat]
    if player["money"] >= cost:
        player["money"] -= cost
        player[stat] += 1
        print(f"⬆️ {stat} upgraded")
    else:
        print("❌ Uang tidak cukup, jangan ngutang")
    pause()

def inventory():
    clear()
    print("🎒 INVENTORY\n")
    if not player["inventory"]:
        print("Kosong. Kayak jiwaku")
    else:
        for o, q in player["inventory"].items():
            print(f"- {o}: {q}")
    pause()

def merchant():
    global merchant_active, merchant_request
    while True:
        clear()
        print("🧙‍♂️ Traveling Merchant\n")
        print("📦 Your Inventory:")
        if not player["inventory"]:
            print("- (empty)")
        else:
            for o, q in player["inventory"].items():
                print(f"- {o}: {q}")
        print("\n📝 Merchant wants:")
        for ore, qty in merchant_request["wanted"].items():
            status = "✔ SOLD" if ore in merchant_request["sold"] else ""
            print(f"- {ore} x{qty} {status}")
        print(f"\n💎 Price multiplier: x{merchant_request['multiplier']}")
        print(f"🎁 Bonus per ore (first time): ${merchant_request['bonus']}")
        print("\n0. Back")
        choice_map = {}
        idx = 1
        for ore in merchant_request["wanted"]:
            if ore not in merchant_request["sold"]:
                print(f"{idx}. Sell {ore}")
                choice_map[str(idx)] = ore
                idx += 1
        choice = input("\n>> ")
        if choice == "0":
            return
        if choice not in choice_map:
            continue
        ore = choice_map[choice]
        need = merchant_request["wanted"][ore]
        owned = player["inventory"].get(ore, 0)
        if owned < need:
            print(f"❌ You need exactly {need} {ore}")
            pause(1.5)
            continue
        base = need * ores[ore]
        total = int(base * merchant_request["multiplier"])
        if ore not in merchant_request["sold"]:
            total += merchant_request["bonus"]
            merchant_request["sold"].add(ore)
        player["inventory"][ore] -= need
        player["money"] += total
        print(f"💰 Sold {need} {ore} for ${total}")
        pause(1.5)
        if len(merchant_request["sold"]) == len(merchant_request["wanted"]):
            print("\n🧙‍♂️ Merchant is satisfied.")
            pause(2)
            return

def main_menu():
    while True:
        clear()
        print("=== TEXT MINER RPG ===\n")
        print(f"Day {player['day']}")
        print(f"💰 Money: ${player['money']}")
        print(f"⛏ Power: {player['power']} | 🛡 Defense: {player['defense']} | ⚡ Speed: {player['speed']} (+{player['bonus_speed']})")
        
        level = get_penalty_level()
        if level > 0:
            print(f"⚠️ Penalty Level: {level}")
        
        if merchant_active:
            print("🧙‍♂️ Merchant is here!")
        elif merchant_cooldown > 0:
            print(f"🧙‍♂️ Merchant arrives in {merchant_cooldown} day(s)")
        else:
            print(f"🧙‍♂️ Merchant arrives in {merchant_timer} day(s)")
        
        print("\nMenu:")
        print("1. Mine")
        print("2. Shop")
        print("3. Upgrade")
        print("4. Inventory")
        
        if merchant_active:
            print("5. Merchant 🧙‍♂️")
            print("6. Exit")
        else:
            print("5. Exit")
        
        choice = input("\n>> ").strip()
        
        if choice == "1":
            mine()
        elif choice == "2":
            shop()
        elif choice == "3":
            upgrade()
        elif choice == "4":
            inventory()
        elif merchant_active and choice == "5":
            merchant()
        elif (merchant_active and choice == "6") or (not merchant_active and choice == "5"):
            break
        else:
            print("Pilihan tidak valid, coba lagi.")
            pause(1.5)

# ---------- RUN ----------
if __name__ == "__main__":
    main_menu()