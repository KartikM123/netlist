import sys, getopt
from datetime import datetime
from commands.ICommand import ICommand, format
from utils.userInfoUtils import UserInfo, prebuiltTrait, printUserInfo, dictToUserInfo
import pandas as pd 
import numpy as np
import json

class SearchCommand(ICommand):
    def __init__(self, args, opts):
        self.args = args
        self.opts = opts
        self.trait = trait
        self.terminal = terminal #know if to prettyprint result
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
        similarWords = self.searchName(name)
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
    def execute(self):
        self.getTrait()
        done = False
        while (not done):
            t, done = self.getTarget()
            if (not done):
                t, done = self.getSearchResults(t)
        return t