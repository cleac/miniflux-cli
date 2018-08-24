from typing import Sequence

import requests

from requests.auth import HTTPBasicAuth

from miniflux_cli.mapping import FeedItem

APIError = type('APIError', (Exception,), {})

APIInvalidAuthError = type('APIInvalidAuthError', (APIError,), {})
APIBadRequest = type('APIBadRequest', (APIError,), {})
APINotFoundError = type('APINotFoundError', (APIError,), {})


def _determine_error_on_code(code):
    return {
        requests.codes.not_found: APINotFoundError,
        requests.codes.bad_request: APIBadRequest,
        requests.codes.unauthorized: APIInvalidAuthError,
    }.get(code, APIError)


class MinifluxAPIManager:

    def __init__(self, config):
        self._host: str = config.url_host
        self._auth: HTTPBasicAuth = HTTPBasicAuth(
            config.login, config.password)

    def get_unread(self) -> Sequence[FeedItem]:

        result = requests.get(
            '{}/v1/entries'.format(self._host),
            params={'status': 'unread'},
            auth=self._auth)

        if result.status_code != requests.codes.ok:
            raise _determine_error_on_code(result.status_code)

        return [
            FeedItem.parse(item)
            for item in result.json()['entries']
        ]

    def mark_read(self, id: int):

        result = requests.put(
            f'{self._host}/v1/entries',
            json={'entry_ids': [id], 'status': 'read'},
            auth=self._auth)

        if result.status_code != requests.codes.no_content and \
                result.status_code != requests.codes.ok:
            raise _determine_error_on_code(result.status_code)(result.status_code)
