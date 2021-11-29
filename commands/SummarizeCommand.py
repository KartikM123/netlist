import sys, getopt
from datetime import datetime
from commands.ICommand import ICommand, format
from commands.ListCommand import ListCommand
import utils
import json
class SummarizeCommand(ICommand):
    def __init__(self, args, opts):
        self.args = args
        self.opts = opts
    def prettyPrintTraits(self, activeTags):
        prettyStr = "TAGS: "
        for tag in activeTags:
            prettyStr += "-"+tag+"- "
        return prettyStr
    def getIdealUser(self, tagOptions, outputtedUsers):
        #make sure that we output a new user
        for i in range (0, len(tagOptions)):
            if not tagOptions[i]["name"] in outputtedUsers:
                return tagOptions[i]["name"], tagOptions[i]["timeSinceLastPinged"]
        return tagOptions[0]["name"] , tagOptions[0]["timeSinceLastPinged"]
    def getUserForTag(self, tag, outputtedUsers):
        lc = ListCommand([],[], tag)
        tagList = lc.execute()
        userToOutput, timePinged = self.getIdealUser(tagList, outputtedUsers)
        print (userToOutput + " | " + timePinged)
        return userToOutput
    def execute(self):
        outputtedUsers = []
        print("--SUMMARY OF NETWORK--")
        activeTags = utils.userInfoUtils.readFileData()["activeTags"]
        print(self.prettyPrintTraits(activeTags))
        for tag in activeTags:
            print("-" + tag + "-")
            user = self.getUserForTag(tag, outputtedUsers)
            outputtedUsers.append(user)
            print("")