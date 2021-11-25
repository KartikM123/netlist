import sys, getopt
from datetime import datetime
from commands.ICommand import ICommand, format
from utils.userInfoUtils import UserInfo
import pandas as pd 
import numpy as np
import json

class SearchCommand(ICommand):
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
        if (test == "s"):
            print lev
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
                entry["lev"] = self.calcSimilarity(name, obj["name"])
                similarWords.append(entry)
        return similarWords
    #user facing
    def getSearchResults(self, name):
        print(name + " was not found, but did you mean any of the following names?")
        similarWords = self.searchName(name)
        similarWords.sort(key=lambda x: x["lev"], reverse=False)
        entryCount = min(len(similarWords), 5) #ony show top 5
        for i in range (0, entryCount): 
            print("[" + str(i) + "] " + similarWords[i]["name"] + " : " + str(similarWords[i]["lev"]))
        entryPicker = int(raw_input("type the entry you desire: "))
        if (entryPicker >= entryCount or entryCount < 0):
            print("invalid entry, restarting search process")
            return ("", False)
        return (similarWords[entryPicker]["name"], True)
    def getTargetName(self):
        newName = ""
        newName = raw_input("Enter name of user: ")
        if (not self.isUniqueName(newName)):
            return (newName, True)
        return (newName, False)
    def execute(self):
        done = False
        while (not done):
            name, done = self.getTargetName()
            if (not done):
                name, done = self.getSearchResults(name)
        print("Successfully picked " + name + "!")
        return name