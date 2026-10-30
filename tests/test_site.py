import argparse
import re
import shutil
import subprocess
import threading
import time
import xml.etree.ElementTree as ET
from contextlib import contextmanager
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest
import yaml
from PIL import Image

from pipeline import site
from tests.fake_github import FakeGitHub

REPO = Path(__file__).parent.parent
BASE_URL = "https://example.test/podcast"
NS = {
    "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
    "podcast": "https://podcastindex.org/namespace/1.0",
    "content": "http://purl.org/rss/1.0/modules/content/",
}


@pytest.fixture
def repo(tmp_path, smoke_bundle):
    """A repo with two published Episodes: the smoke Bundle, then a second about tides."""
    root = tmp_path / "repo"
    for path in ["config/show.yaml", "config/voices.yaml", "artwork/cover.png"]:
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO / path, root / path)
    shutil.copytree(smoke_bundle, root / "bundles" / "2026-10-30-smoke")
    tides = shutil.copytree(smoke_bundle, root / "bundles" / "2026-11-02-tides")
    meta = yaml.safe_load((tides / "meta.yaml").read_text(encoding="utf-8"))
    meta.update(title="How tides work", summary="Why the sea rises twice a day.")
    (tides / "meta.yaml").write_text(yaml.safe_dump(meta), encoding="utf-8")
    (tides / "show_notes.md").write_text(
        'The Moon pulls the sea & the Sun helps.\n\nSources\n\n- NOAA, "Tides"\n',
        encoding="utf-8",
    )
    github = FakeGitHub()
    episodes = []
    for number, bundle_id, seconds, published_at in [
        (1, "2026-10-30-smoke", 3, "2026-10-30T09:00:00Z"),
        (2, "2026-11-02-tides", 4, "2026-11-02T18:30:00Z"),
    ]:
        episode_id = f"ep-{number:03d}-{bundle_id.split('-', 3)[3]}"
        audio = tone_m4a(tmp_path / "releases" / f"{episode_id}.m4a", seconds)
        github.add_published_release(episode_id, audio, published_at)
        episodes.append(
            {
                "number": str(number),
                "episode_id": episode_id,
                "bundle_id": bundle_id,
                "guid": f"00000000-0000-4000-8000-00000000000{number}",
                "voice": "bm_george",
                "file": audio.name,
                "bytes": audio.stat().st_size,
                "duration": seconds,
            }
        )
    write_registry(root, episodes)
    return root, github


def test_feed_carries_the_channel_fields_from_the_show_config(repo, tmp_path):
    root, github = repo

    assert build_site(root, tmp_path / "_site", github) == 0

    channel = feed(tmp_path / "_site").find("channel")
    assert channel.findtext("title") == "Plainly Put"
    assert channel.findtext("description").startswith("One topic per episode")
    assert channel.findtext("language") == "en-GB"
    assert channel.findtext("copyright") == "© 2026 Plainly Put"
    assert channel.findtext("link") == f"{BASE_URL}/archive.html"
    assert channel.findtext("itunes:author", namespaces=NS) == "Plainly Put"
    assert channel.find("itunes:category", NS).get("text") == "Education"
    assert channel.findtext("itunes:explicit", namespaces=NS) == "false"
    assert channel.findtext("itunes:type", namespaces=NS) == "episodic"
    assert channel.find("itunes:image", NS).get("href") == f"{BASE_URL}/cover.png"
    assert channel.findtext("itunes:block", namespaces=NS) == "Yes"
    assert channel.findtext("podcast:block", namespaces=NS) == "yes"
    assert channel.find("itunes:owner", NS) is None
    assert "@" not in (tmp_path / "_site" / "feed.xml").read_text(encoding="utf-8")


def test_items_are_the_registry_newest_first_with_enclosure_guid_and_dates(repo, tmp_path):
    root, github = repo
    out = tmp_path / "_site"

    assert build_site(root, out, github) == 0

    tides, smoke = feed(out).find("channel").findall("item")
    assert tides.findtext("title") == "Episode 2: How tides work"
    assert smoke.findtext("title") == "Episode 1: Why the sky is blue"
    assert tides.findtext("guid") == "00000000-0000-4000-8000-000000000002"
    assert tides.find("guid").get("isPermaLink") == "false"
    assert tides.findtext("pubDate") == "Mon, 02 Nov 2026 18:30:00 +0000"
    assert tides.findtext("itunes:duration", namespaces=NS) == "4"
    assert tides.findtext("itunes:explicit", namespaces=NS) == "false"
    assert tides.findtext("itunes:episodeType", namespaces=NS) == "full"
    assert tides.find("itunes:episode", NS) is None
    assert tides.find("itunes:season", NS) is None
    enclosure = tides.find("enclosure")
    assert enclosure.get("url") == f"{BASE_URL}/audio/ep-002-tides.m4a"
    assert enclosure.get("type") == "audio/x-m4a"
    audio = out / "audio" / "ep-002-tides.m4a"
    assert audio.read_bytes() == github.audio["ep-002-tides", "ep-002-tides.m4a"]
    assert enclosure.get("length") == str(audio.stat().st_size)


