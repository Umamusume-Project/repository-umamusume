import os
import status
import savemanager
import farming

farm = farming.Game()

def hari():
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
    print('4. tidur (ganti hari, pulihkan stamina, dan simpan game)')
    print('5. reset game (hapus data save)')
    print('Masukkan pilihanmu:')
    kegiatan = input('> ')

    if kegiatan == '1':
        farm.farmMenu()
    elif kegiatan == '2':
        from mining import main_menu
        main_menu()
    elif kegiatan == '3':
        from shop import Warung
        Warung().toko()
    elif kegiatan == '4':
        savemanager.savemanager.save()
        tidur()
    elif kegiatan == '5':
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
        status.Status.ganti_day()
        from day import hari
        hari()

hari()
