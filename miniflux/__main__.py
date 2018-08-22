import sys
import os

from miniflux.request import (
    MinifluxAPIManager,
    APIInvalidAuthError,
    APINotFoundError,
)
from miniflux.app import App, Pause
from .contexts.feed import FeedContext
from .config import Config

HELP = """
miniflux-cli

A simple terminal reader for Miniflux2 RSS reader.

Usage.

Currently, miniflux-cli does not do much work. When you first run
an application, it will ask you to enter host, login and password.
After successful authorization, it saves configuration in JSON format
at "$HOME/.config/miniflux.json", you are free to edit it with hands.

After succesful auth, you will see list of new items opened. You can
navigate through it using vim shortcuts or arrow keys. When you want
to open an entry, press Enter or letter "o" and it will open it in your
browser (you can change it, look at "Confuguration" part next). There
is also possibility to open link with alternative command pressing
letter "O" (big letter O). To quit, press "q" or Control+C.

Configuration.

Configuration of application is stored at "$HOME/.config/miniflux.json",
if you want to drop settings - simply delete it. Here are configuration
values descriped:
  * Primary values
    - "url_host": string -- url to miniflux instance you want to connect to
    - "login":    string -- login used to authorize
    - "password": string -- password used to authorize

  * Remembering fields
    - "remember_login":    bool -- whether to remember login, or
                                   not. If empty will ask it while
                                   authorizing and remember the choice.
    - "remember_password": bool -- whether to remember a password, same
                                   like "remember_login"

  * Opening commands
    - "open_command":             string -- command to open links
                                            default: xdg-open
    - "alternative_open_command": string -- alternative command to open links

This app evolves a lot, so remember to update it sometimes.


miniflux-cli  Copyright (C) 2018 alexcleac <alexcleac(at)nesterenko.xyz>
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions
"""


def main():
    # TODO: Switch to argparse
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg in {'-h', '--help'}:
                print(HELP)
                sys.exit(0)

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
