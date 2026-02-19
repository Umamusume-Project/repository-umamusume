import os
import inventory
import status
from shop import Warung
from inventory import Inventory

class Player:
    def __init__(self):
        self.day, self.stamina, self.max_stamina = status.Status.cek_status()
        self.uang = status.uang.cek()

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
    def __init__(self, game):
        self.slots = [None, None, None, None]
        self.player = Player()
        self.game = game

    def plant(self, index):
        if self.slots[index] is None:
            benih_list = [(nama, data) 
                          for nama, data in self.game.inventory.inventory.items() 
                          if data.get('tipe') == 'benih']
            
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
                    
                    self.game.inventory.inventory[selected_crop]['jumlah'] -= 1
                    if self.game.inventory.inventory[selected_crop]['jumlah'] <= 0:
                        del self.game.inventory.inventory[selected_crop]
                    
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
        
        hasil = crop.name
        self.game.inventory.tambah_barang(hasil, 1, 'hasil panen')
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
        self.player = Player()
        self.farm = Farm(self)
        self.inventory = Inventory()
        self.shop = Warung(self)

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
                self.inventory.menu()
            elif pilih == "3":
                self.shop.toko()
            elif pilih == "0":
                return
            else:
                continue

    def slots(self, idx):
        while True:
            idx += 1
            crop = self.farm.slots[idx-1]
            if crop is None:
                ready = '-'
                crop_name = 'Kosong'
            else:
                ready = 'Siap panen!' if crop.is_ready() else f'Belum siap panen ({crop.crop_age}/{crop.grow_time[crop.name]})'
                crop_name = crop.name
            watered = "Sudah disiram" if crop and crop.watered_today else "Belum disiram"
            os.system("cls")
            print(f"==========Lahan {idx}==========")
            print(f'Tanaman yang ditanam: {crop_name}')
            print(f'Sudah siap panen? {ready}')
            print(f'Status: {watered}')
            print("========================")
            print("1. Tanam\n2. Panen\n3. Siram")
            print("========================")
            print("0. Kembali?")
            pilih = input("> ")

            if pilih == "1":
                self.farm.plant(idx-1)
                break
            elif pilih == "2":
                self.farm.panen(idx-1)
                break
            elif pilih == "3":
                self.farm.water(idx-1)
                break
            elif pilih == "0":
                return
            else:
                continue

    def slot_tanam(self):
        while True:
            os.system("cls")
            print("==========Slot==========")
            print("Pilih Lahan untuk Menanam")
            print("========================")
            print("1. Lahan #1\n2. Lahan #2\n3. Lahan #3\n4. Lahan #4")
            print("========================")
            print("0. Kembali?")
            pilih = input("> ")

            try:
                idx = int(pilih) - 1
                if 0 <= idx < len(self.farm.slots):
                    self.slots(idx)
                elif pilih == "0":
                    return
            except ValueError:
                print('Invalid Input!')
                input('')