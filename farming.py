import os
import inventory
import shop
import status

class Player:
    def __init__(self):
        self.day, self.stamina, self.max_stamina = status.Status.cek_status()
        self.uang = status.uang.cek()
        self.inv = inventory.inventory.inventory

class Crop:
    def __init__(self, name):
        self.grow_time = {
            "Wheat": 5,
            "Sawit": 6,
            "Ganja": 13,
            "Tembakau": 7,
            'Jagung' : 8
        }
        self.crop_age = 0
        self.name = name
        self.watered_today = False
    
    def grow(self):
        self.crop_age += 1
        return self.crop_age

    def is_ready(self):
        return self.crop_age >= self.grow_time[self.name]

class Farm:
    def __init__(self):
        self.slots = [None, None, None, None]
        self.player = Player()

    def plant(self, index):
        if self.slots[index] is None:
            # Check if there are any seeds (benih) in inventory
            benih_list = [(nama, data) for nama, data in self.player.inv.items() if data.get('tipe') == 'benih']
            
            if not benih_list:
                print('Belum ada benih, silahkan beli di shop!')
                input('')
                return
            
            print("\nPilih Tanaman:")
            for idx, (crop_name, crop_data) in enumerate(benih_list, start=1):
                print(f"{idx}. {crop_name} : {crop_data['jumlah']} tersedia")
            print("====================")
            pilih = input("> ")

            try:
                idx = int(pilih) - 1
                if 0 <= idx < len(benih_list):
                    selected_crop, selected_data = benih_list[idx]
                    self.slots[index] = Crop(selected_crop.replace("Benih ", ""))
                    
                    # Reduce inventory
                    self.player.inv[selected_crop]['jumlah'] -= 1
                    if self.player.inv[selected_crop]['jumlah'] <= 0:
                        del self.player.inv[selected_crop]
                    
                    print(f"{selected_crop} Berhasil ditanam!")
                    input("Enter untuk kembali...")
                    status.Status.kurangi_stamina(10)
                else:
                    print("Pilihan tidak valid!")
                    input("Enter untuk kembali...")
            except (ValueError, IndexError):
                print("Input tidak valid!")
                input("Enter untuk kembali...")

        else:
            print("Lahan sudah terisi!")
            input("Enter untuk kembali...")

    def water(self, index):
        crop = self.slots[index]
        if crop is None:
            print("Tidak ada tanaman di slot ini!")
            input("Enter untuk kembali...")
            return
        
        if crop.watered_today:
            print(f"{crop.name} sudah disiram hari ini!")
            input("Enter untuk kembali...")
            return
        
        crop.watered_today = True
        status.Status.kurangi_stamina(5)
        print(f"{crop.name} berhasil disiram!")
        input("Enter untuk kembali...")
          
    def panen(self, index):
        crop = self.slots[index]
        if crop is None:
            print("Tidak ada tanaman di lahan ini!")
            input("")
            return
        
        if not crop.is_ready():
            sisa = crop.grow_time.get(crop.name) - crop.crop_age
            print(f"{crop.name} belum siap panen! Sisa {sisa} hari lagi.")
            input("Enter untuk kembali...")
            return
        
        # Tambahkan hasil panen ke inventory
        hasil = crop.name
        if hasil in self.player.inv:
            self.player.inv[hasil]['jumlah'] += 1
        else:
            self.player.inv[hasil] = {'jumlah' : 1, 'tipe' : 'Tanaman'}

        self.slots[index] = None
        status.Status.kurangi_stamina(10)
        print(f'{hasil} berhasil dipanen!')
        input('')

    def next_day(self):
        for crop in self.slots:
            if crop is not None:
                if crop.watered_today:
                    crop.grow()
                crop.watered_today = False

