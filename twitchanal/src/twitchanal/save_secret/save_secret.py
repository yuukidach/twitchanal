import os
import yaml
from termcolor import colored, cprint
from typing import Tuple


def save_id_secret(id: str, secret: str) -> bool:
    """ Save id and secret in yaml file.

    Args:
        id (str): user id
        secret (str): user secret key

    Returns:
        bool: True
    """
    data = {'client_id': id, 'secret_key': secret}
    with open('secret.yaml', 'w') as f:
        yaml.dump(data, f)
    return True


def load_id_secret() -> Tuple[str, str]:
    """ Load id and secret from yaml file.

    Returns:
        (id, secret): return None if no valid data is gotten.
    """
    id = None
    secret = None
    # check if `secret.yaml` exists
    if (not os.path.exists('secret.yaml')):
        cprint(
            'Error: `secret.yaml` not found. '
            'Please go the the dir contains this file '
            'or create a new one.', 'red')
        return (id, secret)

    # load data
    with open('secret.yaml', 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        id = data['client_id']
        secret = data['secret_key']
    return (id, secret)


# load_id_secret()