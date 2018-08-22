from getpass import getpass

from miniflux.request import (
    MinifluxAPIManager,
    APIInvalidAuthError,
    APINotFoundError,
)
from miniflux.app import App
from .contexts.feed import FeedContext
from .config import Config


def main():
    fail_connection = True
    while fail_connection:
        config = Config.load_config() \
            .fill_keys()

        api = MinifluxAPIManager(config)

        try:
            api.get_unread()
        except APIInvalidAuthError:
            print('Wrong login or/and password was provided')
            exit(1)
        except APINotFoundError:
            print('Could not get feed from server. '
                  'Check the url, internet connection and the server')
            exit(2)

        fail_connection = False

    app = App()

    app.register_src('miniflux_api', api)

    app.register_context('feed_view', FeedContext)

    app.set_default('feed_view')

    with app:
        app.loop()


if __name__ == '__main__':
    main()
