import sys, getopt
from datetime import datetime
from commands.ICommand import ICommand, format
from utils.userInfoUtils import UserInfo
import json

class PingCommand(ICommand):
    def __init__(self, args, opts):
        self.args = args
        self.opts = opts
    def isUniqueName(self, name):
        with open('db/network.json', 'r+') as outfile:
            file_data = json.load(outfile)
            for obj in file_data["network"]:
                if (obj["name"] == name):
                    return False
            return True
    def getTargetName(self):
        newName = ""
        while (newName=="" or self.isUniqueName(newName)):
            newName = raw_input("Enter name of user: ")
            if (self.isUniqueName(newName)):
                print("please enter a valid username")
        return newName
    def pingUser(self, name):
        with open('db/network.json', 'r+') as outfile:
            #load fileData
            file_data = json.load(outfile)
            #serialize our new userInfo object
            for user in file_data["network"]:
                if (user["name"] == name):
                    user["timePinged"] = str(datetime.now().strftime(format))
            #reset seek so it will overwrite at base index
            outfile.seek(0)
            # convert back to json.
            json.dump(file_data, outfile)
    def execute(self):
        name = self.getTargetName()
        self.pingUser(name)

