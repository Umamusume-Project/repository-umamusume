import os

class Inventory:
    def __init__(self):
        self.inventory = {}
        self.max_slot = 18
        self.max_stack = 36

    def tambah_barang(self, nama_barang, jumlah, tipe):
        if nama_barang in self.inventory:
            if self.inventory[nama_barang]["jumlah"] + jumlah <= self.max_stack:
                self.inventory[nama_barang]["jumlah"] += jumlah
            else:
                print("Stack penuh!")
                return
        else:
            if len(self.inventory) < self.max_slot:
                self.inventory[nama_barang] = {
                    "jumlah": jumlah,
                    "tipe": tipe
                }
            else:
                print("Inventory penuh!")
                return
            
    def lihat_inventory(self):
            if not self.inventory:
                print("\nInventory kosong!\n")
            else:
                print("\n===== INVENTORY =====")
                for barang, data in self.inventory.items():
                    print(f"{barang} ({data['tipe']}) : {data['jumlah']}")
            print("=====================\n")
            input('')

    def menu(self):
        while True:
            os.system('cls')
            print("===== INVENTORY MENU =====")
            print("1. Lihat Inventory")
            print("0. Kembali")
            print("==========================")
            pilih = input("> ")

            if pilih == "1":
                self.lihat_inventory()
            elif pilih == "0":
                break

