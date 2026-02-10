import os
import json
import savemanager

class uang:
    saldo = 45

    def set(jumlah):
        uang.saldo = jumlah

    def tambah_uang(jumlah):
        uang.saldo += jumlah

    def kurangi_uang(jumlah):
        if uang.saldo >= jumlah:
            uang.saldo -= jumlah
        else:
            print('uang tidak cukup!')
    def cek():
        return uang.saldo
    

class Status:
    day = 1
    stamina = 100
    max_stamina = 100
    
    def kurangi_stamina(jumlah):
        if Status.stamina >= jumlah:
            Status.stamina -= jumlah
        else:
            print('stamina tidak cukup!')

    def ganti_day():
        Status.day += 1
        Status.stamina = Status.max_stamina
    

    def cek_status():
        return Status.day, Status.stamina, Status.max_stamina

    def set(day, stamina, max_stamina):
        Status.day = day
        Status.stamina = stamina
        Status.max_stamina = max_stamina
