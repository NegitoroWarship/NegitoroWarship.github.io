#!/usr/bin/env python3
"""Regenerate the redirect pages for the old GitHub Pages URLs of Lines in Still Water.

The blog was served from negitorowarship.github.io, first as a project site
under /blog/ and then from the user-site root. Every path it had in either era
gets an index.html with an instant meta refresh and a canonical link to the
same page on the new origin, which Google treats as a permanent redirect.
Anything else falls through to 404.html, which redirects visitors only.

Change BASE or PATHS, run this script, and commit the result.
"""

from pathlib import Path

BASE = "https://blog.negitorowarship.workers.dev"

# Search Console's HTML-tag verification for the github.io property.
VERIFICATION = "WHejNE_OkojkP_h6Bj6BjP4aja8C9JdY4BQeAtGu0wM"

# Paths from the user-site era; each is also served under /blog/ for the
# project-site era. Both redirect to the same path on BASE.
PATHS = [
    "/",
    "/journal/",
    "/about/",
    "/notes/",
    "/sitemap/",
    "/posts/building-a-63-key-asymmetric-dactyl-manuform/",
]

ROOT = Path(__file__).resolve().parent
HOST = BASE.split("://", 1)[1]

# No noindex here: it would contradict the canonical link to the new page.
STUB = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved to HOST</title>
EXTRA<link rel="canonical" href="TARGET">
<meta http-equiv="refresh" content="0; url=TARGET">
<script>location.replace("TARGET" + location.hash);</script>
</head>
<body><p>This site has moved to <a href="TARGET">TARGET</a>.</p></body>
</html>
"""

NOT_FOUND = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved to HOST</title>
<meta name="robots" content="noindex">
<script>location.replace("BASE" + (location.pathname.replace(/^\\/blog(?=\\/|$)/, "") || "/") + location.search + location.hash);</script>
</head>
<body><p>This site has moved to <a href="BASE/">BASE/</a>.</p></body>
</html>
"""


def write(path, content):
    file = ROOT / path.lstrip("/")
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content, encoding="utf-8")


def stub(target, extra=""):
    return STUB.replace("HOST", HOST).replace("EXTRA", extra).replace("TARGET", target)


for path in PATHS:
    target = BASE + path
    verification = (
        f'<meta name="google-site-verification" content="{VERIFICATION}">\n'
        if path == "/"
        else ""
    )
    write(path + "index.html", stub(target, verification))
    write("/blog" + path + "index.html", stub(target))

write("/404.html", NOT_FOUND.replace("HOST", HOST).replace("BASE", BASE))
write("/robots.txt", "User-agent: *\nAllow: /\n")
write("/.nojekyll", "")
