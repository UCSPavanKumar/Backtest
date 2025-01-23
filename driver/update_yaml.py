import yaml
import sys
fname = './config/config.yaml'
stream = open(fname,'r')
data = yaml.safe_load(stream)
data['auth_code'] = sys.argv[1]

with open(fname,'w') as yaml_file:
    yaml.dump(data,yaml_file,sort_keys=False)

    