def test_feed_starts_with_apples_declaration_and_escapes_quotes(repo, tmp_path):
    root, github = repo
    out = tmp_path / "_site"

    assert build_site(root, out, github) == 0

    text = (out / "feed.xml").read_text(encoding="utf-8")
    assert text.startswith('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" ')
    assert "&amp;quot;Tides&amp;quot;" in text


def test_item_description_is_the_show_notes(repo, tmp_path):
    root, github = repo
    out = tmp_path / "_site"

    assert build_site(root, out, github) == 0

    tides = feed(out).find("channel").find("item")
    assert tides.findtext("description") == (
        "<p>The Moon pulls the sea &amp; the Sun helps.</p><p>Sources</p>"
        "<ul><li>NOAA, &quot;Tides&quot;</li></ul>"
    )


def test_a_cc_by_voice_gets_its_credit_line_and_a_kokoro_voice_none(repo, tmp_path):
    root, github = repo
    credit = "Voice: alba, Kyutai Pocket TTS voices, CC BY 4.0"
    roster = {"voices": {"bm_george": {"engine": "kokoro"}, "alba": {"credit": credit}}}
    (root / "config" / "voices.yaml").write_text(yaml.safe_dump(roster), encoding="utf-8")
    episodes = registry(root)
    episodes[1]["voice"] = "alba"
    write_registry(root, episodes)
    out = tmp_path / "_site"

    assert build_site(root, out, github) == 0

    tides, smoke = feed(out).find("channel").findall("item")
    assert tides.findtext("description").endswith(f"<p>{credit}</p>")
    assert "Voice:" not in smoke.findtext("description")


def test_a_qa_episode_is_a_bonus_item(repo, tmp_path):
    root, github = repo
    episodes = registry(root)
    episodes[1]["number"] = "1q"
    write_registry(root, episodes)
    out = tmp_path / "_site"

    assert build_site(root, out, github) == 0

    qa, smoke = feed(out).find("channel").findall("item")
    assert qa.findtext("title") == "Episode 1q: How tides work"
    assert qa.findtext("itunes:episodeType", namespaces=NS) == "bonus"
    assert smoke.findtext("itunes:episodeType", namespaces=NS) == "full"


def test_archive_page_lists_every_episode_newest_first_and_is_noindex(repo, tmp_path):
    root, github = repo
    out = tmp_path / "_site"

    assert build_site(root, out, github) == 0

    page = (out / "archive.html").read_text(encoding="utf-8")
    assert '<meta name="robots" content="noindex, nofollow">' in page
    assert "<p>Every episode of Plainly Put so far, newest first.</p>" in page
    assert page.index("Episode 2: How tides work") < page.index("Episode 1: Why the sky is blue")
    assert (
        '<li><a href="https://github.com/example/podcast/releases/download/ep-002-tides/'
        'ep-002-tides.m4a">Episode 2: How tides work</a>'
        "<br>2 November 2026, 1 min<br>Why the sea rises twice a day.</li>"
    ) in page
    assert "feed.xml" not in page


def test_site_has_robots_txt_disallowing_everything_and_the_cover(repo, tmp_path):
    root, github = repo
    out = tmp_path / "_site"

    assert build_site(root, out, github) == 0

    assert (out / "robots.txt").read_text(encoding="utf-8") == "User-agent: *\nDisallow: /\n"
    assert (out / "cover.png").read_bytes() == (REPO / "artwork" / "cover.png").read_bytes()


def test_a_window_file_that_cannot_be_fetched_fails_the_build(repo, tmp_path, capsys):
    root, github = repo
    del github.audio["ep-001-smoke", "ep-001-smoke.m4a"]
    out = tmp_path / "_site"

    assert build_site(root, out, github) == 1

    assert "could not fetch ep-001-smoke.m4a for ep-001-smoke" in capsys.readouterr().err
    assert not (out / "feed.xml").exists()


def test_an_enclosure_length_that_is_not_the_files_bytes_fails_the_build(repo, tmp_path, capsys):
    root, github = repo
    episodes = registry(root)
    episodes[0]["bytes"] += 1
    write_registry(root, episodes)

    assert build_site(root, tmp_path / "_site", github) == 1

    assert "enclosure length" in capsys.readouterr().err


def test_a_duration_that_is_not_the_files_fails_the_build(repo, tmp_path, capsys):
    root, github = repo
    episodes = registry(root)
    episodes[0]["duration"] = 60
    write_registry(root, episodes)

    assert build_site(root, tmp_path / "_site", github) == 1

    assert "itunes:duration 60 s but ep-001-smoke.m4a runs 3 s" in capsys.readouterr().err


def test_a_category_apple_does_not_list_fails_the_build(repo, tmp_path, capsys):
    root, github = repo
    show = root / "config" / "show.yaml"
    show.write_text(
        show.read_text(encoding="utf-8").replace("Education", "Learning"), encoding="utf-8"
    )

    assert build_site(root, tmp_path / "_site", github) == 1

    assert "itunes:category ['Learning'] is not one of Apple's" in capsys.readouterr().err


