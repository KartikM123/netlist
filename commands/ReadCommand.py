from commands.ICommand import ICommand
import json
class ReadCommand(ICommand):
    def __init__(self, args, opts):
        pass
    def readData(self):
        with open('db/network.json', 'r+') as outfile:
            #load fileData
            file_data = json.load(outfile)
            return file_data["network"]
    def execute(self):
        fileData = self.readData()
        print(fileData)