"""The check on the deployed site, run once Pages' edge cache (about 10 minutes, research/04
section 6) has had time to serve the new Feed."""

import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

from pipeline._lib.network import retry


def live_problems(base: str, feeds: dict[str, list[dict]]) -> list[str]:
    """What the live site gets wrong: Apple needs HEAD and range answers for the Cover and
    every enclosure, and each Feed (by its path on the site) must carry exactly its Episodes'
    guids."""
    problems = []
    urls = {f"{base}/cover.png": None, f"{base}/archive.html": None}
    for path, episodes in feeds.items():
        try:
            feed = ET.fromstring(_get(f"{base}/{path}"))
        except (OSError, ET.ParseError) as error:
            problems.append(f"{base}/{path}: {error}")
            continue
        enclosures = {}
        for item in feed.iter("item"):
            enclosure = item.find("enclosure")
            if enclosure is None:
                problems.append(f"{path} item {item.findtext('guid')} has no enclosure")
            else:
                enclosures[item.findtext("guid")] = enclosure.get("url")
        expected = {episode["guid"]: episode for episode in episodes}
        problems += [
            f"{path} has guid {guid}, not in its registry"
            for guid in enclosures.keys() - expected.keys()
        ]
        problems += [
            f"{path} is missing {expected[guid]['episode_id']} (guid {guid})"
            for guid in expected.keys() - enclosures.keys()
        ]
        urls |= {
            url: expected[guid]["bytes"] for guid, url in enclosures.items() if guid in expected
        }

    for url, size in urls.items():
        try:
            length = _head(url)
            if size is not None and length != size:
                problems.append(f"HEAD {url}: Content-Length {length}, registry says {size}")
            if url.endswith(".html"):
                continue
            status = _range(url)
            if status != 206:
                problems.append(f"GET {url} with Range: answered {status}, not 206")
        except OSError as error:
            problems.append(f"{url}: {error}")
    return problems


def _get(url: str) -> bytes:
    def get():
        with urllib.request.urlopen(url, timeout=60) as response:
            return response.read()

    return retry(get, f"GET {url}")


def _head(url: str) -> int:
    def head():
        request = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(request, timeout=60) as response:
            return int(response.headers.get("Content-Length", -1))

    return retry(head, f"HEAD {url}")


def _range(url: str) -> int:
    def get_range():
        request = urllib.request.Request(url, headers={"Range": "bytes=0-99"})
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status

    return retry(get_range, f"GET {url} with Range")
