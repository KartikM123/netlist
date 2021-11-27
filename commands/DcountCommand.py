import sys, getopt
from datetime import datetime
from commands.ICommand import ICommand, format
from utils.commandLineUtils import getTrait, readFileData 
import pandas as pd 
import numpy as np
import json

class DcountCommand(ICommand):
    def __init__(self, args, opts, trait):
        self.args = args
        self.opts = opts
        self.trait = trait
    def getDCount(self):
        file_data = readFileData()
        uniqueTraitValues = []
        for obj in file_data["network"]:
            if not obj[self.trait] in uniqueTraitValues:
                uniqueTraitValues.append(obj[self.trait])
        return uniqueTraitValues
    def execute(self):
        if (self.trait == ""):
            self.trait = getTrait()
        dCount = self.getDCount()
        print("Unique ids for " + self.trait + " are " + dCount)
        return 