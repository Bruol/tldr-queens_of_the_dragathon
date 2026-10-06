"""Compare a running Cloudflare deployment with the original Django views."""
import contextlib
import io
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'TLDRserver'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TLDRserver.settings')
import django
django.setup()
from django.test import Client
from TLDR.models import Lecture, Video

base = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'http://localhost:8787'
client = Client()
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (TLDR archive verification)')]
urllib.request.install_opener(opener)
paths = ['/', '/about']
paths += [f'/classes/{pk}/' for pk in Lecture.objects.values_list('pk', flat=True)]
paths += [f'/transcripts/{pk}/' for pk in Video.objects.values_list('pk', flat=True)]
paths += [f'/download/{pk}/' for pk in Video.objects.values_list('pk', flat=True)]
for path in paths:
    with contextlib.redirect_stdout(io.StringIO()):
        expected = client.get(path, HTTP_HOST='localhost')
    actual = urllib.request.urlopen(base + path, timeout=30)
    assert actual.read() == expected.content, path
    if path.startswith('/download/'):
        disposition = actual.headers['Content-Disposition']
        filename = urllib.parse.unquote(disposition.split("filename*=UTF-8''", 1)[1])
        assert expected['Content-Disposition'] == f'attachment; filename="{filename}"', path
queries = ['', 'graphics', 'GRAPHICS', 'zz-no-results-zz', '<script>"&', '%', '_', 'Ü']
for query in queries:
    path = '/search/?' + urllib.parse.urlencode({'query': query})
    with contextlib.redirect_stdout(io.StringIO()):
        expected = client.get(path, HTTP_HOST='localhost').content.decode()
    actual = urllib.request.urlopen(base + path, timeout=30).read().decode()
    assert re.findall(r"window.location='([^']+)'", expected) == re.findall(r"window.location='([^']+)'", actual), query
    assert ('id="no-results" hidden' in actual) == ('No results found.' not in expected), query
    from html import unescape
    value = re.search(r'name="query" value="([^"]*)"', actual).group(1)
    assert unescape(value) == query, query
for path in ['/classes/999999/', '/transcripts/999999/', '/download/999999/', '/admin/']:
    try:
        urllib.request.urlopen(base + path, timeout=30)
        raise AssertionError(f'{path} should return 404')
    except urllib.error.HTTPError as error:
        assert error.code == 404, (path, error.code)
print(f'PASS: {len(paths)} unchanged pages/downloads, attachment headers, {len(queries)} searches, and missing routes.')
