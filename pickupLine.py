import json

class PickupLines():
    
    def __init__(self):
        self.filename = 'pickuplines.json'
        self.pickuplines = self.loadPickupLines()
    
    def loadPickupLines(self):
        with open(self.filename, 'r') as fp:
            return json.load(fp)

    def getPickupLine(self, name: str):
        return self.pickuplines.get(name, None)





