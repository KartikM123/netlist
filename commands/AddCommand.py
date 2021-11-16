import sys, getopt
from datetime import datetime
from commands.ICommand import ICommand, format
from utils.userInfoUtils import UserInfo
import json

class AddCommand(ICommand):
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
    def getUserInfo(self):
        userInfo = UserInfo()
        newName = ""
        while (newName=="" or not self.isUniqueName(newName)):
            newName = raw_input("Enter name of user: ")
            if (not self.isUniqueName(newName)):
                print("please enter a unique username")
        userInfo.name = newName
        userInfo.info = raw_input("Enter info of " + userInfo.name + ": ")
        userInfo.email = raw_input("Enter email of " + userInfo.name + ": ")
        return userInfo
    def printUserInfo(self, userInfo):
        print("name:", userInfo.name)
        print("info:", userInfo.info)
        print("email:", userInfo.email)
        return
    def saveUserInfo(self, userInfo):
        with open('db/network.json', 'r+') as outfile:
            #load fileData
            file_data = json.load(outfile)
            #serialize our new userInfo object
            newObj = userInfo.serialize()
            newObj["timeAdded"] = str(datetime.now().strftime(format))
            newObj["timePinged"] = str(datetime.now().strftime(format))
            # Join new_data with file_data inside emp_details
            file_data["network"].append(newObj)
            #reset seek so it will overwrite at base index
            outfile.seek(0)
            # convert back to json.
            json.dump(file_data, outfile)
    def execute(self):
        userInfo = self.getUserInfo()
        self.printUserInfo(userInfo)
        self.saveUserInfo(userInfo)
        print("finished add")

