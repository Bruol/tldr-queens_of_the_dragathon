"""Export the public Django views, retaining their URLs and existing templates."""
import contextlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "TLDRserver"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TLDRserver.settings")
import django
django.setup()
from django.test import Client
from TLDR.models import Lecture, Topic, Video


def build():
    output = ROOT / "cloudflare" / "dist"
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()
    client = Client()
    paths = ["/", "/about", "/search/"]
    paths += [f"/classes/{pk}/" for pk in Lecture.objects.values_list("pk", flat=True)]
    paths += [f"/transcripts/{pk}/" for pk in Video.objects.values_list("pk", flat=True)]
    paths += [f"/download/{pk}/" for pk in Video.objects.values_list("pk", flat=True)]
    search = list(Topic.objects.values("id", "summary"))
    for path in paths:
        with contextlib.redirect_stdout(io.StringIO()):
            response = client.get(path, HTTP_HOST="localhost")
        if response.status_code != 200:
            raise RuntimeError(f"{path}: HTTP {response.status_code}")
        content = response.content
        if path == "/search/":
            ids = iter(row["id"] for row in search)
            html = re.sub(r'<div class="course-card"', lambda _: f'<div data-topic-id="{next(ids)}" class="course-card"', content.decode())
            html = html.replace('<div class="cards">', '<div class="cards"><p id="no-results" hidden>No results found.</p>')
            content = html.encode()
        target = output / path.lstrip("/")
        target = target / "index.html" if path.endswith("/") else target.with_suffix(".html")
        if path.startswith("/download/"):
            target = output / path.strip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    shutil.copytree(ROOT / "TLDRserver/TLDR/templates/styles", output / "static")
    headers = ["/*", "  X-Content-Type-Options: nosniff", "  X-Frame-Options: DENY", "  Referrer-Policy: same-origin", "  Cross-Origin-Opener-Policy: same-origin", ""]
    for route in ['/', '/about', '/classes/*', '/transcripts/*', '/search/*']:
        headers += [route, '  Content-Type: text/html; charset=utf-8', '']
    for video in Video.objects.select_related("lecture_id"):
        filename = f"{video.presentation_date:%Y-%m-%d}_{video.lecture_id.lecture_name}.md"
        fallback = filename.encode('ascii', 'replace').decode().replace('?', '_')
        disposition = f'attachment; filename="{fallback}"; filename*=UTF-8\'\'{quote(filename)}'
        headers += [f"/download/{video.pk}", "  Content-Type: text/plain; charset=utf-8", f'  Content-Disposition: {disposition}', ""]
    (output / "_headers").write_text("\n".join(headers))
    (ROOT / "cloudflare/search.json").write_text(json.dumps(search, ensure_ascii=False))
    print(f"Exported {len(paths)} public routes and {len(search)} searchable topics.")


if __name__ == "__main__":
    build()
