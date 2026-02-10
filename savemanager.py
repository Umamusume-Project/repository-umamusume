import os
import status

file_path = 'save.txt'

class savemanager:

    @staticmethod
    def reset():
        status.Status.day = 1
        status.Status.stamina = 100
        status.Status.max_stamina = 100
        status.uang.saldo = 45
        savemanager.save()
        

    @staticmethod
    def save():
        with open(file_path, 'w') as file:
            file.write(f'day={status.Status.day}\n')
            file.write(f'stamina={status.Status.stamina}\n')
            file.write(f'max_stamina={status.Status.max_stamina}\n')
            file.write(f'uang={status.uang.saldo}\n')

    @staticmethod
    def load():
        data = {}
        if not os.path.exists(file_path):
            savemanager.reset()
            return
        with open(file_path, 'r') as file:
          for line in file:
              key, value = line.strip().split('=')
              data[key] = int(value)
        status.Status.set(
            data['day'],
            data['stamina'],
            data['max_stamina']
        )
        status.uang.set(data['uang'])

      
         
