# Heady Zhang — portfolio

A static, dependency-free portfolio for GitHub Pages. All visitor-facing content renders without JavaScript; the small script enhances the mobile navigation.

## Edit and preview

Edit the hero results, project narratives, home cards, experience, research, and about text in `scripts/content.json`. Shared layout, the home page, and case studies are rendered by `scripts/build.py`; styles live in `assets/style.css`.

```sh
python3 scripts/build.py
python3 scripts/check_site.py
python3 -m http.server 4173 --bind 127.0.0.1
```

Visit `http://127.0.0.1:4173`. Commit generated HTML alongside its source. No build service, package installation, or runtime framework is required to deploy.

Content fields: `projects` are the case studies (the first one is the featured card); `home_cards` are the remaining home rows and may point at a project or at an in-page anchor; `prototype` is the research prototype shown under Research; `experience` entries carry bullet lists.

## Publishing

The existing GitHub Pages configuration serves the root of `main`. Use a normal fast-forward or pull request merge into `main`; do not force-push. Directory-based case-study routes work on direct navigation and refresh. `.nojekyll` disables unnecessary processing.

## Content maintenance

Keep project evidence scoped to the milestone and measurement it supports. The public summary intentionally excludes private source repositories, client reports, beta-program details, and personal phone numbers; a resume PDF is published only once a version without a phone number exists. Review dated metrics before updating them, and label counts whose definition changed (for example, agent-audit rule counts) rather than replacing one number with another. Research links point to public primary sources and do not imply publication acceptance.
