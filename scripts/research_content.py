"""Build research content and shared navigation without changing existing page bodies."""
from datetime import date
from html import escape
import json
from pathlib import Path
import re

BASE = 'https://muhammadumaramin.github.io/portfolio/'
NAV = [('index.html', 'Home'), ('experience.html', 'Experience'),
       ('projects.html', 'Projects'), ('about.html', 'About'),
       ('research.html', 'Research'), ('blog.html', 'Blog'), ('contact.html', 'Contact')]
STYLE = '<link rel="stylesheet" href="assets/research.css?v=research-1">'
LATEST_SCRIPT = '<script src="assets/latest-articles.js?v=2" defer></script>'
JOURNAL = re.compile(r'<section\b[^>]*\bid="latest-articles"[^>]*>.*?</section>', re.S)
HIGHLIGHT = re.compile(r'<section\b[^>]*\bid="research-highlights"[^>]*>.*?</section>', re.S)


def capture_home_journal(root):
    path = root / 'index.html'
    if not path.exists():
        return ''
    match = JOURNAL.search(path.read_text())
    return match.group() if match else ''


def external(url, label, cls='text-link'):
    return f'<a class="{cls}" href="{escape(url, quote=True)}" target="_blank" rel="noopener">{escape(label)} <span aria-hidden="true">↗</span></a>'


def paper_content(p):
    published = date.fromisoformat(p['date'])
    display_date = f'{published:%B} {published.day}, {published.year}'
    authors = ', '.join(f'<strong>{escape(a)}</strong>' if a == 'Muhammad Umar Amin' else escape(a) for a in p['authors'])
    doi = external('https://doi.org/' + p['doi'], 'DOI') if p.get('doi') else ''
    return f'''<p class="eyebrow">{published.year} · Published · Coauthor</p>
<h3>{escape(p['headline'])}</h3><p class="research-paper-summary">{escape(p['summary'])}</p>
<p class="research-meta">{escape(p['journal'])}<br>{p['volume']}({p['issue']}), {escape(p['pages'])} · <time datetime="{p['date']}">{display_date}</time></p>
<div class="actions">{external(p['url'], 'Read the paper', 'button' if p.get('featured') else 'text-link')}{doi}</div>
<details class="research-details"><summary>Research approach &amp; citation</summary><p>{escape(p['approach'])}</p>
<p class="research-authors">{authors}.</p><p class="research-citation"><cite>{escape(p['title'])}</cite></p></details>'''


