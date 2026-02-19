import os
import status
import inventory

class Warung:
    def __init__(self, game):
        self.game = game
        self.items = {
            '1': {'nama': 'Benih Wheat',    'harga': 20},
            '2': {'nama': 'Benih Sawit',    'harga': 45},
            '3': {'nama': 'Benih Ganja',    'harga': 100},
            '4': {'nama': 'Benih Tembakau', 'harga': 60},
            '5': {'nama': 'Benih Jagung',   'harga': 30}
        }
        self.sell_prices = {
            # Hasil panen (farming)
            'Wheat': 35,
            'Sawit': 90,
            'Ganja': 200,
            'Tembakau': 90,
            'Jagung': 50,
            # Ore dari mining (tambah ini supaya bisa dijual)
            'Coal': 10,
            'Iron': 25,
            'Crystal': 40,
            'Emerald': 80,
            'Diamond': 150
        }
    
    # ------------------- Func Beli -------------------
    def beli(self, pilihan, jumlah):
        if pilihan not in self.items:
            print('Pilihan tidak valid.')
            input('')
            return
        
        item = self.items[pilihan]
        nama = item['nama']
        total = item['harga'] * jumlah
        
        if status.uang.cek() >= total:
            status.uang.kurangi_uang(total)
            self.game.inventory.tambah_barang(nama, jumlah, 'benih')
            print("====================================")
            print(f'Anda membeli {jumlah} {nama}!')
            print(f'Total biaya : {total} duit')
            print(f'Sisa uang   : {status.uang.cek()} duit')
        else:
            print(f'Uang tidak cukup untuk membeli {nama}.')
        input('')
    
    # ------------------- Func Jual -------------------
    def jualItem(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('==================')
        print('   Jual Barang')
        print('==================')
        print('')
        
        # Tampilkan barang tipe 'hasil panen' ATAU 'ore'
        list_barang = [
            (nama, data) for nama, data in self.game.inventory.inventory.items()
            if data.get('tipe') in ['hasil panen', 'ore']
        ]
        
        if not list_barang:
            print('Tidak ada barang yang bisa dijual (hasil panen / ore).')
            input('')
            return
        
        for idx, (nama, data) in enumerate(list_barang, start=1):
            harga_per_unit = self.sell_prices.get(nama, 0)
            total_harga = harga_per_unit * data['jumlah']
            print(f"{idx}. {nama} ({data['tipe']}) : {data['jumlah']} tersedia (Harga jual: {total_harga} duit)")
        
        print('')
        print('==================')
        pilih = input('Masukkan nomor barang yang ingin dijual: ')
        
        try:
            idx = int(pilih) - 1
            if 0 <= idx < len(list_barang):
                jumlah = int(input('Masukkan jumlah yang ingin dijual: '))
                selected_nama, selected_data = list_barang[idx]
                stok_tersedia = selected_data['jumlah']
                
                if jumlah <= 0 or jumlah > stok_tersedia:
                    print('Jumlah tidak valid atau melebihi stok.')
                    input('')
                    return
                
                harga_jual = self.sell_prices.get(selected_nama, 0) * jumlah
                
                status.uang.tambah_uang(harga_jual)
                self.game.inventory.inventory[selected_nama]['jumlah'] -= jumlah
                
                if self.game.inventory.inventory[selected_nama]['jumlah'] <= 0:
                    del self.game.inventory.inventory[selected_nama]
                
                print(f'Anda menjual {jumlah} {selected_nama} seharga {harga_jual} duit!')
                print(f'Saldo saat ini: {status.uang.cek()} duit')
            else:
                print('Pilihan tidak valid.')
        except ValueError:
            print('Input tidak valid.')
        
        input('Tekan Enter untuk melanjutkan...')
    
    # ------------------- UI -------------------
    def menu_toko(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('==================')
        print('       Toko')
        print('==================')
        print('')
        for pilihan, data in self.items.items():
            print(f"{pilihan}. {data['nama']} ({data['harga']} duit)")
        print('6. Jual Barang')
        print('==================')
        print('0. Kembali')
        print('Masukkan pilihanmu:')
    
    # ---------------- Main --------------------
    def toko(self):
        while True:
            self.menu_toko()            
            jawaban = input('> ')
            if jawaban == '0':
                break
            elif jawaban == '6':
                self.jualItem()
            elif jawaban in self.items:
                try:
                    jumlah = int(input('Masukkan jumlah yang ingin dibeli: '))
                    if jumlah <= 0:
                        print('Jumlah harus lebih dari 0.')
                        input('')
                        continue
                    else:
                        self.beli(jawaban, jumlah)
                except ValueError:
                    print('Input tidak valid.')
                    input('')
            else:
                print('Pilihan tidak valid.')
                input('Tekan Enter untuk melanjutkan...')
