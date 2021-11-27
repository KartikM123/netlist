import sys, getopt
from datetime import datetime
from commands.ICommand import ICommand, format
import utils
import json

class AddCommand(ICommand):
    def __init__(self, args, opts):
        self.args = args
        self.opts = opts
    def uniqueProxy(self,x):
        return utils.commandLineUtils.isUniqueName(x)
    def getUserInfo(self):
        userInfo = utils.userInfoUtils.UserInfo()
        userInfo.name = utils.commandLineUtils.getCallbackResponse("Enter name of user: ", lambda x : self.uniqueProxy(x), "name")
        userInfo.tags = utils.commandLineUtils.getListTags("Enter tags to associate with user")
        for trait in userInfo.traits:
            userInfo.traits[trait] = utils.commandLineUtils.getOptionalResponse("Please enter " + trait + " for " + userInfo.name + ": ", trait)
        userInfo.priority  = utils.commandLineUtils.getCallbackResponse("Enter numerical priority of " + userInfo.name + ": ", lambda x: x.isdigit(), "priority")
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
        utils.userInfoUtils.printUserInfo(userInfo)
        self.saveUserInfo(userInfo)
        print("finished add")

