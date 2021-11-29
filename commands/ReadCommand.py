import sys, getopt
from datetime import datetime
from commands.ICommand import ICommand, format
from utils.userInfoUtils import UserInfo, printUserInfo, dictToUserInfo, readFileData
from commands.SearchCommand import SearchCommand
import json
def getUserInfoFromTarget(name):
        file_data = readFileData()
        for obj in file_data["network"]:
            if (obj["name"] == name):
                return obj
        return {}
class ReadCommand(ICommand):
    def __init__(self, args, opts):
        self.args = args
        self.opts = opts
    def getTargetName(self):
        search = SearchCommand([],[], "name", False, "")
        return search.execute()
    def execute(self):
        name = self.getTargetName()
        userInfo = getUserInfoFromTarget(name)
        printUserInfo(dictToUserInfo(userInfo))