def test_a_cover_with_alpha_fails_the_build(repo, tmp_path, capsys):
    root, github = repo
    Image.new("RGBA", (3000, 3000)).save(root / "artwork" / "cover.png")

    assert build_site(root, tmp_path / "_site", github) == 1

    assert "colour type 6" in capsys.readouterr().err


def test_live_check_passes_when_the_site_answers_head_and_range(repo, tmp_path):
    root, github = repo
    out = tmp_path / "_site"
    with serve(out) as base_url:
        assert build_site(root, out, github, base_url) == 0

        assert check_site(root, base_url) == 0


def test_live_check_fails_on_missing_audio_or_a_guid_the_feed_lacks(repo, tmp_path, capsys):
    root, github = repo
    out = tmp_path / "_site"
    with serve(out) as base_url:
        assert build_site(root, out, github, base_url) == 0
        (out / "audio" / "ep-001-smoke.m4a").unlink()
        episodes = registry(root)
        episodes.append({**episodes[1], "episode_id": "ep-003-tides", "guid": "not-deployed"})
        write_registry(root, episodes)

        assert check_site(root, base_url) == 1

    err = capsys.readouterr().err
    assert f"{base_url}/audio/ep-001-smoke.m4a: HTTP Error 404" in err
    assert "Feed is missing ep-003-tides (guid not-deployed)" in err


@pytest.fixture
def bare_site(tmp_path, monkeypatch):
    """A deployed site with no Episodes, and a record of each wait between retries."""
    root = tmp_path / "repo"
    root.mkdir()
    write_registry(root, [])
    out = tmp_path / "_site"
    out.mkdir()
    (out / "feed.xml").write_text("<rss><channel></channel></rss>", encoding="utf-8")
    (out / "archive.html").write_text("<html></html>", encoding="utf-8")
    shutil.copy(REPO / "artwork" / "cover.png", out / "cover.png")
    waits = []
    monkeypatch.setattr(time, "sleep", waits.append)
    return root, out, waits


def test_live_check_retries_a_failed_request_and_passes_when_it_recovers(bare_site):
    root, out, waits = bare_site
    with serve(out, failures={"/feed.xml": 2}) as base_url:
        assert check_site(root, base_url) == 0

    assert len(waits) == 2
    assert all(0 < wait <= 10 for wait in waits)


def test_live_check_gives_up_after_two_retries(bare_site, capsys):
    root, out, waits = bare_site
    with serve(out, failures={"/feed.xml": 3}) as base_url:
        assert check_site(root, base_url) == 1

    assert len(waits) == 2
    assert f"{base_url}/feed.xml: HTTP Error 503" in capsys.readouterr().err


def test_live_check_does_not_retry_a_missing_file(bare_site, capsys):
    root, out, waits = bare_site
    (out / "cover.png").unlink()
    with serve(out) as base_url:
        assert check_site(root, base_url) == 1

    assert waits == []
    assert "cover.png: HTTP Error 404" in capsys.readouterr().err


def build_site(root, out, github, base_url=BASE_URL):
    args = site_args("--repo", root, "--out", out, "--base-url", base_url)
    return site.main(args, github=github)


def check_site(root, base_url):
    return site.main(site_args("--repo", root, "--base-url", base_url, "--check"))


def site_args(*argv):
    parser = argparse.ArgumentParser()
    site.add_arguments(parser)
    return parser.parse_args([str(arg) for arg in argv])


def feed(out):
    return ET.parse(out / "feed.xml").getroot()


def registry(root):
    return yaml.safe_load((root / "episodes.yaml").read_text(encoding="utf-8"))["episodes"]


def write_registry(root, episodes):
    text = yaml.safe_dump({"episodes": episodes}, sort_keys=False)
    (root / "episodes.yaml").write_text(text, encoding="utf-8")


def tone_m4a(path, seconds):
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-v", "error", "-f", "lavfi", "-i", f"sine=frequency=200:duration={seconds}",
         "-ac", "1", "-c:a", "aac", "-b:a", "64k", "-y", str(path)],
        check=True,
    )  # fmt: skip
    return path


@contextmanager
def serve(folder, failures=None):
    """Serve a folder over HTTP, answering HEAD and byte-range requests as Pages does.
    failures maps a path to how many GETs of it answer 503 first."""
    failures = dict(failures or {})

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(folder), **kwargs)

        def do_GET(self):
            if failures.get(self.path, 0) > 0:
                failures[self.path] -= 1
                return self.send_error(503)
            match = re.fullmatch(r"bytes=(\d+)-(\d+)", self.headers.get("Range", ""))
            path = Path(self.translate_path(self.path))
            if not match or not path.is_file():
                return super().do_GET()
            data = path.read_bytes()
            start, end = int(match[1]), min(int(match[2]), len(data) - 1)
            self.send_response(206)
            self.send_header("Content-Range", f"bytes {start}-{end}/{len(data)}")
            self.send_header("Content-Length", str(end - start + 1))
            self.end_headers()
            self.wfile.write(data[start : end + 1])

        def log_message(self, *args):
            pass

    folder.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
