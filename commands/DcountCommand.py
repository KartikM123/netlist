import sys, getopt
from datetime import datetime
from commands.ICommand import ICommand, format
from utils.userInfoUtils import *
from utils.commandLineUtils import * 
import pandas as pd 
import numpy as np
import json

class DcountCommand(ICommand):
    def __init__(self, args, opts):
        self.args = args
        self.opts = opts
    def getDCount(self, trait):
        file_data = readFileData()
        uniqueTraitValues = []
        for obj in file_data["network"]:
            if not obj[trait] in uniqueTraitValues:
                uniqueTraitValues.append(obj[trait])
        return uniqueTraitValues
    def execute(self):
        trait = getTrait()
        dCount = self.getDCount(trait)
        print("Unique ids for " + trait + " are " + dCount)
        return 