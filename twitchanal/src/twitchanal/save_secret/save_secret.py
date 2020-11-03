import os
import yaml
from termcolor import colored, cprint

def save_id_secret(id, secret):
    data = {'client_id': id, 'secret_key': secret}
    with open('secret.yaml', 'w') as f:
        yaml.dump(data, f)    
    return True


def load_id_secret():
    id = None
    secret = None
    # check if `secret.yaml` exists
    if(not os.path.exists('secret.yaml')):
        cprint('Error: `secret.yaml` not found. '
               'Please go the the dir contains this file '
               'or create a new one.', 'red')
        return (id, secret)

    # load data
    with open('secret.yaml', 'r') as f:
        data = yaml.load(f)
        id = data['client_id']
        secret = data['secret_key']
        print(id)
        print(secret)
    
    return (id, secret)


# load_id_secret()