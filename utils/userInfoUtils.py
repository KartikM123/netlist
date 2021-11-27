import json
#globals
TAGGING_TRAITS = ["priority"] #used to pair lists of items
ID_TRAITS = ["name"] #used to pin down unique identifiers
#general util for interacting with userinfo
def readFileData():
    with open('db/network.json', 'r+') as outfile:
        file_data = json.load(outfile)
        return file_data
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
    file_data = readFileData()
    for trait in file_data["userTraits"]:
        userInfo.traits[trait] = d[trait]
    return userInfo
def prebuiltTrait(s):
    return (s == "name") or (s == "priority") or (s == "timeAdded") or (s == "timePinged")
#userinfo class intended to be used for control manipulation
class UserInfo(object):
    def __init__(self):
        self.name = ""
        self.priority = 1000
        self.traits = {}
        file_data = readFileData()
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