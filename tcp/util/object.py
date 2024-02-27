import json

class Client:
    def __init__(self, json_data):
        client_data = json.loads(json_data)
        self.type = "CLIENT"
        self.ip = client_data.get('ip')
        self.port = client_data.get('port')
        self.name = client_data.get('name')
        self.location = client_data.get('location')
        self.org = client_data.get('org')

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {
            "type": self.type,
            "ip": self.ip,
            "port": self.port,
            "name": self.name,
            "location": self.location,
            "org": self.org
        }
        
class Connector:
    def __init__(self, json_data):
        client_data = json.loads(json_data)
        self.type = "CONNECTOR"
        self.ip = client_data.get('ip')
        self.port = client_data.get('port')
        self.name = client_data.get('name')
       
    def __str__(self):
        return str(self.to_dict())
    
    def to_dict(self):
        return {
            "type": self.type,
            "ip": self.ip,
            "port": self.port,
            "name": self.name
        }