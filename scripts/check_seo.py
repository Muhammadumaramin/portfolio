"""Check metadata and entity consistency; does not emulate Google's indexer."""
from pathlib import Path
from html.parser import HTMLParser
import json
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://muhammadumaramin.github.io/portfolio/'
class Head(HTMLParser):
 def __init__(self):
  super().__init__(); self.capture=None; self.text={}; self.tags=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a))
  if tag=='title' or (tag=='script' and a.get('type')=='application/ld+json'):
   self.capture=tag;self.text.setdefault(tag,'')
 def handle_data(self,data):
  if self.capture:self.text[self.capture]+=data
 def handle_endtag(self,tag):
  if tag==self.capture:self.capture=None
urls=[];titles=[];descriptions=[]
for f in sorted(ROOT.glob('*.html')):
 p=Head();p.feed(f.read_text())
 meta={a.get('name',a.get('property')):a.get('content') for t,a in p.tags if t=='meta'}
 canonical=[a['href'] for t,a in p.tags if t=='link' and a.get('rel')=='canonical']
 expected=BASE if f.name=='index.html' else BASE+f.name
 assert canonical==[expected],(f.name,canonical)
 assert meta['og:url']==expected
 assert 'noindex' not in meta['robots'] and 'index' in meta['robots']
 assert meta['description'] and meta['author']=='Muhammad Umar Amin'
 assert meta['og:title']
 if 'twitter:title' in meta:assert meta['twitter:title']==p.text['title']
 schema=json.loads(p.text['script']) if p.text.get('script') else None
 if schema and '@graph' in schema:
  assert meta['og:title']==p.text['title']
  assert meta['twitter:title']==p.text['title']
  graph=schema['@graph']
  person=next(x for x in graph if x['@type']=='Person')
  assert person['name']=='Muhammad Umar Amin' and person['@id']==BASE+'#person'
  page=next(x for x in graph if x['@type'] in ['WebPage','ProfilePage'])
  assert page['url']==expected
  if f.name=='about.html':
   assert page['@type']=='ProfilePage' and page['mainEntity']['@id']==person['@id']
  if f.name=='research.html':
   records=json.loads((ROOT/'content/research.json').read_text())['publications']
   papers=[x for x in graph if x['@type']=='ScholarlyArticle']
   assert len(papers)==len(records)
   assert {x['url'] for x in papers}=={x['url'] for x in records}
   assert all({'@id':person['@id']} in x['author'] for x in papers)
 elif schema:
  assert schema['@type']=='BlogPosting'
  assert schema['mainEntityOfPage']==expected
  assert schema['author']['name']=='Muhammad Umar Amin'
 else:
  assert f.name=='blog.html',f'{f.name}: missing structured data'
 urls.append(expected);titles.append(p.text['title']);descriptions.append(meta['description'])
assert len(titles)==len(set(titles)) and len(descriptions)==len(set(descriptions))
locs=[x.text for x in ET.parse(ROOT/'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert set(locs)==set(urls) and len(locs)==len(set(locs))
print(f'PASS: {len(urls)} pages; unique titles/descriptions; canonical, available social metadata, portfolio/research/blog schema and sitemap agreement')
