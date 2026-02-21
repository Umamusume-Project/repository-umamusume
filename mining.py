import random
import time
import os

merchant_qty_range = (1, 3)
class Mining:
    def __init__(self, farm, player, warung, merchant_qty_range):
        self.player = player
        self.merchant_qty_range = merchant_qty_range
        self.farm = farm
        self.warung = warung
        # Bos sama merchant
        self.boss_warning = 0
        self.boss_alive = False
        self.boss_defeated = False
        self.boss_cooldown_remaining = 0
        self.BOSS_COOLDOWN_DAYS = 10  # cooldown setelah dikalahkan (dalam mining count)
        self.boss_encounter_count = 0
        self.boss_min_mining = 12  # minimal mining sebelum boss pertama muncul
        self.merchant_request = None
        self.merchant_active = False
        self.merchant_countdown = 0
        self.slow = 0
        # data mining
        self.enemies = {
            "Zombie": {"power": 1.0, "lose": 15},
            "Skeleton": {"power": 2.0, "lose": 35},
            "Spider": {"power": 0.7, "lose": 10},
            "Creeper": {"power": 3.0, "lose": 80},
            "Wither": {"power": 4.0, "lose": 0},
            "Boss": {"power": 6.0, "lose": 0},
        }
        self.ores = {
            "Coal": 5,
            "Iron": 15,
            "Crystal": 25,
            "Emerald": 50,
            "Diamond": 70,
        }
        self.events = [
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

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self, t=1):
        time.sleep(max(0.5, t))

    def get_penalty_level(self):
        mc = self.player.mining_count
        if mc < 11:
            return 0
        return 1 + max(0, (mc - 16) // 5)

    def get_phase(self):
        mc = self.player.mining_count
        if mc == 1:
            return 1
        elif mc <= 5:
            return 2
        else:
            return 3

    def enemy_level(self):
        return max(0, (self.player.mining_count - 5) // 3)

    def roll_enemy(self, phase):
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

    def generate_merchant(self):
        num_requests = 3
        wanted = random.sample(list(self.ores.keys()), num_requests)
        return {
            "wanted": {ore: random.randint(self.merchant_qty_range[0], self.merchant_qty_range[1]) for ore in wanted},
            "multiplier": round(random.uniform(1.4, 1.9), 2),
            "bonus": random.randint(50, 100),
            "sold": set()
        }

    def fight(self, enemy):
        self.clear()
        print(f"⚔️ wah ketemu: {enemy}")
        
        level = self.get_penalty_level()
        if level > 0:
            print(f"⚠️ Level Penalti: {level}")
        self.pause()
        
        base = self.enemies[enemy]["power"]
        if self.player.mining_count <= 2:
            base *= 0.5
        elif self.player.mining_count <= 4:
            base *= 0.75
        
        scale = 1 + self.enemy_level() * 0.25
        
        if enemy == "Boss":
            base *= 2.5
            scale *= 1.5
            print("🔥 INI PERTARUNGAN AKHIR 🔥")
            print("Boss sangat sangat kuat!")
        
        enemy_power = base * scale
        chance = self.player.defense / (self.player.defense + enemy_power)
        
        print(f"Kekuatan musuh: {enemy_power:.1f}")
        print(f"Peluang menang kamu: {chance*100:.1f}%")
        self.pause(2)
        
        if random.random() < chance:
            print(f"✅ Kamu berhasil mengalahkan {enemy}!")
            self.pause()
            return True
        else:
            print(f"💀 yah kau kalah sama {enemy}...")
            self.pause()
            return False

    def handle_lose(self, enemy):
        level = self.get_penalty_level()
        money_mult = 1 + 0.25 * level
        player = self.player
        
        if enemy in ["Zombie", "Skeleton", "Spider", "Creeper"]:
            lose_amount = int(self.enemies[enemy]["lose"] * money_mult)
            if player.uang >= lose_amount:
                player.kurangi_uang(lose_amount)
                print(f"💸 Kehilangan ${lose_amount} (penalti x{money_mult:.1f})")
            else:
                print(f"💸 Uangmu sudah habis! aku jadi merasa kasian..")
                player.kurangi_uang(player.uang)
        elif enemy == "Wither":
            stat = random.choice(['power', 'defense', 'speed'])
            current_stat = getattr(player, stat)
            if current_stat > 1:
                setattr(player, stat, current_stat - 1)
                print(f"Wither mengutukmu! {stat.capitalize()} turun 1")
            else:
                print(f"Wither mencoba mengutuk, tapi {stat.capitalize()} sudah minimal!")
                self.pause(1)
                print("Wither: Dasar skill issue!")
                self.pause(2)
                
        elif enemy == "Boss":
            money_div = 2 + (level // 2)
            lose_amount = player.uang // money_div
            if player.uang >= lose_amount:
                player.kurangi_uang(lose_amount)
                print(f"💸 Kehilangan ${lose_amount} (dibagi {money_div})")
            else:
                print(f"💸 Uangmu tidak cukup untuk penalti boss! Uang jadi 0.")
                player.kurangi_uang(player.uang)
            
            for stat in ["power", "defense", "speed"]:
                setattr(player, stat, max(1, getattr(player, stat) // (2 + (level // 4))))
            
            print("BOSS MENGGEPREK KAU...")
            print(f"Uang dibagi {money_div}, stat dibagi {2 + (level // 4)} (Level {level})")
        
        self.pause(2)

    def handle_win(self, enemy):
        player = self.player
        
        if enemy == "Spider":
            babies = random.randint(1, 5)
            print(f"🕷️ Muncul {babies} baby spider!")
            for i in range(babies):
                print(f"   👶 Baby spider ke-{i+1} dikalahkan. Kamu jadi lebih lambat.")
                self.slow += 1
                time.sleep(0.5)
            self.pause(1)
        
        if enemy == "Creeper":
            ore = random.choice(list(self.ores))
            qty = random.randint(1, 2)
            player.inventory.tambah_barang(ore, qty, "ore")
            print(f"Creeper menjatuhkan {qty} {ore}")
        
        if enemy == "Boss":
            self.boss_alive = False
            self.boss_defeated = True
            self.boss_warning = 0  # reset warning
            ore = random.choice(list(self.ores))
            qty = random.randint(5 + self.boss_encounter_count*2, 12 + self.boss_encounter_count*3)
            money_bonus = 400
            player.inventory.tambah_barang(ore, qty, "ore")
            player.tambah_uang(money_bonus)
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"👑 BOSS DIKALAHKAN! (Pertarungan ke-{self.boss_encounter_count}) 👑")
            print(f"+{qty} {ore}")
            print(f"+ ${money_bonus}")
            print("Tambang bergetar lega...")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            self.pause(4)
            
            # Reset cooldown boss
            self.boss_cooldown_remaining = self.BOSS_COOLDOWN_DAYS
            print(f"Boss akan muncul lagi setelah {self.BOSS_COOLDOWN_DAYS} mining.")

    def open_chest(self):
        self.clear()
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" 🛡️ KAMU MENEMUKAN PETI MISTERIUS! 🛡️")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        time.sleep(2)
        amount = int(random.expovariate(1 / 30)) + 10
        amount = min(amount, 40)
        self.player.tambah_uang(amount)
        print(f"💰 Kamu menemukan ${amount} uang!")
        time.sleep(3)

    def upgrade_stats(self):
        while True:
            self.clear()
            print('==================')
            print('       UPGRADE STATS')
            print('==================')
            print(f"1. Power      (Level {self.player.power}) - Biaya: {45 * self.player.power}")
            print(f"2. Defense    (Level {self.player.defense}) - Biaya: {60 * self.player.defense}")
            print(f"3. Speed      (Level {self.player.speed}) - Biaya: {30 * self.player.speed}")
            print(f"4. Max Stamina (Max {self.player.max_stamina}) - Biaya: 85")
            print('0. Kembali')
            print('==================')
            pilihan = input('Pilih upgrade (0-4): ').strip()

            if pilihan == '0':
                return

            stat_map = {'1': ('power', 45), '2': ('defense', 60), '3': ('speed', 30), '4': ('max_stamina', 85)}
            if pilihan in stat_map:
                stat, base_cost = stat_map[pilihan]
                cost = base_cost if stat == 'max_stamina' else base_cost * getattr(self.player, stat)

                if self.player.uang >= cost:
                    self.player.kurangi_uang(cost)
                    if stat == 'max_stamina':
                        self.player.max_stamina += 20
                        print(f"Max stamina berhasil diupgrade! Sekarang: {self.player.max_stamina}")
                    else:
                        setattr(self.player, stat, getattr(self.player, stat) + 1)
                        print(f"{stat.capitalize()} berhasil diupgrade! Level sekarang: {getattr(self.player, stat)}")
                else:
                    print(f'Uang tidak cukup! Butuh ${cost}, kamu punya ${self.player.uang}')
            
            else:
                print('Pilihan tidak valid.')
            
            input('Tekan Enter untuk melanjutkan...')

    def mine(self):
        player = self.player
        
        if player.stamina < 20:
            print("Aku capeeekkk, biarkan aku tidur...")
            self.pause(2)
            return
        
        player.kurangi_stamina(20)
        print(f"Stamina berkurang -20 (sisa: {player.stamina}/{player.max_stamina})")
        self.pause(1)
        
        self.clear()
        phase = self.get_phase()
        print(f"⛏ Mining ke-{player.mining_count} | Fase {phase}\n")
        
        effective_speed = player.speed
        duration = max(2, 6 - effective_speed + self.slow)
        self.slow = 0
        
        for _ in range(random.randint(3, 5)):
            print(random.choice(self.events))
            self.pause(duration / 3)
        
        # --- BOSS SPAWN LOGIC ---
        # Hanya mulai cek boss setelah mining minimal
        if player.mining_count >= self.boss_min_mining:
            # Kurangi cooldown setiap mining
            if self.boss_cooldown_remaining > 0:
                self.boss_cooldown_remaining -= 1
            
            # Saat cooldown habis, boss bisa muncul
            if self.boss_cooldown_remaining == 0 and not self.boss_alive:
                # Random chance agar tidak pasti setiap mining setelah cooldown
                if random.random() < 0.4:  # 40% chance tiap mining setelah cooldown habis
                    self.boss_warning = 3
                    self.boss_alive = True
                    self.boss_encounter_count += 1
                    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                    print(" ⚠️ TANAH BERGETAR HEBAT... ⚠️")
                    print(f" BOSS BANGKIT (Pertarungan ke-{self.boss_encounter_count})")
                    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                    self.pause(3)
        
        # Warning boss (3 mining countdown sebelum fight)
        if self.boss_warning > 0:
            print(f"⚠️ PERINGATAN BOSS {self.boss_warning}/3")
            self.boss_warning -= 1
            self.pause()
        
        # Tentukan enemy
        if self.boss_warning == 0 and self.boss_alive and not self.boss_defeated:
            enemy = "Boss"
        else:
            enemy = self.roll_enemy(phase)
        
        won_fight = False
        if enemy:
            win = self.fight(enemy)
            if not win:
                self.handle_lose(enemy)
                player.kurangi_stamina(10)
                print(f"Stamina berkurang tambahan -10 karena kalah! (sisa: {player.stamina}/{player.max_stamina})")
                self.pause(1)
                
                if enemy == "Boss":
                    self.boss_alive = False
                    self.boss_warning = 0  # reset warning
                    self.boss_cooldown_remaining = self.BOSS_COOLDOWN_DAYS  # reset cooldown
            else:
                won_fight = True
                self.handle_win(enemy)
                if enemy == "Boss":
                    self.boss_alive = False
                    self.boss_warning = 0  # reset warning
                    self.boss_cooldown_remaining = self.BOSS_COOLDOWN_DAYS  # reset cooldown
        
        if not enemy or won_fight:
            ore = random.choice(list(self.ores))
            power_level = player.power
            min_qty = (power_level // 5) + 1
            max_qty = 2 + player.power
            qty = random.randint(min_qty, max_qty)
            
            player.inventory.tambah_barang(ore, qty, "ore")
            print(f"\nMenemukan {qty} {ore}")
            print("kembali ke menu utama...")
            self.pause(2)
        
        player.mining_count += 1
        
        if player.mining_count % 6 == 0:
            self.merchant_active = True
            self.merchant_request = self.generate_merchant()
            self.merchant_countdown = 0
            print("Pedagang keliling datang!")
            self.pause(1.5)
        elif self.merchant_active:
            print("Pedagang sudah pergi untuk sementara...")
            self.pause(1.5)
            self.merchant_active = False
            self.merchant_request = None
            self.merchant_countdown = 5
        elif self.merchant_countdown > 0:
            self.merchant_countdown -= 1
        
        if player.mining_count >= 10 and (player.mining_count - 10) % 5 == 0:
            self.open_chest()

    def merchant(self):
        while True:
            self.clear()
            player = self.player
            merchant_request = self.merchant_request
            
            print("🧙‍♂️ Pedagang Keliling\n")
            
            print("📦 Inventarismu saat ini:")
            if not player.inventory.items:
                print("   (Kosong)")
            else:
                for barang, data in player.inventory.items.items():
                    tipe = data.get('tipe', 'tidak diketahui')
                    jumlah = data.get('jumlah', 0)
                    print(f"   - {barang} ({tipe}) : {jumlah}")
            
            print("─" * 60)
            
            print("📝 Pedagang ingin membeli:")
            for ore, qty in merchant_request["wanted"].items():
                status_text = "✔ SUDAH DIJUAL" if ore in merchant_request["sold"] else ""
                print(f"   - {ore} x{qty} {status_text}")
            
            print(f"\nPengali harga: x{merchant_request['multiplier']}")
            print(f"Bonus per jenis (sekali): ${merchant_request['bonus']}")
            
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
                self.pause(1)
                continue
            
            ore = choice_map[choice]
            need = merchant_request["wanted"][ore]
            owned = player.inventory.items.get(ore, {"jumlah": 0})["jumlah"]
            
            if owned < need:
                print(f"Kamu hanya punya {owned} {ore}, tapi pedagang minta {need}!")
                self.pause(1.5)
                continue
            
            base = need * self.ores[ore]
            total = int(base * merchant_request["multiplier"])
            if ore not in merchant_request["sold"]:
                total += merchant_request["bonus"]
                merchant_request["sold"].add(ore)
            
            player.inventory.items[ore]["jumlah"] -= need
            if player.inventory.items[ore]["jumlah"] <= 0:
                del player.inventory.items[ore]
            
            player.tambah_uang(total)
            print(f"Berhasil menjual {need} {ore} seharga ${total}")
            self.pause(1.5)
            
            if len(merchant_request["sold"]) == len(merchant_request["wanted"]):
                print("\nPedagang puas dan pergi.")
                self.pause(2)
                self.merchant_active = False
                return

    def main_menu(self):
        while True:
            self.clear()
            player = self.player
            warung = self.warung
            print("=== Mining Menu ===\n")
            print(f"Mining ke-{player.mining_count}")
            print(f" Uang   : {player.uang}")
            print(f" Stamina: {player.stamina}/{player.max_stamina}")
            print(f"Power: {player.power} | 🛡 Defense: {player.defense} | ⚡ Speed: {player.speed}")
            
            level = self.get_penalty_level()
            if level > 0:
                print(f"Level Penalti: {level}")
            
            if self.merchant_active:
                print("Pedagang sedang ada di sini!")
            else:
                if self.merchant_countdown > 0:
                    print(f"Pedagang datang lagi dalam {self.merchant_countdown} mining")
                else:
                    print("Pedagang sedang dalam perjalanan...")
            
            print("\nMenu:")
            print("1. Mulai Menambang")
            print("2. Upgrade Stats")
            print("0. Kembali ke menu hari")
            
            if self.merchant_active:
                print("3. Temui Pedagang")
            
            choice = input("\n>> ").strip()
            
            if choice == "1":
                self.mine()
            elif choice == "2":
                self.upgrade_stats()
            elif self.merchant_active and choice == "3":
                self.merchant()
            elif choice == "0":
                break
            else:
                print("Pilihan tidak valid, coba lagi.")
                self.pause(1.5)
