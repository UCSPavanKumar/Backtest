import yaml
import sys
fname = '/home/iob/algotrading/config/config.yaml'
stream = open(fname,'r')
data = yaml.safe_load(stream)
data['auth_code'] = None
data['access_token'] = None

with open(fname,'w') as yaml_file:
    yaml.dump(data,yaml_file,sort_keys=False)

