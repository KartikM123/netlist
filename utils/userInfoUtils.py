import json
class UserInfo(object):
    def __init__(self):
        self.name = ""
        self.priority = 1000
        self.traits = {}
        with open('db/network.json', 'r+') as outfile:
            file_data = json.load(outfile)
            for trait in file_data["userTraits"]:
                if not self.prebuiltTrait(trait):
                    self.traits[trait] = ""
    def prebuiltTrait(self, s):
        return (s == "name") or (s == "priority") or (s == "timeAdded") or (s == "timePinged")
    def serialize(self):
        obj = {}
        obj["name"] = self.name
        obj["priority"] = self.priority
        for trait in self.traits:
            obj[trait] = self.traits[trait]
        return obj