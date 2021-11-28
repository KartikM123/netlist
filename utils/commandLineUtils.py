import json
import sys
import utils.userInfoUtils
import commands
# utils for special "always search" type cases
def getResponseWithOptions(msg, trait):
    if (msg == "--dc"):
        dcount = commands.DcountCommand.DcountCommand([], [], trait)
        dcount.execute()
        return True
    elif (msg == "--r"):
        r = commands.ReadCommand.ReadCommand([], [])
        r.execute()
        return True
    elif (msg == "--exit"):
        sys.exit()
    return False


# utils for getting generic input
def getOptionalResponse(msg, trait):
    while (1):
        res = raw_input(msg)
        if (getResponseWithOptions(msg, trait)):
            print("Now returning to original query")
        else:
            return res


def getCallbackResponse(msg, callbackCheck, trait):
    while (1):
        res = raw_input(msg)
        if (getResponseWithOptions(res, trait)):
            print("Now returning to original query")
        elif (callbackCheck(res) == True):
            return res
        else:
            print("Please input a valid value")


# utils for generic but common use cases
def promptUserRetry(msg):
    pick = getCallbackResponse(msg + "(y/n)", lambda msg: ((msg == "y") or (msg == "n")), "")
    if (pick == "y"):
        return True
    elif (pick == "n"):
        return False

# utils for managing dynamic traits
def getOptions():
    print("You can search by any of the following traits")
    print(" -- name -- ")
    file_data = utils.userInfoUtils.readFileData()
    for trait in file_data["userTraits"]:
        print(" -- " + trait + " -- ")
    print(" -- tags -- ")
    print(" -- priority -- ")
    print(" -- timePinged -- ")
    print(" -- timeAdded -- ")


def isValidOption(opt):
    file_data = utils.userInfoUtils.readFileData()
    for trait in file_data["userTraits"]:
        if trait == opt:
            return True
    return utils.userInfoUtils.prebuiltTrait(opt)


def getTrait():
    while (1):
        t = raw_input("Pick a trait to search (type `?` for help): ")
        if (t == "?"):
            getOptions()
        elif (isValidOption(t)):
            return t
        else:
            print("Invalid choice :(")

def getListTags(msg):
    activeTags = utils.userInfoUtils.readFileData()["activeTags"]
    while(1):
        t = raw_input(msg + "(split using \",\") [see tags with \"?\"]")
        if (t == "?"):
            print("Active tags: " + str(activeTags))
        else:
            tags = t.split(",")
            res = []
            if (len(tags) == 0):
                print("Please input some tags")
            else:
                for tag in tags:
                    tag = tag.lstrip()
                    if (tag in activeTags):
                        res.append(tag)
                    else:
                        addTag = promptUserRetry(tag + " is a new tag. Would you like to add it to the tag dict?")
                        if (addTag):
                            addTagToNetwork(tag)
                            res.append(tag)
                        else:
                            retryTag = promptUserRetry("Do you want to try to replace this with a similar tag?")
                            if (retryTag):
                                sc = commands.SearchCommand.SearchCommand([],[], "tags--", False, tag)
                                res.append(sc.execute())
                res = list(dict.fromkeys(res)) #remove duplicates
                return res

# misc helpers
def addTagToNetwork(tag):
    with open('db/network.json', 'r+') as outfile:
        #serialize our new userInfo object
        file_data = json.load(outfile)
        # Join new_data with file_data inside emp_details
        file_data["activeTags"].append(tag)
        #reset seek so it will overwrite at base index
        outfile.seek(0)
        # convert back to json.
        json.dump(file_data, outfile)
def isUniqueName(name):
    file_data = utils.userInfoUtils.readFileData()
    for obj in file_data["network"]:
        if (obj["name"] == name):
            return False
    return True


def printInfoOfName(name):
    file_data = utils.userInfoUtils.readFileData()
    for obj in file_data["network"]:
        if obj["name"] == name:
            utils.userInfoUtils.printUserInfo(utils.userInfoUtils.dictToUserInfo(obj))
            return
