import sys, getopt
from datetime import datetime
from commands.ICommand import ICommand, format
import utils
import pandas as pd
import numpy as np
import json

class DcountCommand(ICommand):
    def __init__(self, args, opts, trait):
        self.args = args
        self.opts = opts
        self.trait = trait
    def getDCount(self):
        file_data = utils.userInfoUtils.readFileData()
        uniqueTraitValues = []
        if self.trait == "tags":
            return file_data["activeTags"]
        for obj in file_data["network"]:
            if not obj[self.trait] in uniqueTraitValues:
                uniqueTraitValues.append(obj[self.trait])
        return uniqueTraitValues
    def execute(self):
        if (self.trait == ""):
            self.trait = utils.commandLineUtils.getTrait()
        dCount = ', '.join(self.getDCount())
        print("Unique ids for " + self.trait + " are [" + str(dCount) + "]")
        return 