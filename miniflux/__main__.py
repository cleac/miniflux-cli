from getpass import getpass

from miniflux.request import (
    MinifluxAPIManager,
    APIInvalidAuthError,
    APINotFoundError,
)
from miniflux.app import App
from .tui import FeedContext


def main():
    url = input('Enter url: ')
    login = input('Enter login: ')
    password = getpass('Enter password: ')

    api = MinifluxAPIManager(url, login, password)

    try:
        api.get_unread()
    except APIInvalidAuthError:
        print('Wrong login or/and password was provided')
        exit(1)
    except APINotFoundError:
        print('Could not get feed from server. Check the url and the server')
        exit(2)

    app = App()

    app.register_src('miniflux_api', api)

    app.register_context('feed_view', FeedContext)

    app.set_default('feed_view')

    with app:
        app.loop()


if __name__ == '__main__':
    main()
