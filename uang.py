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
    
