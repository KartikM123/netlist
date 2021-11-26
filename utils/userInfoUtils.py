import json
def printUserInfo(u):
    print("name: " + u.name)
    for trait in u.traits:
        print(trait + ": " + u.traits[trait])
    print("priority: " + u.priority)
    return
def dictToUserInfo(d):
    userInfo = UserInfo()
    userInfo.name = d["name"]
    userInfo.priority = d["priority"]
    with open('db/network.json', 'r+') as outfile:
        file_data = json.load(outfile)
        for trait in file_data["userTraits"]:
            userInfo.traits[trait] = d[trait]
    return userInfo
def prebuiltTrait(s):
    return (s == "name") or (s == "priority") or (s == "timeAdded") or (s == "timePinged")
class UserInfo(object):
    def __init__(self):
        self.name = ""
        self.priority = 1000
        self.traits = {}
        with open('db/network.json', 'r+') as outfile:
            file_data = json.load(outfile)
            for trait in file_data["userTraits"]:
                if not prebuiltTrait(trait):
                    self.traits[trait] = ""
    def serialize(self):
        obj = {}
        obj["name"] = self.name
        obj["priority"] = self.priority
        for trait in self.traits:
            obj[trait] = self.traits[trait]
        return obj