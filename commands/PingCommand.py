import sys, getopt
from datetime import datetime
from commands.ICommand import ICommand, format
from utils.userInfoUtils import UserInfo
from commands.SearchCommand import SearchCommand
import json

class PingCommand(ICommand):
    def __init__(self, args, opts):
        self.args = args
        self.opts = opts
    def getTargetName(self):
        newName = ""
        search = SearchCommand([],[], "name", False, "")
        return search.execute()
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
        print("Successfully pinged " + name + "!")
    def execute(self):
        name = self.getTargetName()
        self.pingUser(name)

