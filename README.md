# Muhammad Umar Amin · Portfolio

Personal portfolio: e-commerce leadership, marketplace strategy and quantitative analytics.

## GitHub Pages

Publish main branch, / (root), in Settings → Pages. Expected URL after a successful deployment: https://muhammadumaramin.github.io/portfolio/

This is a separate website. The original portfolio repository is unchanged.

## Content maintenance

Edit scripts/build_portfolio.py, run python scripts/build_portfolio.py, then python scripts/check_portfolio.py. No build packages required.

The home page and resume page offer a downloadable, searchable two-page PDF at `output/pdf/Muhammad_Umar_Amin_Resume.pdf`. The resume page also supports Print / Save as PDF. Rebuild the download with `python scripts/build_resume.py` (requires pdfLaTeX and the packages in the user-provided template; source is in `resume-source/`).

## Content and search visibility

See [SEO and content notes](docs/SEO.md) for implemented metadata, profile structured data, validation, and remaining Search Console verification.

## Research and recognition

`research.html` presents verified coauthored publications, conference participation, and selected honors. Edit `content/research.json`, then run `python scripts/research_content.py`. This also updates the homepage highlights, shared Research navigation, and sitemap. See [research maintenance and source notes](docs/RESEARCH.md). The homepage continues to show the latest four journal articles.

## Project visuals

Project previews and full-size images live in `images/projects/`. `sources.json` records each original repository file, extraction location, caption, and source checksum. Keep charts and screenshots faithful to their sources. The stock app uses its repository cover image, clearly labeled as a cover. Market Basket Analysis and Bank Loan SQL Analysis have no available original visual yet.

`scripts/project_visuals.py` adds the previews when the portfolio is built. New media needs a manifest entry with the matching project number, accessible alt text, preview dimensions, and original source link. Preview images are lazy-loaded; full-size copies open only when selected.

