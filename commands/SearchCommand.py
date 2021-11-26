import sys, getopt
from datetime import datetime
from commands.ICommand import ICommand, format
from utils.userInfoUtils import UserInfo, prebuiltTrait, printUserInfo, dictToUserInfo
import pandas as pd 
import numpy as np
import json

class SearchCommand(ICommand):
    def __init__(self, args, opts, trait, terminal):
        self.args = args
        self.opts = opts
        self.trait = trait
        self.terminal = terminal #know if to prettyprint result
    def isUniqueName(self, name):
        with open('db/network.json', 'r+') as outfile:
            file_data = json.load(outfile)
            for obj in file_data["network"]:
                if (obj["name"] == name):
                    return False
            return True
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
    def searchPriority(self, target):
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
    def printInfoHelper(self, name):
        with open('db/network.json', 'r+') as outfile:
            file_data = json.load(outfile)
            for obj in file_data["network"]:
                if obj["name"] == name:
                    printUserInfo(dictToUserInfo(obj))
                    return
        return 
    #user facing
    def getYorN(self,msg):
        while (1):
            pick = raw_input(msg)
            if (pick == "y"):
                return True
            elif (pick == "n"):
                return False
            else:
                print("Please typer either y or n")
    def getSearchResults(self, name):
        isUnique = False
        if self.trait == "name":
            print(self.trait + " was not found, but did you mean any of the following names?")
            isUnique = True
        else:
            print("Let's look at your options for " + self.trait)
            if (self.trait == "priority"):
                isUnique = True
            else:
                isUnique = self.getYorN("Would you like to just read info from a single entry? (y/n)")
        if self.trait == "priority":
            similarWords = self.searchPriority(name)
        else:
            similarWords = self.searchName(name)
        if len(similarWords) == 0:
            print("no options found, let's try again")
            return ("", False)
        if (isUnique):
            similarWords.sort(key=lambda x: x["lev"], reverse=False)
            entryCount = min(len(similarWords), 5) #ony show top 5
            for i in range (0, entryCount): 
                if (self.trait == "name"):
                    print("[" + str(i) + "] " + similarWords[i]["name"] + " : " + str(similarWords[i]["lev"]))
                else:
                    print("[" + str(i) + "] " + similarWords[i]["name"] + " : " +  similarWords[i][self.trait] + " | " + str(similarWords[i]["lev"]))
            done = False
            while (not done):
                entryPicker = raw_input("type the entry you desire: ")
                done = True
                if (not entryPicker.isdigit()):
                    print("invalid entry, please input a digit")
                    done = False
            entryPicker = int(entryPicker)
            if (entryPicker >= entryCount or entryCount < 0):
                print("invalid entry, restarting search process")
                return ("", False)
            if (self.terminal):
                self.printInfoHelper(similarWords[entryPicker]["name"])
            return (similarWords[entryPicker]["name"], True)
        else:
            for i in range (0, len(similarWords)):
                print("[" + str(i) + "] " + similarWords[i]["name"] + " : " +  similarWords[i][self.trait] + " | " + str(similarWords[i]["lev"]))
            anotherSearch = self.getYorN("Would you like see a specific user's info? (y/n)")
            if (anotherSearch):
                done = False
                while (not done):
                    entryPicker = raw_input("type the entry you desire: ")
                    done = True
                    if (not entryPicker.isdigit()):
                        print("invalid entry, please input a digit")
                        done = False
                    entryPicker = int(entryPicker)
                    if (entryPicker >= len(similarWords) or len(similarWords) < 0):
                        print("invalid entry, restarting search process")
                        return ("", False)
                    if (self.terminal):
                        self.printInfoHelper(similarWords[entryPicker]["name"])
            return "done"
    def getTarget(self):
        newVal = ""
        newVal = raw_input("Enter " + self.trait + " of user: ")
        if self.trait == "name":
            if (not self.isUniqueName(newVal)):
                return (newVal, True)
            return (newVal, False)
        if self.trait == "priority":
            if (not newVal.isdigit()):
                print("Please input a valid priority digit")
        return (newVal, False)
    def getOptions(self):
        print("You can search by any of the following traits")
        print(" -- name -- ")
        with open('db/network.json', 'r+') as outfile:
            file_data = json.load(outfile)
            for trait in file_data["userTraits"]:
                print(" -- " + trait + " -- ")
        print (" -- priority -- ")
        print (" -- timePinged -- ")
        print (" -- timeAdded -- ")
    def isValidOption(self, opt):
        with open('db/network.json', 'r+') as outfile:
            file_data = json.load(outfile)
            for trait in file_data["userTraits"]:
                if trait == opt:
                    return True
        return prebuiltTrait(opt)
    def getTrait(self):
        while(1):
            t = raw_input("Pick a trait to search (type `?` for help): ")
            if (t == "?"):
                self.getOptions()
            elif (self.isValidOption(t)):
                self.trait = t
                return
            else:
                print("Invalid choice :(")
        
    def execute(self):
        if (self.trait == ""):
            self.getTrait()
        done = False
        while (not done):
            t, done = self.getTarget()
            if (not done):
                t, done = self.getSearchResults(t)
        return t