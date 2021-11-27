import json
from utils.userInfoUtils import UserInfo, printUserInfo, dictToUserInfo, prebuiltTrait
from commands.DcountCommand import DcountCommand
from commands.ReadCommand import ReadCommand
#utils for special "always search" type cases
def getResponseWithOptions(msg, trait):
    if (msg == "--dc"):
        dcount = DcountCommand([],[], trait)
        dcount.execute()
        return True
    elif (msg == "--r"):
        r = ReadCommand([],[])
        r.execute()
        return True
    return False
#utils for getting generic input 
def getOptionalResponse(msg, trait):
    while(1):
        res = raw_input(msg)
        if (getResponseWithOptions(msg, trait)):
            print("Now returning to original query")
        else:
            return res
def getCallbackResponse(msg, callbackCheck, trait):
    while(1):
        res = raw_input(msg)
        if (getResponseWithOptions(res, trait)):
            print("Now returning to original query")
        elif (callbackCheck(res) == True):
            return res
        else:
            print("Please input a valid value")
#utils for generic but common use cases
def promptUserRetry(msg):
    getCallbackResponse(msg +  "(y/n)",  lambda msg: ((msg == "y") or (msg == "n")), "")
    while (1):
        pick = raw_input(msg +  "(y/n)")
        if (pick == "y"):
            return True
        elif (pick == "n"):
            return False
        else:
            print("Please typer either y or n")
#utils for managing dynamic traits
def getOptions():
    print("You can search by any of the following traits")
    print(" -- name -- ")
    file_data = readFileData()
    for trait in file_data["userTraits"]:
        print(" -- " + trait + " -- ")
    print (" -- priority -- ")
    print (" -- timePinged -- ")
    print (" -- timeAdded -- ")
def isValidOption(opt):
    file_data = readFileData()
    for trait in file_data["userTraits"]:
        if trait == opt:
            return True
    return prebuiltTrait(opt)
def getTrait():
    while(1):
        t = raw_input("Pick a trait to search (type `?` for help): ")
        if (t == "?"):
            getOptions()
        elif (isValidOption(t)):
            return t
        else:
            print("Invalid choice :(")
#misc helpers
def isUniqueName(name):
    file_data = readFileData()
    for obj in file_data["network"]:
        if (obj["name"] == name):
            return False
    return True
def printInfoOfName(name):
    file_data = readFileData()
    for obj in file_data["network"]:
        if obj["name"] == name:
            printUserInfo(dictToUserInfo(obj))
            return
def readFileData():
    with open('db/network.json', 'r+') as outfile:
        file_data = json.load(outfile)
        return file_data
