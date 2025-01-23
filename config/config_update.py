import sys
import yaml
class ConfigUpdate:
    def __init__(self):
        self.fname = './config/config.yaml'
        stream = open(self.fname,'r')
        self.data = yaml.safe_load(stream)
    
    def retrieveClientId(self):
        return self.data['client_id']
    
    def updateAccessToken(self,code):
        self.data['access_token'] = code
        with open(self.fname,'w') as yaml_file:
            yaml.dump(self.data,yaml_file,sort_keys=False)
    
    def retrieveAccessToken(self):
        if self.data['access_token'] is not None:
            return self.data['access_token']
        else:
            return None
