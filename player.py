from inventory import Inventory

class Player:
    def __init__(self):
        self.uang = 45
        self.day = 1
        self.stamina = 25
        self.max_stamina = 25
        self.inventory = Inventory()
        self.farm_slots = [None] * 4
        #STAT MINING (kent . . .)
        self.mining_count = 1
        self.power = 1
        self.defense = 1
        self.speed = 1

    def tambah_uang(self, jumlah):
        self.uang += jumlah

    def kurangi_uang(self, jumlah):
        if self.uang >= jumlah:
            self.uang -= jumlah
        else:
            print('Uang ga cukup!!')

    def kurangi_stamina(self, jumlah):
        if self.stamina >= jumlah:
            self.stamina -= jumlah
        else:
            print('stamina kurang!!')

    def ganti_day(self):
        self.day += 1
        self.stamina = self.max_stamina
