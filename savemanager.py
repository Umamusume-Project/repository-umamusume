import json
import os
import status
import uang

file_path = 'save.json'

class savemanager:

    @staticmethod
    def reset():
        data = {
            'day': 1,
            'stamina': 100,
            'max_stamina': 100,
            'uang': 45
        }
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        status.Status.set(1, 100, 100)
        uang.uang.set(45)
        

    @staticmethod
    def save():
        data ={
            'day': status.Status.day,
            'stamina': status.Status.stamina,
            'max_stamina': status.Status.max_stamina,
            'uang':uang.uang.saldo
        }
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load():
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                status.Status.set(
                    data['day'],
                    data['stamina'],
                    data['max_stamina']
                )
                uang.uang.set(data['uang'])
        else:
            savemanager.reset()

    
         
