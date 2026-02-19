import random
import time
import player
import os

merchant_qty_range = (1, 3)

enemies = {
    "Zombie": {"power": 1.0, "lose": 15},
    "Skeleton": {"power": 2.0, "lose": 35},
    "Spider": {"power": 0.7, "lose": 10},
    "Creeper": {"power": 3.0, "lose": 80},
    "Wither": {"power": 4.0, "lose": 0},
    "Boss": {"power": 6.0, "lose": 0},
}

ores = {
    "Coal": 5,
    "Iron": 15,
    "Crystal": 25,
    "Emerald": 50,
    "Diamond": 70,
}

upgrade_cost = {
    "power": 45,
    "defense": 60,
    "speed": 30,
}

events = [
    "Nambang...",
    "Nambang ke bawah...",
    "Duaarrrr...",
    "Masuk lebih dalam...",
    "Nyangkut...",
    "Tadi itu creeper ya?...",
    "Ada Santa lewat...",
    "Nambang nikel...",
    "Nambang lagi...",
    "Batu ini kelihatan berkilau...",
    "Cape bro...",
    "Yang tadi diamond beneran?...",
    "Tadi ada Steve lewat...",
    "Sekali lagi...",
]

player = {
    "mining_count": 1,
    "power": 1,
    "defense": 1,
    "speed": 1,
    "slow": 0,
}

boss_warning = 0
boss_alive = False
boss_defeated = False
boss_next_spawn_day = None
boss_cooldown_remaining = 0
BOSS_COOLDOWN_DAYS = 10
boss_encounter_count = 0
merchant_request = None
merchant_active = False
merchant_countdown = 0

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause(t=1):
    time.sleep(max(0.5, t))

