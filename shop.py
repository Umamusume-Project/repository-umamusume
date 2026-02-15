import os
import status

class Warung:
    def __init__(self):
        self.wheat = 20
        self.sawit = 45
        self.ganja = 100
        self.Biji = 60
    def beli(self, item):
            if item == '1':
                if status.uang.cek() >= self.wheat:
                    status.uang.kurangi_uang(self.wheat)
                    print('Anda membeli Biji Wheat!')
                else:
                    print('Uang tidak cukup untuk membeli Biji Wheat.')
            elif item == '2':
                if status.uang.cek() >= self.sawit:
                    status.uang.kurangi_uang(self.sawit)
                    print('Anda membeli Biji Sawit!')
                else:
                    print('Uang tidak cukup untuk membeli Biji Sawit.')
            elif item == '3':
                if status.uang.cek() >= self.ganja:
                    status.uang.kurangi_uang(self.ganja)
                    print('Anda membeli Biji Ganja!')
                else:
                    print('Uang tidak cukup untuk membeli Biji Ganja.')
            elif item == '4':
                if status.uang.cek() >= self.Biji:
                    status.uang.kurangi_uang(self.Biji)
                    print('Anda membeli Biji Biji!')
                else:
                    print('Uang tidak cukup untuk membeli Biji Biji.')
            else:
                print('Pilihan tidak valid.')

    def toko(self):
            os.system('cls' if os.name == 'nt' else 'clear')
            print('==================')
            print('       Toko')
            print('==================')
            print('')
            print('1. Biji wheat (20)')
            print('2. Biji Sawit (45)')
            print('3. Biji Ganja (100)')
            print('4. Biji Biji (60)')
            print('0. Kembali')
            print('Masukkan pilihanmu:')
            jawaban = input('> ')
            from day import hari
            if jawaban == '0':
                hari()
            elif jawaban in ['1', '2', '3', '4']:
                self.beli(jawaban)
                input('Tekan Enter untuk melanjutkan...')
                self.toko()
            else:
                print('Pilihan tidak valid.')
                input('Tekan Enter untuk melanjutkan...')
                self.toko()
            