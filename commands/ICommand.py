import sys

class ICommand:
    def __init__(self, args, opts):
        pass
    def execute(self):
        raise Exception("NotImplementedException")
    def serialize(self):
        raise Exception("NotImplementedException")