"""Check generated routes, fragments, metadata, link policy, and privacy regressions."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT / 'index.html', ROOT / '404.html', *sorted((ROOT / 'work').glob('*/index.html'))]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = []
        self.references = []
        self.headings = []
        self.main = 0
        self.canonical = 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.headings.append(int(tag[1]))
        if tag == 'main':
            self.main += 1
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical += 1
        if tag == 'a' and attrs.get('href', '').startswith('https://'):
            assert attrs.get('target') == '_blank', (self.path, attrs)
            assert {'noopener', 'noreferrer'} <= set(attrs.get('rel', '').split()), (self.path, attrs)
        for field in ['href', 'src']:
            if field in attrs:
                self.references.append(attrs[field])


pages = {p: Page(p) for p in FILES}
externals = set()
for path, page in pages.items():
    assert len(page.ids) == len(set(page.ids)), f'Duplicate IDs: {path}'
    assert page.main == 1 and page.headings.count(1) == 1, f'Landmark or h1: {path}'
    assert page.canonical == 1, f'Canonical: {path}'
    assert all(b <= a + 1 for a, b in zip(page.headings, page.headings[1:])), f'Heading order: {path}'
    text = path.read_text()
    for forbidden in [r'/Users/', r'/private/', r'(?i)\bTODO\b', r'(?i)\bplaceholder\b', r'\+1[ -]?213', r'(?i)building Argus', r'(?i)globally unique', r'(?i)production-grade', r'(?i)industrial-grade', r'(?i)85\+ rules', r'(?i)Java(?:[ ,<])']:
        assert not re.search(forbidden, text), f'Forbidden content {forbidden}: {path}'
    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', text).group(1)
    assert json.loads(ld)['@type'] == 'Person'
    for ref in page.references:
        parts = urlsplit(ref)
        if parts.scheme in ['https', 'http', 'mailto']:
            if parts.scheme != 'mailto':
                externals.add(ref)
            continue
        target = ROOT / unquote(parts.path).lstrip('/') if parts.path.startswith('/') else path.parent / unquote(parts.path)
        if not parts.path:
            target = path
        if target.is_dir():
            target /= 'index.html'
        assert target.is_file(), f'Missing target: {path}: {ref}'
        if parts.fragment:
            target_page = pages.get(target) or Page(target)
            assert unquote(parts.fragment) in target_page.ids, f'Missing fragment: {path}: {ref}'
print(f'PASS: {len(pages)} pages; all internal routes, assets, fragments, headings, landmarks, metadata, external-link attributes, and privacy regressions.')
print('External destinations:')
print('\n'.join(sorted(externals)))
