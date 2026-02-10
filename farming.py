import os
import status

from status import Status
from status import uang
status = Status()
duit = uang()

class Player:
    def __init__(self):
        self.day = status.day
        self.stamina = status.stamina
        self.maxstamina = status.max_stamina
        self.uang = duit.saldo
        self.crops = ["wheat", "sawit", "ganja", "balls"]

class Farm:
    def __init__(self):
        self.slots = [None, None, None, None]
        self.player = Player()

    def plant(self, index):
        if self.slots[index] is None:
            print("\nPilih Tanaman:")
            print(f"1. {self.player.crops[0]}\n2. {self.player.crops[1]}\n3. {self.player.crops[2]}\n4. {self.player.crops[3]}")
            print("====================")
            pilih = input("> ")

            if pilih == "1":
                idx = int(pilih) - 1
                self.slots[index] = self.player.crops[idx]
                print(f"{self.player.crops[idx]} Berhasil ditanam!")
                input("Enter untuk kembali...")

            elif pilih == "2":
                idx = int(pilih) - 1
                self.slots[index] = self.player.crops[idx]
                print(f"{self.player.crops[idx]} Berhasil ditanam!")
                input("Enter untuk kembali...")

            elif pilih == "3":
                idx = int(pilih) - 1
                self.slots[index] = self.player.crops[idx]
                print(f"{self.player.crops[idx]} Berhasil ditanam!")
                input("Enter untuk kembali...")

            elif pilih == "4":
                idx = int(pilih) - 1
                self.slots[index] = self.player.crops[idx]
                print(f"{self.player.crops[idx]} Berhasil ditanam!")
                input("Enter untuk kembali...")

        else:
            print("Lahan sudah terisi!")
            input("Enter untuk kembali...")

class Game:
    def __init__(self):
        self.running = True
        self.player = Player()
        self.farm = Farm()

    def farmMenu(self):
        os.system("cls")
        print("==========Farm Game==========")
        print(f"day\t:{self.player.day}")
        print(f"duit\t:{self.player.uang}")
        print(f"stamina\t:{self.player.stamina}")
        print("=============================")
        print("1. Pilih Lahan\n2. Inventory\n3. Shop")
        print("=============================")
        print("0. Kembali?")
        pilih = input("> ")

        if pilih == "1":
            self.slot_tanam()
        elif pilih == "2":
            pass
        elif pilih == "3":
            pass

    def slot_tanam(self):
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

    def slot_1(self):
        os.system("cls")
        print("==========Slot 1==========")
        if not(self.farm.slots[0]  == None):
            print(f"Tanaman yang ditanam: {self.farm.slots[0]}")
        else:
            print("Tanaman yang ditanam: Kosong")
        
        print(f"Sudah siap panen?\t ")
        print("==========================")
        print("1. Tanam\n2. Panen\n3. Siram\n0. Kembali?")
        print("==========================")
        pilih = input("> ")

        if pilih == "1":
            idx = int(pilih) - 1
            self.farm.plant(idx)
        elif pilih == "2":
            pass
        elif pilih == "3":
            pass
        elif pilih == "0":
            self.slot_tanam()

    def slot_2(self):
        os.system("cls")
        print("==========Slot 2==========")
        if not(self.farm.slots[1]  == None):
            print(f"Tanaman yang ditanam: {self.farm.slots[1]}")
        else:
            print("Tanaman yang ditanam: Kosong")
        
        print(f"Sudah siap panen?\t ")
        print("==========================")
        print("1. Tanam\n2. Panen\n3. Siram\n0. Kembali?")
        print("==========================")
        pilih = input("> ")

        if pilih == "1":
            idx = int(pilih)
            self.farm.plant(idx)
        elif pilih == "2":
            pass
        elif pilih == "3":
            pass
        elif pilih == "0":
            self.slot_tanam()

    def slot_3(self):
        os.system("cls")
        print("==========Slot 3==========")
        if not(self.farm.slots[2]  == None):
            print(f"Tanaman yang ditanam: {self.farm.slots[2]}")
        else:
            print("Tanaman yang ditanam: Kosong")
        
        print(f"Sudah siap panen?\t ")
        print("==========================")
        print("1. Tanam\n2. Panen\n3. Siram\n0. Kembali?")
        print("==========================")
        pilih = input("> ")

        if pilih == "1":
            idx = int(pilih) + 1
            self.farm.plant(idx)
        elif pilih == "2":
            pass
        elif pilih == "3":
            pass
        elif pilih == "0":
            self.slot_tanam()

    def slot_4(self):
        os.system("cls")
        print("==========Slot 4==========")
        if not(self.farm.slots[3]  == None):
            print(f"Tanaman yang ditanam: {self.farm.slots[3]}")
        else:
            print("Tanaman yang ditanam: Kosong")
        
        print(f"Sudah siap panen?\t ")
        print("==========================")
        print("1. Tanam\n2. Panen\n3. Siram\n0. Kembali?")
        print("==========================")
        pilih = input("> ")

        if pilih == "1":
            idx = int(pilih) + 2
            self.farm.plant(idx)
        elif pilih == "2":
            pass
        elif pilih == "3":
            pass
        elif pilih == "0":
            self.slot_tanam()
    
game = Game()

while game.running == True:
    game.farmMenu()