import json
import os

from getpass import getpass

from miniflux.meta.mapping import DClass

CONFIG_DIR = os.path.join(os.getenv('HOME') + '/.config')


class Config(DClass):

    url_host: str
    login: str
    password: str

    remember_login: bool
    remember_password: bool

    alternative_open_command: str

    @classmethod
    def load_config(cls):
        try:
            with open(CONFIG_DIR + 'miniflux.json', 'r') as f:
                return cls(**json.loads(f.read()))
        except FileNotFoundError:
            return cls()

    def fill_keys(self):
        if not self.url_host:
            self.url_host = input('Please, enter url: ')

        if not self.login:
            self.login = input('Please, enter login: ')
            while self.remember_login is None:
                remember = input('Do you want to remember it? [yN] ')
                if 'y' in remember.lower():
                    self.remember_login = True
                elif not remember or 'n' in remember.lower():
                    self.remember_login = False

        if not self.password:
            self.password = getpass('Please, enter password: ')
            while self.remember_password is None:
                remember = input(
                    'Do you want to remember it? '
                    '(Note: it is stored as plaintext) [yN] ')
                if 'y' in remember.lower():
                    self.remember_password = True
                elif not remember or 'n' in remember.lower():
                    self.remember_password = False

        return self

    def save(self):
        result = self.dict

        # Cleanup "remember" items
        if result['login'] and result['remember_login']:
            del result['remember_login']
        if result['password'] and result['remember_password']:
            del result['remember_password']

        if result['remember_login'] is False and result['login']:
            del result['login']
        if result['remember_password'] is False and result['password']:
            del result['password']

        # Cleanup empty keys
        remove_keys = set()
        for key in result.keys():
            if result[key] is None:
                remove_keys.add(key)
        for key in remove_keys:
            del result[key]

        # Write to file and dumps
        with open('miniflux.json', 'w') as f:
            f.write(json.dumps(result, ensure_ascii=False))
