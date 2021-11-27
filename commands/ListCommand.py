from commands.ICommand import ICommand, format
import json
from datetime import datetime
from utils.commandLineUtils import readFileData
class ListCommand(ICommand):
    def __init__(self, args, opts):
        pass
    def calcTimeSincePinged(self, data):
        newArr = []
        for user in data:
            timePinged = user["timePinged"]
            nowTime = str(datetime.now().strftime(format))
            user["timeSinceLastPinged"] = str(datetime.strptime(nowTime, format) - datetime.strptime(timePinged, format))
            newArr.append(user)
        return newArr
    def sortTime(self, data):
        print(data.sort(key=lambda x: x["timeSinceLastPinged"], reverse=True))
        return data
    def prettyPrint(self, data):
        for obj in data:
            print(obj["name"] + " : " +  obj["timeSinceLastPinged"])
    def execute(self):
        fileData = readFileData()["network"]
        fileData = self.calcTimeSincePinged(fileData)
        self.prettyPrint(self.sortTime(fileData))