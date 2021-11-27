import sys, getopt
from datetime import datetime
from commands.ICommand import *
from utils.userInfoUtils import UserInfo, prebuiltTrait, printUserInfo, dictToUserInfo
from utils.commandLineUtils import *
import pandas as pd 
import numpy as np
import json

class SearchCommand(ICommand):
    def __init__(self, args, opts, trait, terminal):
        self.args = args
        self.opts = opts
        self.trait = trait
        self.terminal = terminal #know if to prettyprint result
    #naive approach -- similar sequences
    #   Pros: easy to implement, max substring
    #   Cons: runtime, only looks for substring and can naively not compare word length
    def similarSubSequence(self, search, test, a, b):
        subsequence = ""
        for i in range(a, len(search)):
            for j in range(b, len(test)):
                if (search[i] == test[j]):
                    subsequence += search[i]
                else:
                    return subsequence
        return subsequence
    def getSimilarSeqs(self, search, test):
        maxSubSequence = {} #this will contain the largest substring similarity
        for i in range(0, len(search)):
            maxSubSequence[i] = ""
            for j in range(0, len(test)):
                if search[i] == search[j]:
                    subsequence = self.similarSubSequence(search, test, i, j)
                    if (len(subsequence) > len(maxSubSequence[i])):
                        maxSubSequence[i] = subsequence
        return maxSubSequence
    def coefficientSimilarSeqs(self, search, test):
        similarSeqs = self.getSimilarSeqs(search, test)
        coefficient = 0
        for subsequence in similarSeqs:
            pctCovered = len(subsequence) / len(search)
            coefficient = max(coefficient, pctCovered)
        return coefficient
    #Levenshtein distance
    #   Pros: Good N^2 runtime. Can help us trace success
    #   Cons: Is ultimately char comparison. Doesn't extract meaning
    def calcEntryLev(self, lev, i, j, xDim, yDim, search, test):
        if (search[i] == test[j]):
            if (i-1 >= 0 and j-1 >= 0):
                return lev[i-1][j-1]
            elif (i-1 >= 0):
                return lev[i-1][j]
            elif (j -1 >= 0):
                return lev[i][j-1]
            return 0
        deletion = 1000
        insertion = 1000
        substitution = 10000
        if (i-1 >= 0):
            deletion = lev[i-1][j] + 1
        if (j-1 >= 0):
            insertion = lev[i][j-1] + 1
        if (i-1 >= 0 and j-1 >= 0):
            substitution = lev[i-1][j-1] + 1
        res = min([deletion, insertion, substitution])
        if (res == 10000 or res == 0):
            return lev[i][j] #return the same value
        return res #return the new value
    def getLevenshteinDistance(self, search, test):
        x = len(search)
        y = len(test)
        lev = np.zeros((x,y), dtype=int)
        lev[0][0] = 0
        #initilaize row
        for j in range(1,y):
            lev[0][j] = self.calcEntryLev(lev, 0, j, x, y, search, test)
        #initilaize column
        for i in range(1,x):
            lev[i][0] = self.calcEntryLev(lev, i, 0, x, y, search, test)
        #calculate lev
        for i in range(1,x):
            for j in range(1,y):
                lev[i][j] = self.calcEntryLev(lev, i, j, x, y, search, test)
        return lev[x-1][y-1]
    #utils
    def calcSimilarity(self, search, test):
        coefficientSimilarity = self.getLevenshteinDistance(search, test)
        #coefficientSimilarity = self.coefficientSimilarSeqs(search, test) #hopefully will add more
        return coefficientSimilarity
    def searchName(self, name):
        similarWords = []
        with open('db/network.json', 'r+') as outfile:
            file_data = json.load(outfile)
            for obj in file_data["network"]:
                entry = {}
                entry["name"] = obj["name"]
                entry[self.trait] = obj[self.trait]
                entry["lev"] = self.calcSimilarity(name, obj[self.trait])
                similarWords.append(entry)
        return similarWords
    def searchTaggedTraits(self, target):
        similarWords = []
        with open('db/network.json', 'r+') as outfile:
            file_data = json.load(outfile)
            for obj in file_data["network"]:
                if obj["priority"] == target:
                    entry = {}
                    entry["name"] = obj["name"]
                    entry[self.trait] = obj[self.trait]
                    entry["lev"] = ""
                    similarWords.append(entry)
        return similarWords
    def getSearchResults(self, name):
        if self.trait in ID_TRAITS:
            #case just for special prompt -- this is just for UID
            print(self.trait + " was not found, but did you mean any of the following?")
            pinpointSingleItem = True
        elif (self.trait in TAGGING_TRAITS):
            #tagging traits must be ranked
            pinpointSingleItem = False
        else:
            #add a general case for info and things like that which may be pinpoint or general
            pinpointSingleItem = promptUserRetry("Do you want to read from a list? (default is ranked)")
        #priority is a sharedID
        if self.trait in TAGGING_TRAITS:
            similarWords = self.searchTaggedTraits(name)
        else:
            similarWords = self.searchName(name)
        #edge case for unpopulated dictionaries
        if len(similarWords) == 0:
            print("no options found, let's try again")
            return ("", False)
        if (pinpointSingleItem):
            similarWords.sort(key=lambda x: x["lev"], reverse=False)
            entryCount = min(len(similarWords), 5) #ony show top 5
            for i in range (0, entryCount): 
                if (self.trait in ID_TRAITS):
                    print("[" + str(i) + "] " + similarWords[i]["name"] + " : " + str(similarWords[i]["lev"]))
                else:
                    print("[" + str(i) + "] " + similarWords[i]["name"] + " : " +  similarWords[i][self.trait] + " | " + str(similarWords[i]["lev"]))
            done = False
            entryPicker = int(getCallbackResponse("Type the entry you desire:", lambda x : ((x.isdigit()) and int(x) >= 0 and int(x) < entryCount)))
            if (self.terminal): #used to differnetiate utility case from general
                printInfoOfName(similarWords[entryPicker]["name"])
            return (similarWords[entryPicker]["name"], True)
        else:
            for i in range (0, len(similarWords)):
                print("[" + str(i) + "] " + similarWords[i]["name"] + " : " +  similarWords[i][self.trait] + " | " + str(similarWords[i]["lev"]))
            anotherSearch = promptUserRetry("Would you like see a specific user's info? (y/n)")
            if (anotherSearch):
                entryPicker = int(getCallbackResponse("Type the entry you desire:", lambda x : (x.isdigit() and int(x) >= 0 and int(x) < entryCount)))
                if (self.terminal):
                    printInfoOfName(similarWords[entryPicker]["name"])
            return "done"
    def getTarget(self):
        newVal = ""
        msg = "Enter " + self.trait + " of user: "
        if (self.trait == "name"):
            #special case as this is a unique identifier
            newVal = getCallbackResponse(msg, lambda x: x != "")
            return (newVal, not isUniqueName(newVal))
        elif (self.trait == "priority"):
            newVal = getCallbackResponse(msg, lambda x : x.isdigit())
        else:
            newVal = getCallbackResponse(msg, lambda x : x != "")
        return (newVal, False)
    def execute(self):
        if (self.trait == ""):
            self.trait = getTrait()
        done = False
        while (not done):
            t, done = self.getTarget()
            if (not done):
                t, done = self.getSearchResults(t)
        return t