"""Add source-backed project previews to the existing portfolio markup."""
from html import escape
import json
import re


def add_project_visuals(markup, root):
    manifest = json.loads((root / 'images/projects/sources.json').read_text())
    records = {item['project_number']: item for item in manifest['visuals']}

    def enhance(match):
        article = match.group(0)
        number = int(re.search(r'<div class="project-number">(\d+)</div>', article).group(1))
        if number not in records or 'class="project-media"' in article:
            return article
        record = records[number]
        field = lambda key: escape(str(record[key]), quote=True)
        source_label = 'Watch walkthrough' if record['extraction'].startswith('Video frame') else 'View source'
        figure = f'''<figure class="project-media">
<a class="project-media-link" href="{field('full')}" target="_blank" rel="noopener" aria-label="View full-size visual: {field('alt')} (opens in a new tab)">
<span class="project-media-label">{field('kind')}</span>
<span class="project-media-frame"><img src="{field('preview')}" width="{field('width')}" height="{field('height')}" alt="{field('alt')}" loading="lazy" decoding="async"></span>
<span class="project-media-open">View full image <span aria-hidden="true">↗</span></span>
</a>
<figcaption>{field('caption')} <a href="{field('source_url')}">{source_label} <span aria-hidden="true">↗</span></a></figcaption>
</figure>'''
        question = re.search(r'<p class="question">.*?</p>', article, flags=re.S)
        if not question or not article.endswith('</div></article>'):
            raise ValueError(f'Unexpected project markup for project {number}')
        before = article[:question.end()]
        body = article[question.end():-len('</div></article>')]
        return before + '\n<div class="project-details"><div class="project-copy">' + body + '</div>\n' + figure + '</div></div></article>'

    return re.sub(r'<article class="project"[^>]*>.*?</article>', enhance, markup, flags=re.S)
