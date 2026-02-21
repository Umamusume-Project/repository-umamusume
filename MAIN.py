import os
from player import Player
from savemanager import Savemanager
from shop import Warung
from inventory import Inventory
from mining import Mining
from farming import Game, Farm

player = Player()
game = Game(player)
farm = game.farm 
warung = Warung(player, farm)
mining = Mining(farm, player, warung, (1, 3))
Savemanager.load(player, game.farm)

def main(player):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('================')
        print('     projek   ')
        print('================')
        print('')
        print(f'    Day {player.day}')
        print(f'Uang kamu: {player.uang}')          
        print(f'stamina: {player.stamina}/{player.max_stamina}')
        print('')
        print('Pilih kegiatan')
        print('1. farming')
        print('2. mining')
        print('3. shop')
        print('4. inventory')
        print('5. tidur (ganti hari, pulihkan stamina, dan simpan game)')
        print('6. reset game (hapus data save)')
        print('0. Keluar dari program (tersimpan)')
        print('Masukkan pilihanmu:')
        kegiatan = input('> ')

        if kegiatan == '1':
            game.farmMenu(player, warung)
        elif kegiatan == '2':
            mining.main_menu()
        elif kegiatan == '3':
            warung.toko()
        elif kegiatan == '4':
            player.inventory.menu()
        elif kegiatan == '5':
            Savemanager.save(player, game.farm)
            tidur()
        elif kegiatan == '6':
            Savemanager.reset(game.farm, player)
            print('Data save telah direset.')
            input('Tekan Enter untuk melanjutkan...')
        elif kegiatan == '0':
            Savemanager.save(player, game.farm)
            print('Terima kasih telah bermain!')
            break
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
        player.ganti_day()

main(player)
