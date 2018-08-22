from getpass import getpass

from miniflux.request import (
    MinifluxAPIManager,
    APIInvalidAuthError,
    APINotFoundError,
)
from miniflux.tui import (
    render_feed_list,
)


def main():
    url = input('Enter url: ')
    login = input('Enter login: ')
    password = getpass('Enter password: ')

    api = MinifluxAPIManager(url, login, password)

    try:
        feed_entries = api.get_unread()
    except APIInvalidAuthError:
        print('Wrong login or/and password was provided')
        exit(1)
    except APINotFoundError:
        print('Could not get feed from server. Check the url and the server')
        exit(2)

    print('\n'.join(render_feed_list(feed_entries, 20)))


if __name__ == '__main__':
    main()
