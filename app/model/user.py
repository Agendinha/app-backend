import json
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    username: str
    password: str
    usertype: str

class UserLogin(BaseModel):
    email: str
    password: str

class User(json.JSONEncoder):
    def __init__(self, id, email, username, password, usertype):
        self.id = id
        self.email = email
        self.username = username
        self.password = password
        self.usertype = usertype

    # init but all fields are optional
    def __init__(self, email=None, username=None, password=None, usertype=None):
        self.email = email
        self.username = username
        self.password = password
        self.usertype = usertype

    def toJSON(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "usertype": self.usertype
        }
    
