import os
import status
import farming
import inventory

file_path = 'save.txt'

class Savemanager:

    @staticmethod
    def reset(game):
        status.Status.day = 1
        status.Status.stamina = 100
        status.Status.max_stamina = 100
        status.uang.saldo = 45
        Savemanager.save(game)
        

    @staticmethod
    def save(game):
        with open(file_path, 'w') as file:
            file.write(f'day={status.Status.day}\n')
            file.write(f'stamina={status.Status.stamina}\n')
            file.write(f'max_stamina={status.Status.max_stamina}\n')
            file.write(f'uang={status.uang.saldo}\n')
            file.write('\ninventory\n') 
            for nama_barang, data in game.inventory.inventory.items():
                file.write(f'{nama_barang}, {data["jumlah"]}, {data["tipe"]}\n')
            file.write('\nfarm\n')
            for crop in game.farm.slots:
                if crop is None:
                    file.write("none\n")
                else:
                    file.write(f'{crop.name}, {crop.crop_age}, {crop.watered_today}\n')

    @staticmethod
    def load(game):
        data = {}
        farm_section = False
        farm_data = []
        inventory_section = False
        if not os.path.exist(file_path):
            Savemanager.save(game)
            print('savedata baru sudah dibuat')
            return

        with open(file_path, 'r') as file:
            lines = file.readlines()
            game.inventory.inventory = {}

            for line in lines:
                line = line.strip()
                if line == '':
                    continue
                if line == 'inventory':
                    inventory_section = True
                    farm_section = False
                    continue
                if line == 'farm':
                    farm_section = True
                    inventory_section = False
                    continue
                # baca data
                if inventory_section:
                    nama_barang, jumlah, tipe = line.split(', ')
                    game.inventory.inventory[nama_barang] = {
                        'jumlah': int(jumlah),
                        'tipe': tipe
                    }
                    continue
                elif farm_section:
                    farm_data.append(line)
                    continue
                part = line.split('=')
                if len(part) == 2:
                    key, value = part
                    try:
                        data[key] = int(value)
                    except ValueError:
                        data[key] = value

            #set data
            if 'day' in data and 'stamina' in data and 'max_stamina' in data:
                status.Status.set(
                    data['day'],
                    data['stamina'],
                    data['max_stamina']
                )
            if 'uang' in data:
                try:
                    status.uang.set(int(data['uang']))
                except Exception:
                    status.uang.set(data['uang'])

            for i in range(4):
                if farm_data[i] == 'none':
                    game.farm.slots[i] = None
                else:
                    nama, umur, watered = farm_data[i].split(', ')
                    crop = farming.Crop(nama)
                    crop.crop_age = int(umur)
                    crop.watered_today = watered == 'True'
                    game.farm.slots[i] = crop
            