import random

player = {
    "uang": 50,
    "stamina": 100,
    "inventory": {}
}

max_slot_inventory = 18
max_stack = 36

def tambah_barang(nama_barang, jumlah, tipe):
    inv = player["inventory"]

    if nama_barang in inv:
        if inv[nama_barang]["jumlah"] + jumlah <= max_stack:
            inv[nama_barang]["jumlah"] += jumlah
        else:
            print("Stack penuh!")
            return
    else:
        if len(inv) < max_slot_inventory:
            inv[nama_barang] = {
                "jumlah": jumlah,
                "tipe": tipe
            }
        else:
            print("Inventory penuh!")
            return

    print(f"{jumlah} {nama_barang} masuk inventory!")

def lihat_inventory():
    inv = player["inventory"]

    if not inv:
        print("\nInventory kosong!\n")
    else:
        print("\n===== INVENTORY =====")
        for barang, data in inv.items():
            print(f"{barang} ({data['tipe']}) : {data['jumlah']}")
        print("=====================\n")


farm_slots = [None, None, None, None]

def farming():
    while True:
        print("\n==== FARMING ====")
        print("Pilih Slot:")
        for i in range(4):
            isi = farm_slots[i] if farm_slots[i] else "Kosong"
            print(f"{i+1}. Slot {i+1} - {isi}")
        print("0. Kembali")

        pilih = input("> ")

        if pilih == "0":
            break

        index = int(pilih) - 1

        print("\n1. Tanam Wheat")
        print("2. Panen")
        print("0. Kembali")
        aksi = input("> ")

        if aksi == "1":
            if farm_slots[index] is None:
                farm_slots[index] = "Wheat"
                print("Wheat berhasil ditanam!")
            else:
                print("Slot sudah terisi!")

        elif aksi == "2":
            if farm_slots[index] is not None:
                hasil = farm_slots[index]
                print(f"{hasil} berhasil dipanen!")
                tambah_barang(hasil, 1, "hasil")
                farm_slots[index] = None
            else:
                print("Slot kosong!")


def mining():
    if player["stamina"] < 10:
        print("Stamina tidak cukup!")
        return

    hasil_tambang = ["Batu", "Besi", "Emas"]
    hasil = random.choice(hasil_tambang)

    print(f"Kamu mendapatkan {hasil}!")
    tambah_barang(hasil, 1, "material")
    player["stamina"] -= 10

def shop():
    print("\n==== SHOP ====")
    print("1. Beli Potion (20 duit)")
    print("0. Kembali")

    pilih = input("> ")

    if pilih == "1":
        if player["uang"] >= 20:
            player["uang"] -= 20
            tambah_barang("Potion", 1, "item")
        else:
            print("Uang tidak cukup!")
            
while True:
    print("\n===== MENU =====")
    print(f"Uang: {player['uang']}")
    print(f"Stamina: {player['stamina']}")
    print("1. Farming")
    print("2. Mining")
    print("3. Shop")
    print("4. Inventory")
    print("0. Keluar")

    pilih = input("> ")

    if pilih == "1":
        farming()
    elif pilih == "2":
        mining()
    elif pilih == "3":
        shop()
    elif pilih == "4":
        lihat_inventory()
    elif pilih == "0":
        break