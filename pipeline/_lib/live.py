"""The check on the deployed site, run once Pages' edge cache (about 10 minutes, research/04
section 6) has had time to serve the new Feed."""

import urllib.error
import urllib.request
import xml.etree.ElementTree as ET


def live_problems(base: str, episodes: list[dict]) -> list[str]:
    """What the live site gets wrong: Apple needs HEAD and range answers for the Cover and
    every enclosure, and the Feed must carry exactly the registry's guids."""
    problems = []
    try:
        feed = ET.fromstring(_get(f"{base}/feed.xml"))
    except (OSError, ET.ParseError) as error:
        return [f"{base}/feed.xml: {error}"]
    enclosures = {
        item.findtext("guid"): item.find("enclosure").get("url") for item in feed.iter("item")
    }
    expected = {episode["guid"]: episode for episode in episodes}
    problems += [
        f"Feed has guid {guid}, not in the registry" for guid in enclosures.keys() - expected.keys()
    ]
    problems += [
        f"Feed is missing {expected[guid]['episode_id']} (guid {guid})"
        for guid in expected.keys() - enclosures.keys()
    ]

    urls = {f"{base}/cover.png": None, f"{base}/archive.html": None}
    urls |= {url: expected[guid]["bytes"] for guid, url in enclosures.items() if guid in expected}
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
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()


def _head(url: str) -> int:
    request = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(request, timeout=60) as response:
        return int(response.headers.get("Content-Length", -1))


def _range(url: str) -> int:
    request = urllib.request.Request(url, headers={"Range": "bytes=0-99"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.status
