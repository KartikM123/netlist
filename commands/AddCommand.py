import sys, getopt
from datetime import datetime
from commands.ICommand import ICommand, format
from utils.userInfoUtils import UserInfo, printUserInfo, dictToUserInfo
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
    def promptUserRetry(self):
        while (1):
            pick = raw_input("No option kept, do you want to leave it blank? (y/n)")
            if (pick == "y"):
                return True
            elif (pick == "n"):
                return False
            else:
                print("Please typer either y or n")
    
    def promptUserString(self, message):
        valid = False
        while (not valid):
            value = raw_input(message)
            if (value == ""):
                valid = self.promptUserRetry()
            else:
                valid = True
        return value
    def getUserInfo(self):
        userInfo = UserInfo()
        newName = ""
        while (newName=="" or not self.isUniqueName(newName)):
            newName = raw_input("Enter name of user: ")
            if (not self.isUniqueName(newName)):
                print("please enter a unique username")
        userInfo.name = newName
        for trait in userInfo.traits:
            userInfo.traits[trait] = self.promptUserString("Please enter " + trait + " for " + userInfo.name + ": ")
        userFavor = ""
        while (not userFavor.isdigit()):
            userFavor = raw_input("Enter numerical priority of " + userInfo.name + ": ")
            if (not userFavor.isdigit()):
                print("Please input a valid digit")
        userInfo.priority = userFavor
        return userInfo
    def saveUserInfo(self, userInfo):
        with open('db/network.json', 'r+') as outfile:
            #serialize our new userInfo object
            newObj = userInfo.serialize()
            newObj["timeAdded"] = str(datetime.now().strftime(format))
            newObj["timePinged"] = str(datetime.now().strftime(format))
            file_data = json.load(outfile)
            # Join new_data with file_data inside emp_details
            file_data["network"].append(newObj)
            #reset seek so it will overwrite at base index
            outfile.seek(0)
            # convert back to json.
            json.dump(file_data, outfile)
    def execute(self):
        userInfo = self.getUserInfo()
        printUserInfo(userInfo)
        self.saveUserInfo(userInfo)
        print("finished add")

