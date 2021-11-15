class UserInfo(object):
    def __init__(self):
        self.name = ""
        self.info = ""
        self.email = ""
    def serialize(self):
        obj = {}
        obj["name"] = self.name
        obj["info"] = self.info
        obj["email"] = self.email
        return obj