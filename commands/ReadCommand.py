import sys, getopt
from datetime import datetime
from commands.ICommand import ICommand, format
from utils.userInfoUtils import UserInfo, printUserInfo, dictToUserInfo
from SearchCommand import SearchCommand
import json

class ReadCommand(ICommand):
    def __init__(self, args, opts):
        self.args = args
        self.opts = opts
    def getTargetName(self):
        search = SearchCommand([],[], "name", False)
        return search.execute()
    def getUserInfoFromTarget(self, name):
        with open('db/network.json', 'r+') as outfile:
            file_data = json.load(outfile)
            for obj in file_data["network"]:
                if (obj["name"] == name):
                    return obj
            return
    def execute(self):
        name = self.getTargetName()
        userInfo = self.getUserInfoFromTarget(name)
        printUserInfo(dictToUserInfo(userInfo))

