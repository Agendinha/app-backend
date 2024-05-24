import json
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    username: str
    password: str
    phone: str
    postalcode: str
    usertype: str

class UserLogin(BaseModel):
    email: str
    password: str

class User(json.JSONEncoder):
    def __init__(self, id, email, username, password, phone, postalcode, usertype):
        self.id = id
        self.email = email
        self.username = username
        self.password = password
        self.phone = phone
        self.postalcode = postalcode
        self.usertype = usertype

    # init but all fields are optional
    def __init__(self, email=None, username=None, password=None, phone=None, postalcode=None, usertype=None):
        self.email = email
        self.username = username
        self.password = password
        self.phone = phone
        self.postalcode = postalcode
        self.usertype = usertype

    def toJSON(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "phone": self.phone,
            "postalcode": self.postalcode,
            "usertype": self.usertype
        }
    
