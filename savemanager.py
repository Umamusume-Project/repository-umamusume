import os
import player
import farming

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'save.txt')

class Savemanager:
    @staticmethod
    def reset(farm, player):
        player.day = 1
        player.uang = 45
        player.stamina = 20
        player.max_stamina = 20
        player.inventory.items.clear()
        farm.slots = [None] * 4
        Savemanager.save(farm)
    
    @staticmethod
    def save(farm):
        with open(file_path, 'w') as file:
            file.write(f'day={player.day}\n')
            file.write(f'stamina={player.stamina}\n')
            file.write(f'max_stamina={player.max_stamina}\n')
            file.write(f'uang={player.uang}\n')
            file.write('\ninventory\n')
            for nama_barang, data in player.inventory.items.items():
                file.write(f'{nama_barang}, {data["jumlah"]}, {data["tipe"]}\n')
            file.write('\nfarm\n')
            for crop in farm.slots:
                if crop is None:
                    file.write("None\n")
                else:
                    file.write(f'{crop.name}, {crop.crop_age}, {crop.watered_today}\n')
    
    @staticmethod
    def load(player, farm):
        if not os.path.exists(file_path):
            return
        
        data = {}
        farm_section = False
        farm_data = []
        inventory_section = False
        
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line == '':
                    continue
                if line == '[inventory]':
                    inventory_section = True
                    farm_section = False
                    continue
                elif line == '[farm]':
                    farm_section = True
                    inventory_section = False
                    continue
                elif '=' in line:
                    key, value = line.split('=')
                    if key == 'day':
                        player.day = int(value)
                    elif key == 'stamina':
                        player.stamina = int(value)
                    elif key == 'max_stamina':
                        player.max_stamina = int(value)
                    elif key == 'uang':
                        player.uang = int(value)
                    
                if inventory_section == True:
                    nama, jumlah, tipe = line.split(',')
                    player.inventory.items[nama] = {
                        'jumlah': int(jumlah),
                        'tipe': tipe
                    }
                if farm_section == True:            
                    for i in range(min(4, len(farm_data))):
                        if farm_data[i] == 'none':
                            farm.slots[i] = None
                        else:
                            nama, umur, watered = farm_data[i].split(', ')
                            crop = farming.Crop(nama.strip())
                            crop.crop_age = int(umur)
                            crop.watered_today = watered.strip() == 'True'
                            farm.slots[i] = crop
