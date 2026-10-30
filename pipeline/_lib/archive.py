import html


def archive_html(show: dict, items: list[dict]) -> str:
    """The Archive page: one plain sentence, then every Episode newest first (research/18 I9)."""
    title = html.escape(show["title"])
    rows = []
    for item in items:
        published = item["published"]
        minutes = max(1, round(item["duration"] / 60))
        rows.append(
            f'<li><a href="{html.escape(item["release_url"])}">{html.escape(item["title"])}</a>'
            f"<br>{published.day} {published:%B %Y}, {minutes} min"
            f"<br>{html.escape(item['summary'])}</li>"
        )
    return "\n".join(
        [
            "<!doctype html>",
            f'<html lang="{html.escape(show["language"])}">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="robots" content="noindex, nofollow">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{title}</title>",
            "</head>",
            "<body>",
            f"<p>Every episode of {title} so far, newest first.</p>",
            "<ul>",
            *rows,
            "</ul>",
            "</body>",
            "</html>",
            "",
        ]
    )
