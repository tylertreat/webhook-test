from httplib2 import Http
import json
import logging
import sys
import time
import traceback


_API_KEY = None
_PROJECT_ID = None
_DEBUG = False

_SERVICE_HOST = 'https://kaput-dev.appspot.com'
_SERVICE_ENDPOINT = '/api/v1/exception'

_HTTP = Http()


def init(api_key, project_id, patch=True, debug=False):
    """Initialize the Kaput service for error monitoring."""

    global _API_KEY
    _API_KEY = api_key
    global _PROJECT_ID
    _PROJECT_ID = project_id
    global _DEBUG
    _DEBUG = debug

    if not _API_KEY:
        raise Exception('Kaput API key required')

    if not _PROJECT_ID:
        raise Exception('Project ID required')

    if patch:
        # Use a hook to capture and report exceptions.
        # TODO: Support chaining user/third-party excepthooks. This overwrites
        # them currently.
        sys.excepthook = _handle_exception

        if _DEBUG:
            logging.debug('Kaput exception hook enabled')


def handle_exception(exc):
    """Capture the exception information and send it to the Kaput service for
    processing.
    """

    _handle_exception(exc.__class__, exc, sys.exc_traceback)


def _handle_exception(exc_type, exc_value, exc_traceback):
    """Capture the exception information and send it to the Kaput service for
    processing.
    """

    frames = traceback.extract_tb(exc_traceback)

    payload = {
        'project_id': _PROJECT_ID,
        'timestamp': time.time(),
        'exception': exc_type.__name__,
        'message': exc_value.message,
        'frames': frames,
        'stacktrace': traceback.format_exc()
    }

    # TODO: Make requests asynchronously.
    # TODO: Handle retries.
    _HTTP.request('%s%s' % (_SERVICE_HOST, _SERVICE_ENDPOINT),
                  method='POST',
                  headers={'kaput-api-key': _API_KEY,
                           'Content-Type': 'application/json'},
                  body=json.dumps(payload))

    if _DEBUG:
        logging.debug('Kaput service request sent')

    # Pass through to default hook.
    return sys.__excepthook__(exc_type, exc_value, exc_traceback)