def render_body(data):
    featured, *others = data['publications']
    papers = ''.join(f'<article class="research-paper" id="{p["id"]}">{paper_content(p)}</article>' for p in others)
    honors = ''.join(f'<article class="research-honor"><p class="eyebrow">{escape(h["year"])} · {escape(h["category"])}</p><h3>{escape(h["title"])}</h3><p>{escape(h["description"])}</p></article>' for h in data['honors'])
    earlier = ''.join(f'<p><strong>{escape(h["title"])} · {h["year"]}</strong><br>{escape(h["organization"])}</p>' for h in data['earlier_honors'])
    conference = data['conference']
    return f'''<section class="research-hero" aria-labelledby="research-heading"><div><p class="eyebrow">Commerce · Analytics · Applied research</p><h1 id="research-heading">Research &amp;<br>recognition.</h1><p class="lead">I bring a quantitative perspective to business problems. My coauthored research explores smarter logistics, adaptive supply chains, and safer digital transactions.</p></div><aside class="research-perspective"><p class="eyebrow">The thread connecting my work</p><p class="research-motto">Better questions.<br>Stronger evidence.<br>More useful decisions.</p>{external(data['scholar_url'], 'Google Scholar')}</aside></section>
<nav class="research-jumps" aria-label="Research page sections"><a href="#publications"><span>01</span> Publications</a><a href="#conferences"><span>02</span> Conferences</a><a href="#recognition"><span>03</span> Recognition</a></nav>
<section class="research-section" id="publications" aria-labelledby="publications-heading"><div class="section-heading"><div><p class="eyebrow">Selected publications</p><h2 id="publications-heading">From inquiry to application.</h2></div><p class="research-section-note">Collaborative research connecting analytical methods with operational questions.</p></div>
<article class="research-feature" id="{featured['id']}"><div class="research-cover"><p class="eyebrow">Featured research · Supply chains</p><p class="research-question">How can a supply chain adapt before disruption becomes delay?</p><div class="research-cover-topics"><span>Digital twins</span><span>Reinforcement learning</span></div></div><div class="research-paper-body">{paper_content(featured)}</div></article><div class="research-paper-grid">{papers}</div>
<div class="research-project-link"><p>Explore the code, dashboards, and academic studies behind my analytical work.</p><a class="text-link" href="projects.html">View project portfolio →</a></div></section>
<section class="research-section" id="conferences" aria-labelledby="conferences-heading"><div class="section-heading"><div><p class="eyebrow">Conferences &amp; academic community</p><h2 id="conferences-heading">Ideas grow through conversation.</h2></div></div><article class="research-conference"><div class="research-date">October<span>2025 · San Antonio</span></div><div><span class="research-role">{escape(conference['role'])}</span><h3>{escape(conference['name'])}</h3><p class="research-paper-summary">{escape(conference['summary'])}</p>{external(conference['url'], 'About the event')}</div></article></section>
<section class="research-section" id="recognition" aria-labelledby="recognition-heading"><div class="section-heading"><div><p class="eyebrow">Honors &amp; scholarships</p><h2 id="recognition-heading">Milestones along the way.</h2></div></div><div class="research-honors">{honors}</div><details class="research-details research-earlier"><summary>Earlier academic recognition</summary><div class="research-earlier-grid">{earlier}</div></details></section>
<section class="research-closing" aria-labelledby="research-contact-heading"><div><h2 id="research-contact-heading">A shared question is a good start.</h2><p>For conversations about analytics, commerce, or applied research, get in touch.</p></div><a class="text-link" href="contact.html">Start a conversation →</a></section>'''


def render_highlight():
    return '''<section class="section" id="research-highlights" aria-labelledby="research-highlights-heading"><div class="section-heading"><div><p class="eyebrow">Beyond the day-to-day</p><h2 id="research-highlights-heading">The research behind my perspective.</h2></div></div><div class="home-research-grid"><article class="home-research-item"><p class="eyebrow">Selected publication</p><h3><a href="research.html#digital-twins">Adaptive supply chains</a></h3><p>Coauthored research exploring digital twins and learning-based operational decisions.</p></article><article class="home-research-item"><p class="eyebrow">Academic community</p><h3><a href="research.html#conferences">TUMC 2025</a></h3><p>Graduate panelist representing Lamar University at St. Mary’s University.</p></article><article class="home-research-item"><p class="eyebrow">Recognition</p><h3><a href="research.html#recognition">Phi Kappa Phi</a></h3><p>Honor society induction, December 2025.</p></article></div><div class="actions"><a class="button" href="research.html">Explore research &amp; recognition <span aria-hidden="true">→</span></a></div></section>'''


