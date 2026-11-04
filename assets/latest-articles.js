/* The blog index is the source of truth: append numbered articles there and the homepage follows automatically. */
(function () {
  'use strict';
  function selectLatest(posts) {
    return posts.sort((a,b) => b.sequence-a.sequence).slice(0,5);
  }
  async function refreshArticles() {
    const target=document.querySelector('[data-latest-articles]');
    if (!target) return;
    try {
      const response=await fetch('blog.html', {cache:'no-cache'});
      if (!response.ok) return;
      const page=new DOMParser().parseFromString(await response.text(),'text/html');
      const posts=[];
      page.querySelectorAll('article.featured').forEach(card=>{
        const link=card.querySelector('h2 a');
        const sequence=Number((card.querySelector('.eyebrow')?.textContent.match(/Article\s+(\d+)/i)||[])[1]);
        if(!link || !sequence) return;
        const url=new URL(link.getAttribute('href'),response.url || location.href);
        if(url.origin!==location.origin || !url.pathname.startsWith(new URL('.',location.href).pathname)) return;
        const heading=card.querySelector('h2');
        posts.push({sequence,url:url.href,title:link.textContent.trim(),summary:heading.nextElementSibling?.textContent.trim()||'',meta:card.querySelector('.post-meta')?.textContent.trim()||''});
      });
      const latest=selectLatest(posts);
      if(!latest.length) return; // Keep the accessible, server-rendered fallback on any load failure.
      const fragment=document.createDocumentFragment();
      latest.forEach(post=>{
        const article=document.createElement('article');article.className='home-article';
        const category=document.createElement('p');category.className='eyebrow';category.textContent='Article '+String(post.sequence).padStart(2,'0');
        const heading=document.createElement('h3');
        const title=document.createElement('a');title.href=post.url;title.textContent=post.title;heading.append(title);
        const summary=document.createElement('p');summary.textContent=post.summary;
        const meta=document.createElement('p');meta.className='home-article-meta';meta.textContent=post.meta;
        const read=document.createElement('a');read.className='text-link';read.href=post.url;read.textContent='Read full article →';
        article.append(category,heading,summary,meta,read);fragment.append(article);
      });
      target.replaceChildren(fragment);
    } catch (_) { /* Preserve the fallback when offline. */ }
  }
  refreshArticles();
})();