# --------------MENU UTAMA----------------
class Game:
    def __init__(self):
        self.running = False
        self.player = Player()
        self.farm = Farm()

    def farmMenu(self):
        while True:
            os.system("cls")
            print("==========Farm Game==========")
            print(f"day\t:{status.Status.day}")
            print(f"duit\t:{status.uang.saldo}")
            print(f"stamina\t:{status.Status.stamina}")
            print("=============================")
            print("1. Pilih Lahan\n2. Inventory\n3. Shop")
            print("=============================")
            print("0. Kembali?")
            pilih = input("> ")

            if pilih == "1":
                self.slot_tanam()
            elif pilih == "2":
                inventory.inventory.menu()
            elif pilih == "3":
                shop.shop.toko()
            elif pilih == "0":
                from day import hari
                hari()
            else:
                continue

    def slot_tanam(self):
        while True:
            os.system("cls")
            print("==========Slot==========")
            print("Pilih Slot untuk Menanam")
            print("========================")
            print("1. Slot #1\n2. Slot #2\n3. Slot #3\n4. Slot #4")
            print("========================")
            print("0. Kembali?")
            pilih = input("> ")

            if pilih == "1":
                self.slot_1()
            elif pilih == "2":
                self.slot_2()
            elif pilih == "3":
                self.slot_3()
            elif pilih == "4":
                self.slot_4()
            elif pilih == "0":
                return
            else:
                continue

    def slot_info(self, index):
        crop = self.farm.slots[index]
        if crop is not None:
            ready = "Siap panen!" if crop.is_ready() else f"Belum siap ({crop.crop_age}/{crop.grow_time.get(crop.name)} hari)"
            watered = "Sudah disiram" if crop.watered_today else "Belum disiram"
            print(f"Tanaman yang ditanam: {crop.name}")
            print(f"Sudah siap panen? {ready}")
            print(f"Status siram: {watered}")
        else:
            print("Tanaman yang ditanam: Kosong")
            print(f"Sudah siap panen? -")

    def slot_1(self):
        while True:
            os.system("cls")
            print("===============Slot 1===============")
            self.slot_info(0)
            print("====================================")
            print("1. Tanam\n2. Panen\n3. Siram\n0. Kembali?")
            print("====================================")
            pilih = input("> ")

            if pilih == "1":
                self.farm.plant(0)
                break
            elif pilih == "2":
                self.farm.panen(0)
                break
            elif pilih == "3":
                self.farm.water(0)
                break
            elif pilih == "0":
                return
            else:
                continue

    def slot_2(self):
        while True:
            os.system("cls")
            print("==========Slot 2==========")
            self.slot_info(1)
            print(f"Sudah siap panen?\t ")
            print("==========================")
            print("1. Tanam\n2. Panen\n3. Siram\n0. Kembali?")
            print("==========================")
            pilih = input("> ")

            if pilih == "1":
                self.farm.plant(1)
                break
            elif pilih == "2":
                self.farm.panen(1)
                break
            elif pilih == "3":
                pass
            elif pilih == "0":
                return
            else:
                continue

    def slot_3(self):
        while True:
            os.system("cls")
            print("==========Slot 3==========")
            self.slot_info(2)
            print(f"Sudah siap panen?\t ")
            print("==========================")
            print("1. Tanam\n2. Panen\n3. Siram\n0. Kembali?")
            print("==========================")
            pilih = input("> ")

            if pilih == "1":
                self.farm.plant(2)
                break
            elif pilih == "2":
                self.farm.panen(2)
                break
            elif pilih == "3":
                pass
            elif pilih == "0":
                return
            else:
                continue

    def slot_4(self):
        while True:
            os.system("cls")
            print("==========Slot 4==========")
            self.slot_info(3) 
            print(f"Sudah siap panen?\t ")
            print("==========================")
            print("1. Tanam\n2. Panen\n3. Siram\n0. Kembali?")
            print("==========================")
            pilih = input("> ")

            if pilih == "1":
                self.farm.plant(3)
                break
            elif pilih == "2":
                self.farm.panen(3)
                break
            elif pilih == "3":
                pass
            elif pilih == "0":
                return
            else:
                continue
    
game = Game()
farm = Farm()