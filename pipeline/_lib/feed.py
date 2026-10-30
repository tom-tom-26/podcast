"""The Feed: RSS 2.0 with the iTunes and podcast namespaces, and the checks research/04 section 10
sets for it (constraints 1-4)."""

import html
import re
import xml.etree.ElementTree as ET
from email.utils import format_datetime, parsedate_to_datetime
from pathlib import Path

from pipeline._lib.encode import duration_seconds

DECLARATION = '<?xml version="1.0" encoding="UTF-8"?>'
NS = {
    "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
    "podcast": "https://podcastindex.org/namespace/1.0",
    "content": "http://purl.org/rss/1.0/modules/content/",
}
# Apple's top-level categories, https://podcasters.apple.com/support/1691-apple-podcasts-categories
CATEGORIES = {
    "Arts", "Business", "Comedy", "Education", "Fiction", "Government", "History",
    "Health & Fitness", "Kids & Family", "Leisure", "Music", "News",
    "Religion & Spirituality", "Science", "Society & Culture", "Sports", "Technology",
    "True Crime", "TV & Film",
}  # fmt: skip
CHANNEL_TAGS = [
    "title", "description", "language", "link", "copyright",
    "itunes:author", "itunes:type", "itunes:explicit",
]  # fmt: skip
ITEM_TAGS = [
    "title", "description", "guid", "pubDate",
    "itunes:duration", "itunes:explicit", "itunes:episodeType",
]  # fmt: skip
# Anything that could carry the owner's name or email (user story 53).
OWNER_TAGS = ["itunes:owner", "itunes:email", "managingEditor", "webMaster"]
AUDIO_TYPE = "audio/x-m4a"


def build_feed(show: dict, base: str, items: list[dict]) -> str:
    explicit = str(show["explicit"]).lower()
    lines = [
        DECLARATION,
        '<rss version="2.0" '
        + " ".join(f'xmlns:{prefix}="{uri}"' for prefix, uri in NS.items())
        + ">",
        "<channel>",
        f"<title>{_escape(show['title'])}</title>",
        f"<link>{_escape(base)}/archive.html</link>",
        f"<description>{_escape(show['description'])}</description>",
        f"<language>{_escape(show['language'])}</language>",
        f"<copyright>{_escape(show['copyright'])}</copyright>",
        f"<itunes:author>{_escape(show['author'])}</itunes:author>",
        f'<itunes:category text="{_escape(show["category"])}"/>',
        f"<itunes:explicit>{explicit}</itunes:explicit>",
        f"<itunes:type>{_escape(show['type'])}</itunes:type>",
        f'<itunes:image href="{_escape(base)}/cover.png"/>',
        # Keeps the show out of Apple's directory and podcast indexes; Follow by URL still works.
        "<itunes:block>Yes</itunes:block>",
        "<podcast:block>yes</podcast:block>",
    ]
    for item in items:
        lines += [
            "<item>",
            f"<title>{_escape(item['title'])}</title>",
            f"<description>{_escape(show_notes_html(item['notes']))}</description>",
            f'<enclosure url="{_escape(item["url"])}" length="{item["bytes"]}" '
            f'type="{AUDIO_TYPE}"/>',
            f'<guid isPermaLink="false">{_escape(item["guid"])}</guid>',
            f"<pubDate>{format_datetime(item['published'])}</pubDate>",
            f"<itunes:duration>{item['duration']}</itunes:duration>",
            f"<itunes:explicit>{explicit}</itunes:explicit>",
            f"<itunes:episodeType>{'bonus' if item['bonus'] else 'full'}</itunes:episodeType>",
            "</item>",
        ]
    lines += ["</channel>", "</rss>", ""]
    return "\n".join(lines)


def show_notes_html(notes: str) -> str:
    """Show notes as the little HTML Apple shows: paragraphs, bullet lists and links."""
    blocks = []
    for block in re.split(r"\n\s*\n", notes.strip()):
        lines = [line.strip() for line in block.splitlines()]
        if all(line.startswith("- ") for line in lines):
            blocks.append("<ul>" + "".join(f"<li>{_inline(li[2:])}</li>" for li in lines) + "</ul>")
        else:
            blocks.append(f"<p>{_inline(' '.join(lines))}</p>")
    return "".join(blocks)


