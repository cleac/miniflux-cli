from typing import NamedTuple, Optional, Mapping, Any

import json
import os

from getpass import getpass

CONFIG_FILE = os.path.join(os.getenv('HOME') + '/.config/miniflux.json')


class Config(NamedTuple):

    url_host: str
    login: str
    password: Optional[str]

    remember_password: Optional[bool]

    alternative_open_command: Optional[str]

    open_command: str = 'xdg-open'


def load():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return Config(**json.loads(f.read()))
    except FileNotFoundError:
        with open(CONFIG_FILE, 'w') as f:
            f.write('{}')
    except TypeError:
        pass
    return Config(**read_initial_config())


def read_initial_config() -> Mapping[str, Any]:
    with open(CONFIG_FILE, 'r') as f:
        config = json.loads(f.read())

    if 'url_host' not in config:
        config['url_host'] = input('Please, enter url: ')

    if 'login' not in config:
        config['login'] = input('Please, enter login: ')

    if 'password' not in config:
        config['password'] = getpass('Please, enter password: ')
        while 'remember_password' not in config:
            remember = input(
                'Do you want to remember it? '
                '(Note: it is stored as plaintext) [yN] ')
            if 'y' in remember.lower():
                config['remember_password'] = True
            elif not remember or 'n' in remember.lower():
                config['remember_password'] = False

    return config


def save(config: Config):
    result = dict(config._asdict())

    # Set "remember" password to None
    if result['password'] and result['remember_password']:
        result['remember_password'] = None
    if result['remember_password'] is False and result['password']:
        result['password'] = None

    # Cleanup empty keys
    remove_keys = set()
    for key in result.keys():
        if result[key] is None:
            remove_keys.add(key)
    for key in remove_keys:
        del result[key]

    # Write to file and dumps
    with open(CONFIG_FILE, 'w') as f:
        f.write(json.dumps(result, ensure_ascii=False))
