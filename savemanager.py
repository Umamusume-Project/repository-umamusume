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

        with open(file_path, 'r') as file:
            lines = file.readlines()

            for line in lines:
                line = line.strip()
                if line == '':
                    continue
                if line == 'farm':
                    farm_section = True
                    continue
                if not farm_section:
                    parts = line.split('=')
                    if len(parts) == 2:
                        key, value = parts
                        try:
                            data[key] = int(value)
                        except ValueError:
                            data[key] = value
                else:
                    farm_data.append(line)

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
            