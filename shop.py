import os
import status
import inventory

class Warung:
    def __init__(self):
        self.items = {
            'Benih Wheat' : 20,
            'Benih Sawit' : 45,
            'Benih Ganja' : 100,
            'Benih Tembakau' : 60,
            'Benih Jagung' : 30
        }
        
    def beli(self, item, jumlah):
            if item == '1':
                total = self.items['Benih Wheat'] * int(jumlah)
                if status.uang.cek() >= total:
                    inventory.inventory.tambah_barang('Benih Wheat', int(jumlah), 'benih')
                    status.uang.kurangi_uang(total)
                    print("====================================")
                    print(f'Anda membeli {jumlah} Biji Wheat!')
                    print(f'Total biaya: {total} duit')
                    print(f'Sisa uang: {status.uang.cek()} duit')
                    input('')
                else:
                    print('Uang tidak cukup untuk membeli Biji Wheat.')
                    input('')

            elif item == '2':
                total = self.items['Benih Sawit'] * int(jumlah)
                if status.uang.cek() >= total:
                    inventory.inventory.tambah_barang('Benih Sawit', int(jumlah), 'benih')
                    status.uang.kurangi_uang(total)
                    print("====================================")
                    print(f'Anda membeli {jumlah} Biji Sawit!')
                    print(f'Total biaya: {total} duit')
                    print(f'Sisa uang: {status.uang.cek()} duit')
                    input('')
                else:
                    print('Uang tidak cukup untuk membeli Biji Sawit.')
                    input('')

            elif item == '3':
                total = self.items['Benih Ganja'] * int(jumlah)
                if status.uang.cek() >= total:
                    inventory.inventory.tambah_barang('Benih Ganja', int(jumlah), 'benih')
                    status.uang.kurangi_uang(total)
                    print("====================================")
                    print(f'Anda membeli {jumlah} Biji Ganja!')
                    print(f'Total biaya: {total} duit')
                    print(f'Sisa uang: {status.uang.cek()} duit')
                    input('')
                else:
                    print('Uang tidak cukup untuk membeli Biji Ganja.')
                    input('')

            elif item == '4':
                total = self.items['Benih Tembakau'] * int(jumlah)
                if status.uang.cek() >= total:
                    inventory.inventory.tambah_barang('Benih Tembakau', int(jumlah), 'benih')
                    status.uang.kurangi_uang(total)
                    print("====================================")
                    print(f'Anda membeli {jumlah} Biji Tembakau!')
                    print(f'Total biaya: {total} duit')
                    print(f'Sisa uang: {status.uang.cek()} duit')
                    input('')
                else:
                    print('Uang tidak cukup untuk membeli Biji Tembakau.')
                    input('')

            elif item == '5':
                total = self.items['Benih Jagung'] * int(jumlah)
                if status.uang.cek() >= total:
                    inventory.inventory.tambah_barang('Benih Jagung', int(jumlah), 'benih')
                    status.uang.kurangi_uang(total)
                    print(f'Anda membeli {jumlah} Biji Jagung!')
                    print(f'Total biaya: {total} duit')
                    print(f'Sisa uang: {status.uang.cek()} duit')
                    input('')
                else:
                    print('Uang tidak cukup untuk membeli Biji Jagung.')
                    input('')

    def jualItem(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('==================')
        print('   Jual Barang')
        print('==================')
        print('')
        inventory.inventory.tampilkan_barang()
        print('')
        print('==================')


    def toko(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('==================')
            print('       Toko')
            print('==================')
            print('')
            for idx, (item, price) in enumerate(self.items.items(), start=1):
                print(f'{idx}. {item} ({price} duit)')
            print('6. Jual Barang')
            print('==================')
            print('0. Kembali')
            print('Masukkan pilihanmu:')
            jawaban = input('> ')
            if jawaban == '0':
                break
            elif jawaban == '6':
                self.jualItem()
            elif jawaban in ['1', '2', '3', '4', '5']:
                try:
                    jumlah = int(input('Masukkan jumlah yang ingin dibeli: '))
                    self.beli(jawaban, jumlah)
                except ValueError:
                    print('Input tidak valid.')
                    input('')
            else:
                print('Pilihan tidak valid.')
                input('Tekan Enter untuk melanjutkan...')
            
shop = Warung()