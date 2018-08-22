import os

from miniflux.request import (
    MinifluxAPIManager,
    APIInvalidAuthError,
    APINotFoundError,
)
from miniflux.app import App, Pause
from .contexts.feed import FeedContext
from .config import Config


def main():
    try:
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
        config.save()

        app = App()

        app.register_src('miniflux_api', api)
        app.register_src('config', config)
        app.register_src('pause', Pause(app))

        app.register_context('feed_view', FeedContext)

        app.set_default('feed_view')

        with app:
            app.loop()
    except KeyboardInterrupt:
        pass
    except Exception:
        if os.getenv('MINIFLUX_CLI_DEBUG', False):
            raise


if __name__ == '__main__':
    main()
