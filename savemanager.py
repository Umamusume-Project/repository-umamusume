import os
import json
import farming

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'save.json')

class Savemanager:
    @staticmethod
    def reset(farm, player):
        player.day = 1
        player.uang = 45
        player.stamina = 20
        player.max_stamina = 20
        player.inventory.items.clear()
        farm.slots = [None] * 4
        #mining
        player.mining_count = 1
        player.power = 1
        player.defense = 1
        player.speed = 1
        Savemanager.save(player, farm)
    
    @staticmethod
    def save(player, farm):
      data = {
          'player': player.to_dict(),
          'farm': farm.to_dict()
      }
      with open(file_path, 'w') as file:
          json.dump(data, file, indent=4)

    @staticmethod
    def load(player, farm):
        if not os.path.exists(file_path):
            return
        with open(file_path, 'r') as file:
            data = json.load(file)
            player.from_dict(data.get('player', {}))
            farm.from_dict(data.get('farm', {}))