"""Validate active static pages, internal URLs, metadata, and project ownership."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
from collections import Counter
import re
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.refs=[];self.h1=0;self.images=[];self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  d=dict(attrs);self.tags.append((tag,d))
  if 'id' in d:self.ids.append(d['id'])
  if tag=='h1':self.h1+=1
  for key in ['src','href']:
   if key in d:self.refs.append(d[key])
  if tag=='img':self.images.append(d)
pages={f.name:Page(f.read_text()) for f in ROOT.glob('*.html')}
errors=[]
for name,p in pages.items():
 if p.h1!=1:errors.append(f'{name}: {p.h1} h1s')
 if any(v>1 for v in Counter(p.ids).values()):errors.append(f'{name}: duplicate ID')
 for im in p.images:
  if not im.get('alt'):errors.append(f'{name}: missing image alt')
 for ref in p.refs:
  u=urlparse(ref)
  if u.scheme or u.netloc:continue
  target=unquote(u.path) or name
  if (ROOT/target).is_dir():target=str(Path(target)/"index.html")
  if not (ROOT/target).is_file():errors.append(f'{name}: missing {target}')
  if u.fragment and target in pages and u.fragment not in pages[target].ids:errors.append(f'{name}: missing anchor {ref}')
 text=(ROOT/name).read_text()
 for bad in ['rishabhnmishra','info@yoursite.com','tel://0101010101','href="#"']:
  if bad in text:errors.append(f'{name}: placeholder {bad}')
 for marker in ['name="description"','rel="canonical"','name="viewport"','<main','Skip to content']:
  if marker not in text:errors.append(f'{name}: missing {marker}')
 for tag,attrs in p.tags:
  if tag=='script' and attrs.get('src') and urlparse(attrs['src']).path not in ['assets/portfolio.js','assets/latest-articles.js']:errors.append(f'{name}: unexpected runtime dependency')
print(f'{len(pages)} active pages; {sum(len(p.refs) for p in pages.values())} references checked')
if errors:raise SystemExit('\n'.join(errors))
print('PASS: internal files and anchors, unique IDs, headings, alt text, metadata, no placeholders, no legacy runtime dependencies')
