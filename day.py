import os
import status
import savemanager
import farming


def hari():
    savemanager.savemanager.load()
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
        farming.game.farmMenu()
    elif kegiatan == '2':
        from mining import main_menu
        main_menu()
    elif kegiatan == '3':
        from shop import Warung
        Warung().toko()
        hari()
    elif kegiatan == '4':
        from inventory import inventory
        inventory.menu()
        hari()
    elif kegiatan == '5':
        savemanager.savemanager.save()
        tidur()
    elif kegiatan == '6':
        savemanager.savemanager.reset()
        print('Data save telah direset.')
        input('Tekan Enter untuk melanjutkan...')
        hari()

    else:
        print('Pilihan tidak valid')
        input('Tekan Enter untuk melanjutkan...')
        hari()
    return

def tidur():
        os.system('cls' if os.name == 'nt' else 'clear')
        print('=================================')
        print('kamu tidur dan memulihkan stamina')
        print('=================================')
        print('')
        input('tekan enter untuk melanjutkan...')
        from farming import game
        game.farm.next_day()
        status.Status.ganti_day()
        from day import hari
        hari()

hari()
