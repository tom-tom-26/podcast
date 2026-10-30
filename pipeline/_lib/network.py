"""The one retry the Pipeline allows, for network calls only: at most two more tries after a
short wait. A local failure, or an answer that will not change, fails at once."""

import sys
import time
import urllib.error

RETRIES = 2
WAIT_SECONDS = 5


def retry(call, what: str):
    for attempt in range(RETRIES + 1):
        try:
            return call()
        except (TimeoutError, urllib.error.URLError, ConnectionError) as error:
            if attempt == RETRIES or not _transient(error):
                raise
            print(f"{what}: {error}; retrying in {WAIT_SECONDS} s", file=sys.stderr)
            time.sleep(WAIT_SECONDS)


def _transient(error: OSError) -> bool:
    # A 404 or 403 says the same thing the second time; a 5xx or 429 may not.
    if isinstance(error, urllib.error.HTTPError):
        return error.code >= 500 or error.code == 429
    return True
