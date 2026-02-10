import os
import status
import savemanager

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
    print('3. tidur (ganti hari dan pulihkan stamina)')
    print('4. reset game (hapus data save)')
    print('Masukkan pilihanmu:')
    kegiatan = input('> ')

    if kegiatan == '1':
        print('lorem ipsum')
    elif kegiatan == '2':
        print('Kamu memilih kegiatan 2')
    elif kegiatan == '3':
        savemanager.savemanager.save()
        tidur()
    elif kegiatan == '4':
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