def feed_problems(feed: str, base: str, site: Path) -> list[str]:
    """What in the built Feed breaks Apple's rules or disagrees with the site's audio."""
    problems = []
    if not feed.startswith(DECLARATION):
        problems.append(f"feed.xml: does not start with {DECLARATION}")
    problems += [
        f"feed.xml: no xmlns:{prefix} declaration"
        for prefix, uri in NS.items()
        if f'xmlns:{prefix}="{uri}"' not in feed
    ]
    try:
        rss = ET.fromstring(feed.encode("utf-8"))
    except ET.ParseError as error:
        return problems + [f"feed.xml: not well-formed XML: {error}"]
    if rss.tag != "rss" or rss.get("version") != "2.0":
        problems.append('feed.xml: root is not <rss version="2.0">')
    channel = rss.find("channel")
    if channel is None:
        return problems + ["feed.xml: no <channel>"]

    problems += _empty(channel, CHANNEL_TAGS, "channel")
    if not re.fullmatch(r"[a-z]{2}(-[A-Z]{2})?", channel.findtext("language") or ""):
        problems.append("channel: language is not an ISO code such as en-GB")
    categories = [c.get("text") for c in channel.findall("itunes:category", NS)]
    if not categories or any(c not in CATEGORIES for c in categories):
        problems.append(f"channel: itunes:category {categories} is not one of Apple's")
    problems += _true_or_false(channel, "channel")
    image = channel.find("itunes:image", NS)
    href = image.get("href", "") if image is not None else ""
    if not href.startswith(f"{base}/") or not href.endswith((".png", ".jpg")):
        problems.append(f"channel: itunes:image {href!r} is not a PNG or JPG on this site")
    if channel.findtext("itunes:block", namespaces=NS) != "Yes":
        problems.append("channel: no <itunes:block>Yes</itunes:block>")
    if channel.findtext("podcast:block", namespaces=NS) != "yes":
        problems.append("channel: no <podcast:block>yes</podcast:block>")
    problems += [f"channel: has <{tag}>" for tag in OWNER_TAGS if channel.find(tag, NS) is not None]

    items = channel.findall("item")
    if not items:
        problems.append("channel: no Episodes")
    guids, urls = set(), set()
    for item in items:
        guid = item.findtext("guid") or ""
        name = f"item {guid or item.findtext('title')}"
        problems += _empty(item, ITEM_TAGS, name)
        problems += _true_or_false(item, name)
        problems += [
            f"{name}: has <{tag}>"
            for tag in ("itunes:episode", "itunes:season")
            if item.find(tag, NS) is not None
        ]
        if item.findtext("itunes:episodeType", namespaces=NS) not in ("full", "bonus"):
            problems.append(f"{name}: itunes:episodeType is not full or bonus")
        if guid in guids:
            problems.append(f"{name}: guid used by another item")
        guids.add(guid)
        try:
            if parsedate_to_datetime(item.findtext("pubDate")).tzinfo is None:
                problems.append(f"{name}: pubDate has no zone offset")
        except (TypeError, ValueError):
            problems.append(f"{name}: pubDate is not an RFC 2822 date")

        enclosure = item.find("enclosure")
        if enclosure is None:
            problems.append(f"{name}: no enclosure")
            continue
        url, length = enclosure.get("url", ""), enclosure.get("length", "")
        if not enclosure.get("type"):
            problems.append(f"{name}: enclosure has no type")
        if url in urls:
            problems.append(f"{name}: enclosure URL used by another item")
        urls.add(url)
        if not url.isascii() or not url.startswith(f"{base}/"):
            problems.append(f"{name}: enclosure URL {url!r} is not an ASCII URL on this site")
            continue
        audio = site / url.removeprefix(f"{base}/")
        if not audio.is_file():
            problems.append(f"{name}: enclosure {url} is not in the site")
            continue
        if length != str(audio.stat().st_size):
            problems.append(
                f"{name}: enclosure length {length} but {audio.name} is "
                f"{audio.stat().st_size} bytes"
            )
        duration = item.findtext("itunes:duration", namespaces=NS) or ""
        if not duration.isdigit():
            problems.append(f"{name}: itunes:duration {duration!r} is not whole seconds")
        elif abs(int(duration) - duration_seconds(audio)) > 1:
            problems.append(
                f"{name}: itunes:duration {duration} s but {audio.name} runs "
                f"{duration_seconds(audio)} s"
            )
    return problems


def _escape(text: str) -> str:
    # research/04: &apos; and &quot;, never HTML entities such as &rsquo;.
    return html.escape(str(text), quote=True).replace("&#x27;", "&apos;")


def _inline(text: str) -> str:
    return re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', html.escape(text, quote=True)
    )


def _empty(element: ET.Element, tags: list[str], name: str) -> list[str]:
    return [
        f"{name}: <{tag}> missing or empty"
        for tag in tags
        if not element.findtext(tag, namespaces=NS)
    ]


def _true_or_false(element: ET.Element, name: str) -> list[str]:
    if element.findtext("itunes:explicit", namespaces=NS) not in ("true", "false"):
        return [f"{name}: itunes:explicit is not true or false"]
    return []
