from commands.ICommand import ICommand, format
from commands.SearchCommand import SearchCommand
import json
from datetime import datetime
import utils
class ListCommand(ICommand):
    def __init__(self, args, opts, tag):
        self.tag = tag
        pass
    def calcTimeSincePinged(self, data):
        newArr = []
        for user in data:
            timePinged = user["timePinged"]
            nowTime = str(datetime.now().strftime(format))
            user["timeSinceLastPinged"] = str(datetime.strptime(nowTime, format) - datetime.strptime(timePinged, format))
            newArr.append(user)
        return newArr
    def getUsersofTagged(self, tag):
        network = utils.userInfoUtils.readFileData()["network"]
        totalUsers = []
        for user in network:
            if tag in user["tags"]:
                totalUsers.append(user)
        return totalUsers
    def sortTime(self, data):
        data.sort(key=lambda x: x["timeSinceLastPinged"], reverse=False)
        return data
    def prettyPrint(self, data):
        for obj in data:
            print(obj["name"] + " : " +  obj["timeSinceLastPinged"])
    def execute(self):
        preset = False
        if self.tag == "":
            listByTag = utils.commandLineUtils.promptUserRetry("Would you like to list by tag?")
        else:
            listByTag = True
            preset = True
        if listByTag:
            if (self.tag == ""):
                sc = SearchCommand([],[],"tags--", False, "")
                self.tag = sc.execute()
            tagList = self.getUsersofTagged(self.tag)
        else:
            tagList = utils.userInfoUtils.readFileData()["network"]
        tagList = self.calcTimeSincePinged(tagList)
        tagList = self.sortTime(tagList)
        if not preset:
            self.prettyPrint(tagList)
        return tagList