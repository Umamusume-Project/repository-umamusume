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
# mining = Mining(player, farm)
Savemanager.load(player, game.farm)

def hari(player):
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
        print('Masukkan pilihanmu:')
        kegiatan = input('> ')

        if kegiatan == '1':
            game.farmMenu(player, warung)
        elif kegiatan == '2':
            from mining import main_menu
            main_menu(farm, warung)
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

hari(player)

# if __name__ == "__main__":
#     hari()
