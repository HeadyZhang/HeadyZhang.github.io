"""Render a dependency-free static portfolio from one shared content source."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "scripts/content.json").read_text())
BASE = "https://headyzhang.github.io"
PROJECTS = {p['slug']: p for p in DATA['projects']}
e = html.escape


def external(url, label, css="external"):
    return f'<a class="{css}" href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)}<span aria-hidden="true"> ↗</span><span class="sr-only"> (opens in a new tab)</span></a>'


def nav():
    sections = ''.join(f'<a href="/#{s.lower()}">{s}</a>' for s in ['Work', 'Experience', 'Research', 'About', 'Contact'])
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-inner">
<a class="brand" href="/" aria-label="Heady Zhang, home"><span class="brand-mark" aria-hidden="true">HZ</span>heady.zhang</a>
<button class="menu-toggle" hidden aria-controls="navigation" aria-expanded="false">Menu <span aria-hidden="true">+</span></button>
<nav id="navigation" aria-label="Primary"><div class="nav-sections">{sections}</div><div class="nav-social">{external(DATA['github'], 'GitHub')}{external(DATA['linkedin'], 'LinkedIn')}</div></nav>
</div></header>'''


def footer():
    return '<footer class="wrap"><div class="site-footer"><span>© 2026 Haiyue Zhang</span><span>Los Angeles, CA · Built with care, grounded in evidence.</span></div></footer>'


def shell(title, description, route, body, kind="website"):
    person = {"@context": "https://schema.org", "@type": "Person", "name": "Haiyue Zhang", "alternateName": "Heady Zhang", "url": BASE + "/", "jobTitle": DATA['role'], "email": "mailto:" + DATA['email'], "sameAs": [DATA['github'], DATA['linkedin']], "alumniOf": [{"@type": "CollegeOrUniversity", "name": "University of Southern California"}, {"@type": "CollegeOrUniversity", "name": "Shanghai Jiao Tong University"}], "homeLocation": {"@type": "Place", "name": "Los Angeles, CA"}}
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#f7f7f2">
<link rel="canonical" href="{BASE}{route}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="{kind}"><meta property="og:url" content="{BASE}{route}"><meta property="og:site_name" content="Heady Zhang"><meta property="og:locale" content="en_US"><meta name="twitter:card" content="summary">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"><link rel="stylesheet" href="/assets/style.css"><script src="/assets/site.js" defer></script>
<script type="application/ld+json">{json.dumps(person, ensure_ascii=False)}</script></head><body>{nav()}{body}{footer()}</body></html>'''


def results():
    hero = DATA['hero']
    items = ''.join(f'<li><span class="result-kicker">{e(r["system"])}</span><strong>{e(r["figure"])}</strong><small>{e(r["scope"])}</small></li>' for r in hero['results'])
    return f'<figure class="diagram results" aria-labelledby="results-title"><div class="diagram-top"><span class="mono" id="results-title">Measured results, with their scope</span><span class="mono">{len(hero["results"])} systems</span></div><ol class="results-list">{items}</ol><figcaption class="diagram-caption">{e(hero["results_caption"])}</figcaption></figure>'


def gateway_visual():
    steps = [
        ('01', 'Rate limiter', 'Per-API-key token bucket → 429'),
        ('02', 'Admission control', 'In-flight ceiling, never queues → 503'),
        ('03', 'Validate + deadline', 'One end-to-end budget per request'),
        ('04', 'Weighted / canary router', 'Pool split, then replica (smooth WRR), filtered by health and breaker state'),
        ('05', 'Upstream call', 'Buffered, or SSE opened headers-first; bytes relayed unmodified'),
    ]
    rows = ''.join(f'<li><span class="gw-n">{n}</span><div><strong>{e(t)}</strong><small>{e(d)}</small></div></li>' for n, t, d in steps)
    return f'''<div class="gateway-visual" aria-label="MaaS Gateway request path as built: client, rate limiter, admission control, validate and deadline, weighted or canary router, upstream call, two vLLM processes on one NVIDIA L4."><div class="gw-title"><span class="mono">Request path · as built</span><span class="mono">1 gateway · 2 vLLM · 1 GPU</span></div><p class="gw-client mono">Client · OpenAI-compatible SDK or curl</p><ol class="gw-steps">{rows}</ol><div class="gw-upstream"><span>vLLM process A · vLLM process B</span><span class="mono">1 × NVIDIA L4 · 23 GB</span></div><p class="gw-state" aria-label="Control state consulted by the request path"><span>Health probes</span><span>Circuit breaker</span><span>Retry budget</span><span>Scheduler credit</span></p><p class="gw-foot">E3 · ONE ENGINE KILLED MID-TRAFFIC<br>Breaker excluded it in ≈2 s; health probe agreed at ≈10 s. p95 345 → 709 ms: the measured cost of masking a failure.</p></div>'''


def actions(project, href, label='View case study', aria=None):
    links = ''.join(external(x['url'], x['label'], 'text-link external') for x in (project['links'] if project else []))
    aria_attr = f' aria-label="{e(aria)}"' if aria else ''
    return f'<div class="actions"><a class="text-link" href="{href}"{aria_attr}>{e(label)} <span aria-hidden="true">↗</span></a>{links}</div>'


def heading(number, label, title, description=""):
    intro = f'<p class="section-intro">{e(description)}</p>' if description else ''
    return f'<div class="section-heading"><p class="section-label"><span class="index">{number}</span>{label}</p><div><h2>{title}</h2>{intro}</div></div>'


def featured(p):
    chips = ''.join(f'<li>{e(x)}</li>' for x in p['chips'])
    return f'''<article class="work-featured"><div><p class="project-kicker">{e(p['category'])}</p><h3 class="project-name"><a href="/work/{p['slug']}/">{e(p['name'])}</a></h3><p class="project-subtitle">{e(p['subtitle'])}</p><p class="project-description">{e(p['summary'])}</p><p class="project-description">{e(p['proof'])}</p><ul class="evidence-list">{chips}</ul>{actions(p, f"/work/{p['slug']}/", aria=f"View {p['name']} case study")}<p class="status"><span class="dot"></span>{e(p['status'])}</p></div>{gateway_visual()}</article>'''


def row(index, card):
    p = PROJECTS.get(card.get('project'))
    name = card.get('name') or p['name']
    href = card.get('href') or f'/work/{p["slug"]}/'
    subtitle = card.get('subtitle') or p['subtitle']
    status = card.get('status') or p['status']
    summary = card.get('summary') or p['summary']
    proof = card.get('proof') or p['proof']
    label = card.get('link_label', 'View case study')
    aria = f'{label}: {name}'
    return f'''<article class="work-row"><span class="index">{index:02d}</span><div><p class="project-kicker">{e(card['kicker'])}</p><h3 class="project-name"><a href="{href}">{e(name)}</a></h3><p class="project-subtitle">{e(subtitle)}</p><p class="status">{e(status)}</p></div><div class="work-summary"><p class="project-description">{e(summary)}</p><p class="project-description">{e(proof)}</p>{actions(p, href, label, aria)}</div></article>'''


def experience():
    out = ''
    for x in DATA['experience']:
        bullets = ''.join(f'<li>{e(b)}</li>' for b in x['bullets'])
        out += f'<div class="experience-row"><p class="experience-date">{e(x["dates"])}</p><div><div class="experience-title"><h3>{e(x["organization"])}</h3><span>{e(x["role"])}</span></div><ul class="experience-bullets">{bullets}</ul></div></div>'
    return out


def research():
    papers = ''.join(f'<article class="paper"><div>{external(x["url"], x["title"], "paper-title")}<p class="paper-meta">{e(x["meta"])}</p></div><span class="paper-arrow" aria-hidden="true">↗</span></article>' for x in DATA['research'])
    proto = DATA['prototype']
    p = PROJECTS[proto['project']]
    prototype = f'''<article class="prototype"><p class="project-kicker">{e(proto['label'])}</p><h3><a href="/work/{p['slug']}/">{e(p['name'])}</a></h3><p>{e(proto['summary'])}</p><p class="status"><span class="dot"></span>{e(proto['status'])}</p>{actions(p, f"/work/{p['slug']}/", aria=f"View {p['name']} case study")}</article>'''
    return f'<div class="research-list">{papers}{prototype}</div>'


def about():
    a = DATA['about']
    copy = ''.join(f'<p>{e(x)}</p>' for x in a['paragraphs'])
    education = ''.join(f'<p><strong>{e(x["school"])}</strong>{e(x["degree"])}<br>{e(x["detail"])}</p>' for x in a['education'])
    skills = ''.join(f'<div class="skill-line"><dt>{e(x["label"])}</dt><dd>{e(x["items"])}</dd></div>' for x in a['skills'])
    return f'<div class="about-grid"><div class="about-copy">{copy}<div class="education">{education}</div></div><dl class="skills">{skills}</dl></div>'


def home():
    hero = DATA['hero']
    rows = ''.join(row(i, card) for i, card in enumerate(DATA['home_cards'], 2))
    body = f'''<main id="main" class="wrap"><section class="hero" aria-labelledby="hero-title"><div class="hero-topline"><p class="eyebrow"><span class="dot"></span>{e(hero['eyebrow'])}</p><p class="hero-availability">Available full-time · {DATA['availability']}</p></div><div class="hero-grid"><div><h1 id="hero-title">Haiyue Zhang<br><span class="alias">You can call me Heady.</span></h1><p class="role">{e(DATA['role'])}</p><p class="hero-lead">{e(DATA['description'])}</p><p class="hero-support">{e(hero['support'])}</p><div class="actions"><a class="button" href="#work">Explore work <span aria-hidden="true">↓</span></a>{external(DATA['github'], 'GitHub', 'text-link external')}<a class="text-link" href="#contact">Contact <span aria-hidden="true">↗</span></a></div></div>{results()}</div><div class="hero-bottom"><span>{e(hero['now'])}</span><span class="mono">Los Angeles, CA</span></div></section>
<section class="section" id="work">{heading('01', 'Selected work', 'Built across the serving stack.', 'From an LLM inference gateway and a production AI backend to GPU training workflows and CUDA kernels.')}{featured(DATA['projects'][0])}{rows}</section>
<section class="section" id="experience">{heading('02', 'Experience', 'From the lab to the customer.')}{experience()}</section>
<section class="section" id="research">{heading('03', 'Research', 'Make the work inspectable.', 'Public research on agent security, auditability, and execution governance, plus one research prototype.')}{research()}</section>
<section class="section" id="about">{heading('04', 'About', 'An engineer who follows the evidence.')}{about()}</section>
<section class="contact" id="contact"><div><p class="eyebrow">05 / Get in touch</p><h2>Building serving or ML infrastructure?<br>Let's make it concrete.</h2><p>Los Angeles, CA · Available full-time {DATA['availability']}</p></div><div class="contact-details"><a class="contact-email" href="mailto:{DATA['email']}">{DATA['email']}</a><div class="contact-links">{external(DATA['github'], 'GitHub')}{external(DATA['linkedin'], 'LinkedIn')}</div></div></section></main>'''
    return shell(f'Haiyue (Heady) Zhang — {DATA["role"]}', DATA['description'] + ' USC M.S. ECE, available May 2027.', '/', body)


def case(project):
    toc = ''.join(f'<a href="#{x["id"]}">{e(x["title"])}</a>' for x in project['sections'])
    sections = ''.join(f'<section class="case-section" id="{x["id"]}"><h2>{e(x["title"])}</h2>{x["html"]}</section>' for x in project['sections'])
    links = ''.join(external(x['url'], x['label'], 'text-link external') for x in project['links'])
    body = f'''<main id="main" class="wrap"><article><header class="case-hero"><a class="breadcrumb" href="/#work"><span aria-hidden="true">←</span> Selected work</a><p class="project-kicker">{e(project['category'])}</p><h1>{e(project['name'])}</h1><p class="case-deck">{e(project['deck'])}</p><dl class="case-metadata"><div><dt>Role</dt><dd>{e(project['ownership'])}</dd></div><div><dt>Period</dt><dd>{e(project['period'])}</dd></div></dl><p class="mono case-stack">{e(project['stack'])}</p><div class="case-status">{e(project['status_detail'])}</div>{f'<div class="actions">{links}</div>' if links else ''}</header><div class="case-layout"><nav class="case-nav" aria-label="In this case study"><p class="mono">In this case study</p>{toc}</nav><div class="case-body">{sections}<div class="case-end"><a class="text-link" href="/#work"><span aria-hidden="true">←</span> All selected work</a>{links}</div></div></div></article></main>'''
    return shell(project['name'] + ' — Heady Zhang', project['deck'], '/work/' + project['slug'] + '/', body, 'article')


def build():
    (ROOT / 'index.html').write_text(home())
    projects = DATA['projects']
    for project in projects:
        directory = ROOT / 'work' / project['slug']
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'index.html').write_text(case(project))
    (ROOT / '404.html').write_text(shell('Page not found — Heady Zhang', 'Return to Heady Zhang’s selected engineering work.', '/404.html', '<main id="main" class="wrap"><div class="error-page"><p class="eyebrow">404 / Route not found</p><h1>A different path.</h1><p>This page is not here. You can find the current projects in selected work.</p><a class="button" href="/#work">Back to selected work <span aria-hidden="true">→</span></a></div></main>'))
    routes = ['/'] + ['/work/' + p['slug'] + '/' for p in projects]
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}{r}</loc></url>\n' for r in routes) + '</urlset>\n')
    (ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: ' + BASE + '/sitemap.xml\n')
    print(f'Built {len(projects) + 2} HTML pages, sitemap.xml, and robots.txt.')


if __name__ == '__main__':
    build()
