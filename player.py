from inventory import Inventory

class Player:
    def __init__(self):
        self.uang = 45
        self.day = 1
        self.max_stamina = 20
        self.stamina = self.max_stamina
        self.inventory = Inventory()
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
        self.stamina = max(0, self.stamina - jumlah)
        if self.stamina == 0:
            print("Stamina kamu habis total!")

    def ganti_day(self):
        self.day += 1
        self.stamina = self.max_stamina

    def to_dict(self):
        return {
            'uang': self.uang,
            'day': self.day,
            'stamina': self.stamina,
            'max_stamina': self.max_stamina,
            'mining_count': self.mining_count,
            'power': self.power,
            'defense': self.defense,
            'speed': self.speed,
            'inventory': self.inventory.to_dict()
        }
    
    def from_dict(self, data):
        self.uang = data['uang']
        self.day = data['day']
        self.stamina = data['stamina']
        self.max_stamina = data['max_stamina']
        self.mining_count = data.get('mining_count', 1)
        self.power = data.get('power', 1)
        self.defense = data.get('defense', 1)
        self.speed = data.get('speed', 1)
        self.inventory.from_dict(data.get('inventory', {}))
