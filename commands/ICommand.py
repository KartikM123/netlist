import sys

format = "%a %b %d %H:%M:%S %Y"
#this file is just for reference. ICommand is not used explicitly anywhere
class ICommand:
    def __init__(self, args, opts):
        pass
    def execute(self):
        raise Exception("NotImplementedException")