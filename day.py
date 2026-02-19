import os
import status
from savemanager import Savemanager
from farming import Game

game = Game()
Savemanager.load(game)

def hari():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        day, stamina, max_stamina = status.Status.cek_status()
        print('================')
        print('     projek   ')
        print('================')
        print('')
        print(f'    Day {day}')
        print(f'Uang kamu: {status.uang.cek()}')          
        print(f'stamina: {stamina}/{max_stamina}')
        print('')
        print('Pilih kegiatan')
        print('1. farming')
        print('2. mining')
        print('3. shop')
        print('4. inventory')
        print('5. tidur (ganti hari, pulihkan stamina, dan simpan game)')
        print('6. reset game (hapus data save)')
        print('Masukkan pilihanmu:')
        kegiatan = input('> ')

        if kegiatan == '1':
            game.farmMenu()
        elif kegiatan == '2':
            from mining import main_menu
            main_menu(game)
        elif kegiatan == '3':
            from shop import Warung
            game.shop.toko()
        elif kegiatan == '4':
            from inventory import Inventory
            game.inventory.menu()
        elif kegiatan == '5':
            Savemanager.save(game)
            tidur()
        elif kegiatan == '6':
            Savemanager.reset(game)
            print('Data save telah direset.')
            input('Tekan Enter untuk melanjutkan...')
        else:
            print('Pilihan tidak valid')
            input('Tekan Enter untuk melanjutkan...')
        

def tidur():
        os.system('cls' if os.name == 'nt' else 'clear')
        print('=================================')
        print('kamu tidur dan memulihkan stamina')
        print('=================================')
        print('')
        input('tekan enter untuk melanjutkan...')
        game.farm.next_day()
        status.Status.ganti_day()

hari()

if __name__ == "__main__":
    hari()
