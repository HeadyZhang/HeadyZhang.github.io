"""Render a dependency-free static portfolio from one shared content source."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "scripts/content.json").read_text())
BASE = "https://headyzhang.github.io"
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
    person = {"@context": "https://schema.org", "@type": "Person", "name": "Haiyue Zhang", "alternateName": "Heady Zhang", "url": BASE + "/", "jobTitle": DATA['role'], "email": "mailto:" + DATA['email'], "sameAs": [DATA['github'], DATA['linkedin']], "alumniOf": {"@type": "CollegeOrUniversity", "name": "Shanghai Jiao Tong University"}, "homeLocation": {"@type": "Place", "name": "Los Angeles, CA"}}
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#f7f7f2">
<link rel="canonical" href="{BASE}{route}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="{kind}"><meta property="og:url" content="{BASE}{route}"><meta property="og:site_name" content="Heady Zhang"><meta property="og:locale" content="en_US"><meta name="twitter:card" content="summary">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"><link rel="stylesheet" href="/assets/style.css"><script src="/assets/site.js" defer></script>
<script type="application/ld+json">{json.dumps(person, ensure_ascii=False)}</script></head><body>{nav()}{body}{footer()}</body></html>'''


def pipeline():
    return '''<figure class="diagram"><div class="diagram-top"><span class="mono">A system, from intent to action</span><span class="mono">01 → 04</span></div>
<svg viewBox="0 0 440 350" role="img" aria-labelledby="pipeline-title pipeline-description">
<title id="pipeline-title">From ambiguous input to verified execution</title><desc id="pipeline-description">An operating question becomes a model proposal. Deterministic evidence and dependency checks lead to human review and a signed execution gate. Unresolved evidence returns to review.</desc>
<defs><pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".65" fill="#c8d0bf"/></pattern><marker id="arrow" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M1 1L6 4L1 7" fill="none" stroke="#77846d" stroke-width="1.2"/></marker></defs>
<rect width="440" height="350" fill="url(#dots)"/>
<g fill="none" stroke="#88957c" stroke-width="1.2" marker-end="url(#arrow)"><path d="M128 78H184"/><path d="M306 113V158"/><path d="M306 233V277H250"/><path d="M148 277H84V174H201" stroke-dasharray="3 5"/></g>
<g font-family="ui-monospace, monospace" font-size="10" fill="#56624d"><text x="13" y="31">01 / AMBIGUITY</text><text x="190" y="31">02 / MODEL PROPOSAL</text><text x="201" y="149">03 / EVIDENCE CHECK</text></g>
<rect x="12" y="45" width="116" height="67" rx="2" fill="#f7f7f2" stroke="#bec8b3"/><g font-family="-apple-system, sans-serif" font-size="13" fill="#3f4b38"><text x="26" y="73">Should we</text><text x="26" y="92">take this action?</text></g>
<rect x="184" y="45" width="243" height="68" rx="2" fill="#f7f7f2" stroke="#bec8b3"/><text x="200" y="73" font-family="-apple-system, sans-serif" font-size="14" fill="#303a2b">A proposal, with assumptions</text><text x="200" y="95" font-family="ui-monospace, monospace" font-size="10" fill="#65715d">Claims · candidates · context</text>
<rect x="201" y="158" width="226" height="74" rx="2" fill="#e1e8fc" stroke="#8ea4e6"/><text x="217" y="186" font-family="-apple-system, sans-serif" font-size="14" fill="#214cdb">What does the evidence allow?</text><text x="217" y="210" font-family="ui-monospace, monospace" font-size="10" fill="#405581">Typed contracts + dependencies</text>
<text x="11" y="213" font-family="ui-monospace, monospace" font-size="9" fill="#64705b">UNRESOLVED?</text><text x="11" y="229" font-family="ui-monospace, monospace" font-size="9" fill="#64705b">RETURN TO REVIEW</text>
<rect x="148" y="252" width="279" height="70" rx="2" fill="#253428"/><circle cx="168" cy="274" r="3" fill="#b6d69d"/><text x="180" y="278" font-family="ui-monospace, monospace" font-size="9" fill="#c9dbbd">04 / HUMAN APPROVAL + SIGNED GATE</text><text x="165" y="305" font-family="-apple-system, sans-serif" font-size="17" fill="#f1f5ec">Verified execution</text>
<g fill="#214cdb"><circle class="pipeline-signal" cx="157" cy="78" r="3"/><circle class="pipeline-signal signal-two" cx="306" cy="133" r="3"/><circle class="pipeline-signal signal-three" cx="306" cy="243" r="3"/></g></svg>
<ol class="mobile-pipeline"><li><span>01 / INPUT</span><strong>Should we take this action?</strong><small>Operating context and constraints</small></li><li><span>02 / MODEL PROPOSAL</span><strong>A proposal, with assumptions</strong><small>Claims, candidates, and context</small></li><li><span>03 / EVIDENCE CHECK</span><strong>What does the evidence allow?</strong><small>Typed contracts and dependencies</small></li><li><span>04 / HUMAN APPROVAL + SIGNED GATE</span><strong>Verified execution</strong><small>Unresolved evidence returns to review.</small></li></ol><figcaption class="diagram-caption">Models propose. Evidence constrains. People authorize.</figcaption></figure>'''


def actions(project):
    slug = project['slug']
    links = ''.join(external(x['url'], x['label'], 'text-link external') for x in project['links'])
    return f'<div class="actions"><a class="text-link" href="/work/{slug}/" aria-label="View {e(project["name"])} case study">View case study <span aria-hidden="true">↗</span></a>{links}</div>'


def heading(number, label, title, description=""):
    intro = f'<p class="section-intro">{e(description)}</p>' if description else ''
    return f'<div class="section-heading"><p class="section-label"><span class="index">{number}</span>{label}</p><div><h2>{title}</h2>{intro}</div></div>'


def home():
    p = DATA['projects'][0]
    chips = ''.join(f'<li>{e(x)}</li>' for x in p['chips'])
    featured = f'''<article class="work-featured"><div><p class="project-kicker">{p['category']}</p><h3 class="project-name"><a href="/work/causalops/">CausalOps</a></h3><p class="project-subtitle">{e(p['subtitle'])}</p><p class="project-description">{e(p['summary'])}</p><p class="project-description">{e(p['proof'])}</p><ul class="evidence-list">{chips}</ul>{actions(p)}<p class="status"><span class="dot"></span>Research prototype · Product value unvalidated</p></div>
<div class="contract-visual" role="img" aria-label="Illustrative review contract: evidence has sources, dependencies are checked, and execution requires signed human approval. This illustration is not a live system status."><div class="contract-title"><span class="mono">A reviewable contract</span><span class="mono">Illustration</span></div><div class="contract-row"><span class="contract-number">01</span><div><strong>Trace the claim</strong><small>Every judgment has an evidence boundary.</small></div><span class="check">↳</span></div><div class="contract-row"><span class="contract-number">02</span><div><strong>Check the dependencies</strong><small>Unsupported inputs cannot grant authority.</small></div><span class="check">↳</span></div><div class="contract-row"><span class="contract-number">03</span><div><strong>Require an explicit approval</strong><small>Bind the signature to the intended execution.</small></div><span class="check">↳</span></div><p class="contract-foot">PROPOSAL ≠ PERMISSION<br>13 targeted gate mutations detected in a frozen milestone.</p></div></article>'''
    rows = ''
    for i, p in enumerate(DATA['projects'][1:], 2):
        rows += f'''<article class="work-row"><span class="index">0{i}</span><div><p class="project-kicker">{e(p['category'].split(' / ')[1])}</p><h3 class="project-name"><a href="/work/{p['slug']}/">{e(p['name'])}</a></h3><p class="project-subtitle">{e(p['subtitle'])}</p><p class="status">{e(p['status'])}</p></div><div class="work-summary"><p class="project-description">{e(p['summary'])}</p><p class="project-description">{e(p['proof'])}</p>{actions(p)}</div></article>'''
    experience = ''.join(f'<div class="experience-row"><p class="experience-date">{e(x["dates"])}</p><div><div class="experience-title"><h3>{e(x["organization"])}</h3><span>{e(x["role"])}</span></div><p>{e(x["detail"])}</p></div></div>' for x in DATA['experience'])
    research = ''.join(f'<article class="paper"><div>{external(x["url"], x["title"], "paper-title")}<p class="paper-meta">{e(x["meta"])}</p></div><span class="paper-arrow" aria-hidden="true">↗</span></article>' for x in DATA['research'])
    body = f'''<main id="main" class="wrap"><section class="hero" aria-labelledby="hero-title"><div class="hero-topline"><p class="eyebrow"><span class="dot"></span>Systems thinking. End-to-end delivery.</p><p class="hero-availability">Available full-time · {DATA['availability']}</p></div><div class="hero-grid"><div><h1 id="hero-title">Haiyue Zhang<br><span class="alias">You can call me Heady.</span></h1><p class="role">{e(DATA['role'])}</p><p class="hero-lead">{e(DATA['description'])}</p><p class="hero-support">From customer-facing product delivery to auditable AI workflows and GPU training, inference, and evaluation tooling.</p><div class="actions"><a class="button" href="#work">Explore selected work <span aria-hidden="true">↓</span></a><a class="text-link" href="#contact">Contact <span aria-hidden="true">↗</span></a></div></div>{pipeline()}</div><div class="hero-bottom"><span>USC M.S. ECE · Machine Learning &amp; Data Science · Graduating {DATA['availability']}</span><span class="mono">Los Angeles, CA</span></div></section>
<section class="section" id="work">{heading('01', 'Selected work', 'Built across the full system.', 'Four bodies of work, from customer workflows to the controls and compute beneath them.')}{featured}{rows}</section>
<section class="capabilities" aria-label="Capabilities and proof"><div class="capability"><p class="mono">01 / Understand & deliver</p><h3>Customer → Product</h3><p>Requirements discovery, workflow design, deployment.</p><a href="/work/topify/">Customer workflows → Railway deployment ↗</a></div><div class="capability"><p class="mono">02 / Constrain & authorize</p><h3>Model → Authority</h3><p>Typed contracts, deterministic gates, auditability.</p><a href="/work/causalops/">Model proposals → signed execution gates ↗</a></div><div class="capability"><p class="mono">03 / Run & investigate</p><h3>GPU → Evidence</h3><p>Training, inference, evaluation, root-cause debugging.</p><a href="/work/gpu-systems/">ToolRL reproduction → evaluation bug fix ↗</a></div></section>
<section class="section" id="experience">{heading('02','Experience','From the lab to the customer.')}{experience}</section>
<section class="section" id="research">{heading('03','Selected research','Make the work inspectable.', 'A small selection of public research on agent security, auditability, and execution governance.')}<div class="research-list">{research}</div></section>
<section class="section" id="about">{heading('04','About','An engineer who follows the evidence.')}<div class="about-grid"><div class="about-copy"><p>I like problems that begin as an unclear requirement and become a system someone can inspect, use, and improve.</p><p>My work spans B2B product delivery, AI-agent security, and research infrastructure. Across those settings, I care about clear acceptance criteria, the behavior of the running system, and the limits of what its results prove.</p><div class="education"><p><strong>University of Southern California</strong>M.S. ECE · Machine Learning &amp; Data Science<br>Expected {DATA['availability']}</p><p><strong>Shanghai Jiao Tong University</strong>B.S. Electrical and Computer Engineering</p></div></div><dl class="skills"><div class="skill-line"><dt>Languages</dt><dd>Python, C/C++, SQL, JavaScript</dd></div><div class="skill-line"><dt>ML systems</dt><dd>PyTorch, DeepSpeed, veRL, vLLM<br><small>vLLM: research rollout inference</small></dd></div><div class="skill-line"><dt>Engineering</dt><dd>Linux, Docker, FastAPI, Railway, Git, CI/CD, property-based testing, mutation testing</dd></div></dl></div></section>
<section class="contact" id="contact"><div><p class="eyebrow">05 / Get in touch</p><h2>Have a hard systems problem?<br>Let's make it concrete.</h2><p>Los Angeles, CA · Available full-time {DATA['availability']}</p></div><div class="contact-details"><a class="contact-email" href="mailto:{DATA['email']}">{DATA['email']}</a><div class="contact-links">{external(DATA['github'],'GitHub')}{external(DATA['linkedin'],'LinkedIn')}</div></div></section></main>'''
    return shell('Haiyue (Heady) Zhang — AI Systems & Infrastructure Engineer', DATA['description'] + ' USC M.S. ECE, graduating May 2027.', '/', body)


def case(project, following):
    toc = ''.join(f'<a href="#{x["id"]}">{e(x["title"])}</a>' for x in project['sections'])
    sections = ''.join(f'<section class="case-section" id="{x["id"]}"><h2>{e(x["title"])}</h2>{x["html"]}</section>' for x in project['sections'])
    links = ''.join(external(x['url'], x['label'], 'text-link external') for x in project['links'])
    body = f'''<main id="main" class="wrap"><article><header class="case-hero"><a class="breadcrumb" href="/#work"><span aria-hidden="true">←</span> Selected work</a><p class="project-kicker">{e(project['category'])}</p><h1>{e(project['name'])}</h1><p class="case-deck">{e(project['deck'])}</p><dl class="case-metadata"><div><dt>Role</dt><dd>{e(project['ownership'])}</dd></div><div><dt>Period</dt><dd>{e(project['period'])}</dd></div></dl><p class="mono" style="margin-top:20px;font-size:.62rem;color:var(--muted)">{e(project['stack'])}</p><div class="case-status">{e(project['status_detail'])}</div>{f'<div class="actions">{links}</div>' if links else ''}</header><div class="case-layout"><nav class="case-nav" aria-label="In this case study"><p class="mono">In this case study</p>{toc}</nav><div class="case-body">{sections}<div class="next-case"><div><p>Next case study</p><a href="/work/{following['slug']}/">{e(following['name'])} <span aria-hidden="true">↗</span></a></div><a class="text-link" href="/#work">All selected work</a></div></div></div></article></main>'''
    return shell(project['name'] + ' — Heady Zhang', project['deck'], '/work/' + project['slug'] + '/', body, 'article')


def build():
    (ROOT / 'index.html').write_text(home())
    projects = DATA['projects']
    for i, project in enumerate(projects):
        directory = ROOT / 'work' / project['slug']
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'index.html').write_text(case(project, projects[(i + 1) % len(projects)]))
    (ROOT / '404.html').write_text(shell('Page not found — Heady Zhang', 'Return to Heady Zhang’s selected engineering work.', '/404.html', '<main id="main" class="wrap"><div class="error-page"><p class="eyebrow">404 / Route not found</p><h1>A different path.</h1><p>This page is not here. You can find the current projects in selected work.</p><a class="button" href="/#work">Back to selected work <span aria-hidden="true">→</span></a></div></main>'))
    routes = ['/'] + ['/work/' + p['slug'] + '/' for p in projects]
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}{r}</loc></url>\n' for r in routes) + '</urlset>\n')
    (ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: ' + BASE + '/sitemap.xml\n')
    print(f'Built {len(projects) + 2} HTML pages, sitemap.xml, and robots.txt.')


if __name__ == '__main__':
    build()