def research_page(root, data):
    template = (root / 'index.html').read_text()
    title = 'Research & Recognition | Muhammad Umar Amin'
    description = 'Explore Muhammad Umar Amin’s coauthored research in supply chains, geospatial logistics, and fraud detection, plus conferences and academic recognition.'
    url = BASE + 'research.html'
    template = re.sub(r'<title>.*?</title>', '<title>' + escape(title) + '</title>', template, count=1)
    for attr, key, value in [('name', 'description', description), ('property', 'og:title', title),
                             ('property', 'og:description', description), ('property', 'og:url', url),
                             ('name', 'twitter:title', title), ('name', 'twitter:description', description)]:
        template = re.sub(rf'<meta {attr}="{key}" content="[^"]*">', f'<meta {attr}="{key}" content="{escape(value, quote=True)}">', template, count=1)
    template = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', template, count=1)
    graph_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', template, re.S)
    graph = json.loads(graph_match.group(1))
    nodes = graph['@graph']
    person = next(n for n in nodes if n['@type'] == 'Person')
    person['sameAs'] = list(dict.fromkeys(person['sameAs'] + [data['scholar_url']]))
    webpage = next(n for n in nodes if n['@type'] == 'WebPage')
    webpage.update({'@id': url + '#webpage', 'url': url, 'name': title, 'description': description,
                    'mainEntity': {'@id': url + '#publication-list'}})
    articles = []
    for p in data['publications']:
        article = {'@type': 'ScholarlyArticle', '@id': url + '#' + p['id'], 'name': p['title'],
                   'headline': p['headline'], 'url': p['url'], 'datePublished': p['date'],
                   'description': p['summary'], 'pagination': p['pages'],
                   'author': [{'@id': BASE + '#person'} if a == 'Muhammad Umar Amin' else {'@type': 'Person', 'name': a} for a in p['authors']],
                   'isPartOf': {'@type': 'PublicationIssue', 'issueNumber': p['issue'], 'isPartOf': {
                       '@type': 'PublicationVolume', 'volumeNumber': p['volume'], 'isPartOf': {
                           '@type': 'Periodical', 'name': p['journal']}}}}
        if p.get('doi'):
            article['identifier'] = {'@type': 'PropertyValue', 'propertyID': 'DOI', 'value': p['doi']}
            article['sameAs'] = 'https://doi.org/' + p['doi']
        articles.append(article)
    nodes.extend(articles)
    nodes.append({'@type': 'ItemList', '@id': url + '#publication-list', 'name': 'Selected publications',
                  'numberOfItems': len(articles), 'itemListElement': [
                      {'@type': 'ListItem', 'position': i, 'item': {'@id': a['@id']}} for i, a in enumerate(articles, 1)]})
    encoded = json.dumps(graph, ensure_ascii=False).replace('<', '\\u003c')
    template = template[:graph_match.start(1)] + encoded + template[graph_match.end(1):]
    template = re.sub(r'<script\b[^>]*src="assets/latest-articles\.js[^"]*"[^>]*></script>', '', template)
    template = re.sub(r'(<main\b[^>]*>).*?(</main>)', lambda m: m[1] + render_body(data) + m[2], template, count=1, flags=re.S)
    return template


def update_research(root, home_journal=''):
    root = Path(root)
    data = json.loads((root / 'content/research.json').read_text())
    (root / 'research.html').write_text(research_page(root, data))
    nav_files = {file for file, _ in NAV}
    for path in sorted(root.glob('*.html')):
        html = path.read_text()
        current = path.name if path.name in nav_files else ('blog.html' if 'class="active" href="blog.html"' in html else '')
        nav = ''.join(f'<a href="{"./" if filename == "index.html" else filename}"' + (' class="active" aria-current="page"' if filename == current else '') + f'>{label}</a>' for filename, label in NAV)
        html, count = re.subn(r'(<nav\b[^>]*aria-label="Main navigation"[^>]*>).*?(</nav>)', lambda m: m[1] + nav + m[2], html, count=1, flags=re.S)
        if count != 1:
            raise ValueError(f'Missing main navigation: {path.name}')
        html = re.sub(r'<link rel="stylesheet" href="assets/research\.css[^"]*">', '', html)
        html = html.replace('</head>', STYLE + '</head>', 1)
        if path.name == 'index.html':
            html = HIGHLIGHT.sub('', html)
            if not JOURNAL.search(html) and home_journal:
                html = html.replace('</main>', home_journal + '</main>', 1)
            journal = JOURNAL.search(html)
            if journal:
                html = html[:journal.start()] + render_highlight() + html[journal.start():]
                if 'src="assets/latest-articles.js' not in html:
                    html = html.replace('</head>', LATEST_SCRIPT + '</head>', 1)
            else:
                html = html.replace('</main>', render_highlight() + '</main>', 1)
        path.write_text(html)
    # Include existing articles even when the core builder regenerated its smaller sitemap.
    sitemap = root / 'sitemap.xml'
    original = sitemap.read_text() if sitemap.exists() else ''
    previous = {re.search(r'<loc>(.*?)</loc>', item).group(1): item for item in re.findall(r'<url>.*?</url>', original, re.S)}
    entries = []
    for path in sorted(root.glob('*.html')):
        url = BASE if path.name == 'index.html' else BASE + path.name
        entries.append(previous.get(url, f'<url><loc>{url}</loc></url>'))
    sitemap.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(entries) + '\n</urlset>\n')


if __name__ == '__main__':
    update_research(Path(__file__).resolve().parents[1])
    print('Updated research page, homepage highlights, navigation, and sitemap.')
