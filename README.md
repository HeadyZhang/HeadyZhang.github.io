# Heady Zhang — portfolio

A static, dependency-free portfolio for GitHub Pages. All visitor-facing content renders without JavaScript; the small script enhances the mobile navigation.

## Edit and preview

Edit project narratives, dates, research, and links in `scripts/content.json`. Shared layout and the home page are rendered by `scripts/build.py`; styles live in `assets/style.css`.

```sh
python3 scripts/build.py
python3 scripts/check_site.py
python3 -m http.server 4173 --bind 127.0.0.1
```

Visit `http://127.0.0.1:4173`. Commit generated HTML alongside its source. No build service, package installation, or runtime framework is required to deploy.

## Publishing

The existing GitHub Pages configuration serves the root of `main`. Use a normal fast-forward or pull request merge into `main`; do not force-push. Directory-based case-study routes work on direct navigation and refresh. `.nojekyll` disables unnecessary processing.

## Content maintenance

Keep project evidence scoped to the milestone and measurement it supports. The public summary intentionally excludes private source repositories, client reports, and personal phone numbers. Review dated metrics before updating them. Research links point to public primary sources and do not imply publication acceptance.
