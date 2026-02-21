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

def ui():
    width = 55
    border = '=' * width
    print(border)
    print('Game Farming dan Mining'.center(width))
    print(border)
    print(f'Day {player.day}'.center(width))
    print(f'Uang kamu: {player.uang}'.center(width))
    print(f'Stamina: {player.stamina}/{player.max_stamina}'.center(width))
    print(border)
    print('Pilih kegiatan'.center(width))
    print(border)
    print('1. Farming\n2. Mining\n3. Shop\n4. Inventory\n5. Tidur (ganti hari, pulihkan stamina, dan simpan game)\n6. Reset game (hapus data save)\n0. Keluar dari program (tersimpan)')
    print(border)
    print('Masukkan pilihanmu:')

def main(player):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        ui()
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