def get_penalty_level():
    if player["mining_count"] < 11:
        return 0
    return 1 + max(0, (player["mining_count"] - 16) // 5)

def generate_merchant():
    num_requests = 3
    wanted = random.sample(list(ores.keys()), num_requests)
    return {
        "wanted": {ore: random.randint(merchant_qty_range[0], merchant_qty_range[1]) for ore in wanted},
        "multiplier": round(random.uniform(1.4, 1.9), 2),
        "bonus": random.randint(50, 100),
        "sold": set()
    }

def get_phase():
    if player["mining_count"] == 1:
        return 1
    elif player["mining_count"] <= 5:
        return 2
    else:
        return 3

def enemy_level():
    return max(0, (player["mining_count"] - 5) // 3)

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
    print(f"⚔️ wah ketemu: {enemy}")
    
    level = get_penalty_level()
    if level > 0:
        print(f"⚠️ Level Penalti: {level}")
    
    pause()
    
    base = enemies[enemy]["power"]
    
    if player["mining_count"] <= 2:
        base *= 0.5
    elif player["mining_count"] <= 4:
        base *= 0.75
    
    scale = 1 + enemy_level() * 0.25
    
    if enemy == "Boss":
        base *= 2.5
        scale *= 1.5
        print("🔥 INI PERTARUNGAN AKHIR 🔥")
        print("Boss sangat sangat kuat!")
    
    enemy_power = base * scale
    chance = player["defense"] / (player["defense"] + enemy_power)
    
    print(f"Kekuatan musuh: {enemy_power:.1f}")
    print(f"Peluang menang kamu: {chance*100:.1f}%")
    pause(2)
    
    if random.random() < chance:
        print(f"✅ Kamu berhasil mengalahkan {enemy}!")
        pause()
        return True
    else:
        print(f"💀 yah kau kalah sama {enemy}...")
        pause()
        return False

def handle_lose(enemy):
    level = get_penalty_level()
    money_mult = 1 + 0.25 * level
    
    if enemy in ["Zombie", "Skeleton", "Spider", "Creeper"]:
        lose_amount = int(enemies[enemy]["lose"] * money_mult)
        
        current = player.uang.cek()
        new_money = max(0, current - lose_amount)
        player.uang.set(new_money)
        
        print(f"💸 Kehilangan ${lose_amount} (penalti x{money_mult:.1f})")
        if new_money == 0:
            print("Uang kamu habis total! Kini saldo: $0")
    
    elif enemy == "Wither":
        stat = random.choice(["power", "defense", "speed"])
        if player[stat] > 1:
            player[stat] -= 1
            print(f"⬇️ Wither mengutukmu! {stat.capitalize()} turun 1")
        else:
            print(f"⬇️ Wither mencoba mengutuk, tapi {stat.capitalize()} sudah minimal!")
            pause()
            print("Wither: Dasar skill issue!")
    
    elif enemy == "Boss":
        money_div = 2 + (level // 2)
        stat_div = 2 + (level // 4)
        
        current = player.uang.cek()
        new_money = max(0, current // money_div)
        player.uang.set(new_money)
        
        for s in ["power", "defense", "speed"]:
            player[s] = max(1, player[s] // stat_div)
        
        print("💀 BOSS MENGGEPREK KAU...")
        print(f"Uang dibagi {money_div}, stat dibagi {stat_div} (Level {level})")
        if new_money == 0:
            print("Uang kamu habis total! Kini saldo: $0")
    
    pause(2)

def handle_win(enemy, game):
    if enemy == "Spider":
        babies = random.randint(1, 5)
        print(f"🕷️ Muncul {babies} baby spider!")
        for _ in range(babies):
            print("👶 Baby spider dikalahkan. Kamu jadi lambat.")
            player["slow"] += 1
            pause(0.5)
    
    if enemy == "Creeper":
        ore = random.choice(list(ores))
        qty = random.randint(1, 2)
        game.inventory.tambah_barang(ore, qty, "ore")
        print(f"💎 Creeper menjatuhkan {qty} {ore}")
    
    if enemy == "Boss":
        global boss_alive, boss_cooldown_remaining, boss_encounter_count
        boss_alive = False
        ore = random.choice(list(ores))
        qty = random.randint(5 + boss_encounter_count*2, 12 + boss_encounter_count*3)
        money_bonus = 500 + boss_encounter_count * 300
        
        game.inventory.tambah_barang(ore, qty, "ore")
        player.uang.tambah_uang(money_bonus)
        
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"👑 BOSS DIKALAHKAN! (Pertarungan ke-{boss_encounter_count}) 👑")
        print(f"+{qty} {ore}")
        print(f"+ ${money_bonus}")
        print("Tambang bergetar lega...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        pause(4)
        
        boss_cooldown_remaining = BOSS_COOLDOWN_DAYS

def open_chest(game):
    clear()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" 🛡️ KAMU MENEMUKAN PETI MISTERIUS! 🛡️")
    print(" Peti nya  silau banget gila... ")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    time.sleep(2)
    
    amount = int(random.expovariate(1 / 30)) + 10
    amount = min(amount, 200)
    
    player.uang.tambah_uang(amount)
    
    print(f"💰 Kamu menemukan ${amount} uang!")
    
    time.sleep(3)

def mine(game):
    global boss_warning, boss_alive, boss_defeated
    global boss_next_spawn_day, boss_cooldown_remaining, boss_encounter_count
    global merchant_active, merchant_request, merchant_countdown
    
    if player.Status.stamina < 30:
        print("😭Aku capeeekkk, biarkan aku tidur...")
        pause(2)
        return
    
    player.Status.kurangi_stamina(30)
    print(f"Stamina berkurang -30 (sisa: {player.Status.stamina}/{player.Status.max_stamina})")
    pause(1)
    
    clear()
    phase = get_phase()
    print(f"⛏ Mining ke-{player['mining_count']} | Fase {phase}\n")
    
    effective_speed = player["speed"]
    duration = max(2, 6 - effective_speed + player["slow"])
    player["slow"] = 0
    
    for _ in range(random.randint(3, 5)):
        print(random.choice(events))
        pause(duration / 3)
    
    if boss_next_spawn_day is None and player["mining_count"] >= 12:
        boss_next_spawn_day = random.randint(12, 16)
    
    if boss_next_spawn_day is not None and player["mining_count"] == boss_next_spawn_day:
        boss_warning = 3
        boss_alive = True
        boss_encounter_count += 1
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" ⚠️ TANAH BERGETAR HEBAT... ⚠️")
        print(f" BOSS BANGKIT (Pertarungan ke-{boss_encounter_count})")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        pause(3)
        boss_next_spawn_day = None
    
    if boss_cooldown_remaining > 0:
        boss_cooldown_remaining -= 1
        if boss_cooldown_remaining == 0:
            boss_next_spawn_day = player["mining_count"] + random.randint(1, 4)
    
    if boss_warning > 0:
        print(f"⚠️ PERINGATAN BOSS {boss_warning}/3")
        boss_warning -= 1
        pause()
    
    if boss_warning == 0 and boss_alive and not boss_defeated:
        enemy = "Boss"
    else:
        enemy = roll_enemy(phase)
    
    won_fight = False
    if enemy:
        win = fight(enemy)
        if not win:
            handle_lose(enemy)
            player.Status.kurangi_stamina(10)
            print(f"Stamina berkurang tambahan -10 karena kalah! (sisa: {player.Status.stamina}/{player.Status.max_stamina})")
            pause(1)
            
            if enemy == "Boss":
                boss_alive = False
                boss_cooldown_remaining = random.randint(10, 16)
        else:
            won_fight = True
            handle_win(enemy, game)
            if enemy == "Boss":
                boss_alive = False
                boss_cooldown_remaining = random.randint(10, 16)
    
    if not enemy or won_fight:
        ore = random.choice(list(ores))
        power_level = player["power"]
        min_qty = (power_level // 5) + 1
        max_qty = 2 + player["power"]
        qty = random.randint(min_qty, max_qty)
        
        game.inventory.tambah_barang(ore, qty, "ore")
        print(f"\n🎉 Menemukan {qty} {ore}")
        print("🏠 Pulang ke rumah...")
        pause(2)
    
    player["mining_count"] += 1
    
    if player["mining_count"] % 6 == 0:
        merchant_active = True
        merchant_request = generate_merchant()
        merchant_countdown = 0
        print("🧙‍♂️ Pedagang keliling datang!")
        pause(1.5)
    elif merchant_active:
        print("🧙‍♂️ Pedagang sudah pergi untuk sementara...")
        pause(1.5)
        merchant_active = False
        merchant_request = None
        merchant_countdown = 5
    elif merchant_countdown > 0:
        merchant_countdown -= 1
    
    if player["mining_count"] >= 10 and (player["mining_count"] - 10) % 5 == 0:
        open_chest(game)

def upgrade():
    clear()
    print("⚙️ UPGRADE\n")
    for i, s in enumerate(["power", "defense", "speed"], 1):
        print(f"{i}. {s.capitalize()} (${upgrade_cost[s] * player[s]})")
    print("0. Kembali")
    c = input("\n>> ").strip().lower()
    if c == "0":
        return
    if c not in ["1", "2", "3"]:
        print("Pilihan tidak valid.")
        pause(1)
        return
    stat = ["power", "defense", "speed"][int(c)-1]
    cost = upgrade_cost[stat] * player[stat]
    if player.uang.cek() >= cost:
        player.uang.kurangi_uang(cost)
        player[stat] += 1
        print(f"⬆️ {stat.capitalize()} berhasil di-upgrade!")
    else:
        print("❌ Uang tidak cukup, jangan ngutang!")
    pause()

def merchant(game):
    global merchant_active, merchant_request, merchant_countdown
    while True:
        clear()
        print("🧙‍♂️ Pedagang Keliling\n")
        
        # Tampilkan inventory + permintaan pedagang bersamaan
        print("📦 Inventarismu saat ini:")
        if not game.inventory.inventory:
            print("   (Kosong)")
        else:
            for barang, data in game.inventory.inventory.items():
                print(f"   - {barang} ({data['tipe']}) : {data['jumlah']}")
        
        print("─" * 50)
        
        print("📝 Pedagang ingin membeli:")
        for ore, qty in merchant_request["wanted"].items():
            status_text = "✔ SUDAH DIJUAL" if ore in merchant_request["sold"] else ""
            print(f"   - {ore} x{qty} {status_text}")
        
        print(f"\n💎 Pengali harga: x{merchant_request['multiplier']}")
        print(f"🎁 Bonus per jenis (sekali): ${merchant_request['bonus']}")
        
        print("\nMenu:")
        print("0. Kembali")
        
        choice_map = {}
        idx = 1
        for ore in merchant_request["wanted"]:
            if ore not in merchant_request["sold"]:
                print(f"{idx}. Jual {ore}")
                choice_map[str(idx)] = ore
                idx += 1
        
        choice = input("\n>> ").strip()
        
        if choice == "0":
            return
        
        if choice not in choice_map:
            print("Pilihan tidak valid.")
            pause(1)
            continue
        
        ore = choice_map[choice]
        need = merchant_request["wanted"][ore]
        owned = game.inventory.inventory.get(ore, {"jumlah": 0})["jumlah"]
        
        if owned < need:
            print(f"❌ Kamu hanya punya {owned} {ore}, tapi pedagang minta {need}!")
            pause(1.5)
            continue
        
        base = need * ores[ore]
        total = int(base * merchant_request["multiplier"])
        if ore not in merchant_request["sold"]:
            total += merchant_request["bonus"]
            merchant_request["sold"].add(ore)
        
        game.inventory.inventory[ore]["jumlah"] -= need
        if game.inventory.inventory[ore]["jumlah"] <= 0:
            del game.inventory.inventory[ore]
        
        player.uang.tambah_uang(total)
        print(f"💰 Berhasil menjual {need} {ore} seharga ${total}")
        pause(1.5)
        
        if len(merchant_request["sold"]) == len(merchant_request["wanted"]):
            print("\n🧙‍♂️ Pedagang puas dan pergi.")
            pause(2)
            merchant_active = False
            return

def main_menu(game):
    global merchant_active, merchant_request, merchant_countdown
    
    while True:
        clear()
        print("=== TEXT MINER RPG ===\n")
        print(f"Mining ke-{player['mining_count']} (Day {player.Status.day}) - Penambangan")
        print(f" Uang   : ${player.uang.cek()}")
        print(f" Stamina: {player.Status.stamina}/{player.Status.max_stamina}")
        print(f"⛏ Power: {player['power']} | 🛡 Defense: {player['defense']} | ⚡ Speed: {player['speed']}")
        
        level = get_penalty_level()
        if level > 0:
            print(f"⚠️ Level Penalti: {level}")
        
        if merchant_active:
            print("🧙‍♂️ Pedagang sedang ada di sini!")
        else:
            if merchant_countdown > 0:
                print(f"🧙‍♂️ Pedagang datang lagi dalam {merchant_countdown} mining")
            else:
                print("🧙‍♂️ Pedagang sedang dalam perjalanan...")
        
        print("\nMenu:")
        print("1. Mulai Menambang")
        print("2. Upgrade")
        print("0. Kembali ke menu hari")
        
        if merchant_active:
            print("6. Temui Pedagang 🧙‍♂️")
        
        choice = input("\n>> ").strip()
        
        if choice == "1":
            mine(game)
        elif choice == "2":
            upgrade()
        elif merchant_active and choice == "6":
            merchant(game)
        elif choice == "0":
            break
        else:
            print("Pilihan tidak valid, coba lagi.")
            pause(1.5)
