from typing import NamedTuple, Optional, Dict, Any

import json
import os

from getpass import getpass

CONFIG_FILE = os.path.join(os.getenv('HOME') + '/.config/miniflux.json')


class Config(NamedTuple):

    url_host: str
    login: str
    password: Optional[str]

    remember_password: Optional[bool]

    open_command: str = 'xdg-open'
    alternative_open_command: Optional[str] = None


def migrate_config(obj: Dict[str, Any]) -> Dict[str, Any]:
    if 'remember_login' in obj:
        del obj['remember_login']
    return obj


def read_data_from_file() -> Dict[str, Any]:
    with open(CONFIG_FILE, 'r') as f:
        return json.loads(f.read())


def load():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return Config(
                migrate_config(read_data_from_file()))
    except FileNotFoundError:
        with open(CONFIG_FILE, 'w') as f:
            f.write('{}')
    except TypeError:
        pass
    return Config(**read_initial_config())


def read_initial_config() -> Dict[str, Any]:
    config = read_data_from_file()

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

    return migrate_config(config)


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
