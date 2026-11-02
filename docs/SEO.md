# Profile content and Google SEO

Updated November 1, 2026. The original portfolio repository is unchanged. This work applies only to `Muhammadumaramin/portfolio`.

## Content

The current stylesheet and visual design are preserved. The home page now explains Umar's role, channels, leadership scope, expertise, and working approach. A resume link is prominent. About connects his international e-commerce experience, mathematics education, teaching, analytics, and current management role. Experience includes buyer planning and reporting responsibilities. Projects now distinguishes professional practice from academic research, without inventing case-study outcomes or exposing employer data.

No unverified sales-growth claims, testimonials, certifications, or awards were added.

## Implemented on the website

- Six unique descriptive titles and meta descriptions; natural coverage of the person's name, e-commerce management, Amazon 1P/3P, Walmart, marketplace operations, analytics, and San Antonio.
- Crawlable HTML with content visible without JavaScript; clear headings and descriptive internal links.
- Homepage canonical is `https://muhammadumaramin.github.io/portfolio/`. The `/index.html` copy points to that same canonical. Other pages have self-referencing canonicals. Navigation home links and sitemap use the preferred root URL.
- JSON-LD Person, WebSite, and WebPage entities, with ProfilePage on About. Shared identity connects name, existing professional profiles, role, employer, education, and expertise. No ratings or invented social statistics.
- Open Graph and Twitter metadata, image descriptions and dimensions, and a descriptive portrait alt attribute.
- A six-URL XML sitemap, without duplicate homepage variants. Explicit index/follow instructions on normal pages.
- Existing HTTPS and lightweight static runtime retained.

## Robots scope

Google reads robots.txt at the origin root, `https://muhammadumaramin.github.io/robots.txt`, not at `/portfolio/robots.txt`. The existing project-level robots file is retained, but is not represented as an effective origin-level crawl policy. Editing the origin root could involve another repository, so it is outside the user's authorization to change only this portfolio. The sitemap should be submitted directly through Search Console. A missing root robots.txt does not itself block crawling.

## Verification performed

- Local file/anchor, heading, image alt, and placeholder checks.
- JSON-LD JSON parsing and Person/ProfilePage identity-reference checks (not a claim of Google rich-result eligibility or a completed Rich Results Test).
- Unique metadata; canonical, Open Graph URL, and sitemap agreement.
- Stylesheet byte-for-byte unchanged.
- Desktop visual review and narrow/tablet overflow checks.
- Public HTTP checks after Pages deployment.

## Search Console and ongoing visibility

Search Console has not been connected, site ownership has not been verified there, and no sitemap submission or indexing request has been made on the user's behalf.

Use a URL-prefix property for `https://muhammadumaramin.github.io/portfolio/`. Domain verification requires DNS ownership, which a GitHub Pages project does not provide. With the owner's Google account, obtain the exact HTML verification file or tag from Google, add it unchanged to this repository, complete verification, submit `sitemap.xml`, and inspect the homepage and About URL. Do not invent a verification token. Do not remove a verification file/tag after it succeeds.

The six-page website can support discovery for the person's name and relevant professional context. Broad competitive terms such as “Amazon expert” are not promised ranking targets. Further useful evidence includes permissioned work samples and specific documented outcomes. Add the new website link to the user's LinkedIn and GitHub profile manually or through separately authorized profile edits. Do not change other profiles without permission.

No guaranteed rankings, indexing deadlines, or rich-result display are promised. Search Console setup and sitemap submission are discovery/measurement tools, not ranking guarantees.

## Official references

- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/essentials
- https://developers.google.com/search/docs/appearance/structured-data/profile-page
- https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://support.google.com/webmasters/answer/9008080
- https://support.google.com/webmasters/answer/34592
