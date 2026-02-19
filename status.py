class uang:
    saldo = 45
    
    @staticmethod
    def set(jumlah):
        uang.saldo = jumlah
    
    @staticmethod
    def tambah_uang(jumlah):
        uang.saldo += jumlah
    
    @staticmethod
    def kurangi_uang(jumlah):
        if uang.saldo >= jumlah:
            uang.saldo -= jumlah
            return True
        else:
            print('Uang tidak cukup!')
            return False
    
    @staticmethod
    def cek():
        return uang.saldo

class Status:
    day = 1
    stamina = 100
    max_stamina = 100
    
    @staticmethod
    def kurangi_stamina(jumlah):
        if Status.stamina >= jumlah:
            Status.stamina -= jumlah
        else:
            print('Stamina tidak cukup!')
    
    @staticmethod
    def ganti_day():
        Status.day += 1
        Status.stamina = Status.max_stamina
    
    @staticmethod
    def cek_status():
        return Status.day, Status.stamina, Status.max_stamina
    
    @staticmethod
    def set(day, stamina, max_stamina):
        Status.day = day
        Status.stamina = stamina
        Status.max_stamina = max_stamina
