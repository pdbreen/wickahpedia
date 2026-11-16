#!/usr/bin/env python3
"""Build Wickahpedia's static per-article pages and sitemap.xml from index.html.

The site is a single-page app: every article lives as a hidden <section> in
index.html and is shown by JavaScript, so no article has its own URL for
search engines. This script generates one crawlable page per article at
/<slug>/ (e.g. /toasters-are-time-machines/) plus a sitemap, from the live
sections in index.html. It is idempotent: re-running it rebuilds every page
and rewrites sitemap.xml from the current index.html.

Run from the repo root:  python3 scripts/build_article_pages.py

The Mon/Thu generator runs this after editing index.html and before commit
(see GENERATING.md). Stdlib only.
"""

import html
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
SITE = "https://wickahpedia.com"
TODAY = date.today().isoformat()
BEACON = (
    "<!-- Cloudflare Web Analytics -->"
    "<script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' "
    "data-cf-beacon='{\"token\": \"b054a8daf1074e269d1467f36f311aa5\"}'></script>"
    "<!-- End Cloudflare Web Analytics -->"
)

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_esc} &mdash; Wickahpedia</title>
    <meta name="description" content="{desc_esc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{url}">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title_esc}">
    <meta property="og:description" content="{desc_esc}">
    <meta property="og:url" content="{url}">
{og_image}    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title_esc}">
    <meta name="twitter:description" content="{desc_esc}">
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
{style_block}
    {beacon}
    <script type="application/ld+json">
{json_ld}
    </script>
</head>
<body class="p-4 sm:p-6 lg:p-8">
    <header class="bg-white p-4 shadow-md rounded-lg mb-6">
        <div class="flex items-center gap-3">
            <a href="/"><img src="/images/logo.jpg" alt="Wickahpedia Logo" class="w-12 h-12 mr-3 rounded-full shadow-inner"></a>
            <div>
                <div class="text-3xl font-bold text-gray-800"><a href="/" class="hover:underline">Wickahpedia</a></div>
                <a href="/" class="text-sm text-gray-500 hidden sm:block hover:text-gray-800 hover:underline">The Sum of All Misinformation</a>
            </div>
        </div>
    </header>
    <main class="w-full bg-white p-6 shadow-md rounded-lg">
        <div class="satire-note"><strong>Satire.</strong> Wickahpedia is a fictional encyclopedia &mdash; every claim on this page is made up, stated with total confidence. See Our Editorial Policy on the <a href="/" class="wiki-link">front page</a>.</div>
        <article>
{body}
        </article>
        <p class="text-sm text-gray-500 border-t border-gray-200 pt-3 mt-6"><a href="/" class="wiki-link">&larr; Back to the Front Page</a> &middot; Wickahpedia &mdash; The Sum of All Misinformation. Satirical and entirely fictional.</p>
    </main>
</body>
</html>
"""

SATIRE_CSS = (
    "\n        .satire-note { border-left: 4px solid #3366cc; background-color: #eef3fb;"
    " padding: 0.6rem 0.9rem; margin-bottom: 1rem; font-size: 0.92rem;"
    " border-radius: 0 6px 6px 0; }"
)


def strip_tags(text):
    return re.sub(r"<[^>]+>", "", text)


def clean_text(text):
    return re.sub(r"\s+", " ", html.unescape(strip_tags(text))).strip()


def main():
    source = INDEX.read_text(encoding="utf-8")

    style_match = re.search(r"<style>.*?</style>", source, re.DOTALL)
    if not style_match:
        print("ERROR: no <style> block found in index.html", file=sys.stderr)
        return 1
    style_block = style_match.group(0).replace(
        "</style>", SATIRE_CSS + "\n    </style>"
    )
    # Drop the SPA's hide/show rule: article pages must never hide content.
    style_block = re.sub(
        r"/\* Class to hide/show pages \*/\s*\.page-content\s*\{[^}]*\}",
        "",
        style_block,
    )

    sections = re.findall(r"<section\b[^>]*>.*?</section>", source, re.DOTALL)
    articles = []
    seen = set()
    errors = []
    warnings = []
    for section in sections:
        open_end = section.index(">")
        opentag = section[: open_end + 1]
        if 'data-article="true"' not in opentag:
            continue
        slug_match = re.search(r'id="page-([^"]+)"', opentag)
        if not slug_match:
            errors.append("article section without id=page-<slug>")
            continue
        slug = slug_match.group(1)
        if slug in seen:
            errors.append(f"duplicate article slug: {slug}")
            continue
        seen.add(slug)
        added_match = re.search(r'data-added="([^"]+)"', opentag)
        added = added_match.group(1) if added_match else None
        inner = section[open_end + 1 : section.rindex("</section>")]
        articles.append({"slug": slug, "added": added, "inner": inner})

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    if not articles:
        print("ERROR: no article sections found", file=sys.stderr)
        return 1

    slugs = {a["slug"] for a in articles}

    def rewrite_internal_link(match):
        target = match.group(1)
        text = match.group(2)
        if target in slugs:
            return f'<a href="/{target}/" class="wiki-link">{text}</a>'
        warnings.append(f"{slug}: non-article link target '{target}' -> /")
        return f'<a href="/" class="wiki-link">{text}</a>'

    built = []
    for a in articles:
        slug = a["slug"]
        inner = a["inner"]

        title_match = re.search(r"<h2[^>]*>(.*?)</h2>", inner, re.DOTALL)
        if not title_match:
            errors.append(f"{slug}: no <h2> title found")
            continue
        title = clean_text(title_match.group(1))

        prose_match = re.search(
            r"<p[^>]*leading-relaxed[^>]*>(.*?)</p>", inner, re.DOTALL
        )
        if not prose_match:
            errors.append(f"{slug}: no opening paragraph found")
            continue
        premise = clean_text(prose_match.group(1))
        # Sentence-aware truncation: accumulate whole sentences up to ~200
        # chars so the description never cuts mid-number or mid-phrase.
        fragments = re.split(r"(?<=[.!?])\s+", premise)
        sentences = []
        for frag in fragments:
            if sentences and len(sentences[-1]) < 20:
                sentences[-1] = sentences[-1] + " " + frag
            else:
                sentences.append(frag)
        kept = ""
        for sent in sentences:
            candidate = (kept + " " + sent).strip()
            if len(candidate) > 200 and kept:
                break
            kept = candidate
        if not kept:
            kept = premise[:190].rsplit(" ", 1)[0] + "…"
        description = kept + " Satirical article from Wickahpedia."

        img_match = re.search(r'<img\s+src="images/([^"]+)"', inner)
        image_file = img_match.group(1) if img_match else None
        if image_file and not (ROOT / "images" / image_file).exists():
            warnings.append(f"{slug}: image file missing: images/{image_file}")
            image_file = None
        if not image_file:
            warnings.append(f"{slug}: no image; page built without og:image")

        # --- Transform the section HTML into standalone-page HTML ---
        body = inner
        # Drop the empty language-note div and the JS-only read-aloud line.
        body = re.sub(r'<div class="lang-note"[^>]*></div>', "", body)
        body = re.sub(
            r"<p><button class=\"readaloud-btn[^\"]*\".*?</p>",
            "",
            body,
            flags=re.DOTALL,
        )
        # Drop the JS-only Improve/Cite button block.
        body = re.sub(
            r'<div class="mt-6">\s*<button class="improve-btn[^"]*".*?</div>',
            "",
            body,
            flags=re.DOTALL,
        )
        # Drop the SPA-only permalink line (the mirror page IS the URL).
        body = re.sub(
            r'<p[^>]*>[^<]*<a\b[^>]*class="permalink-copy[^"]*"[^>]*>[^<]*</a>\s*</p>',
            "",
            body,
        )
        # Internal links -> real article URLs (or / for SPA-only targets).
        body = re.sub(
            r'<a\b[^>]*data-page="([^"]+)"[^>]*>(.*?)</a>',
            rewrite_internal_link,
            body,
            flags=re.DOTALL,
        )
        # Red links (unwritten articles) -> styled plain text.
        body = re.sub(
            r'<a\b[^>]*class="red-link[^"]*"[^>]*>(.*?)</a>',
            r'<span class="red-link">\1</span>',
            body,
            flags=re.DOTALL,
        )
        # Category and language links -> plain text (SPA-only views).
        body = re.sub(
            r'<a\b[^>]*class="cat-link[^"]*"[^>]*>(.*?)</a>',
            r"\1",
            body,
            flags=re.DOTALL,
        )
        body = re.sub(
            r'<a\b[^>]*class="lang-link[^"]*"[^>]*>(.*?)</a>',
            r"\1",
            body,
            flags=re.DOTALL,
        )
        # Catch-all: any remaining dead "#" link (older hand-written ones
        # without data-page) -> plain text, so no dead link ships.
        body = re.sub(
            r'<a\b[^>]*href="#"[^>]*>(.*?)</a>',
            r"\1",
            body,
            flags=re.DOTALL,
        )
        # Absolute image paths (pages live one level down).
        body = body.replace('src="images/', 'src="/images/')
        # Heading hierarchy: article title h2 -> h1, section h3 -> h2.
        body = re.sub(r"<h2(\s[^>]*)?>", r"<h1\1>", body, count=1)
        body = body.replace("</h2>", "</h1>", 1)
        body = re.sub(r"<h3(\s[^>]*)?>", r"<h2\1>", body)
        body = body.replace("</h3>", "</h2>")

        leftovers = re.findall(r'href="#"|<button', body)
        if leftovers:
            warnings.append(f"{slug}: leftover dead links/buttons: {leftovers}")
        if "page-content" in body:
            warnings.append(f"{slug}: 'page-content' class survived transform")

        url = f"{SITE}/{slug}/"
        title_esc = html.escape(title, quote=True)
        desc_esc = html.escape(description, quote=True)
        og_image = ""
        image_url = None
        if image_file:
            image_url = f"{SITE}/images/{image_file}"
            og_image = (
                f'    <meta property="og:image" content="{image_url}">\n'
                f'    <meta property="og:image:alt" content="{title_esc}">\n'
            )
        ld = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description,
            "mainEntityOfPage": url,
            "author": {
                "@type": "Organization",
                "name": "Wickahpedia",
                "url": SITE + "/",
            },
            "publisher": {
                "@type": "Organization",
                "name": "Wickahpedia",
                "url": SITE + "/",
                "logo": {
                    "@type": "ImageObject",
                    "url": SITE + "/images/logo.jpg",
                },
            },
        }
        if image_url:
            ld["image"] = [image_url]
        if a["added"]:
            ld["datePublished"] = a["added"]
            ld["dateModified"] = a["added"]
        json_ld = json.dumps(ld, indent=4, ensure_ascii=False)

        page = PAGE_TEMPLATE.format(
            title_esc=title_esc,
            desc_esc=desc_esc,
            url=url,
            og_image=og_image,
            style_block=style_block,
            beacon=BEACON,
            json_ld=json_ld,
            body=body,
        )
        outdir = ROOT / slug
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "index.html").write_text(page, encoding="utf-8")
        built.append(a)

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    # --- Sitemap: homepage first, then articles newest-first ---
    def sort_key(a):
        return a["added"] or "0000-00-00"

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        "  <url>",
        f"    <loc>{SITE}/</loc>",
        f"    <lastmod>{TODAY}</lastmod>",
        "    <changefreq>weekly</changefreq>",
        "    <priority>1.0</priority>",
        "  </url>",
    ]
    for a in sorted(built, key=sort_key, reverse=True):
        lines += [
            "  <url>",
            f"    <loc>{SITE}/{a['slug']}/</loc>",
            f"    <lastmod>{a['added'] or TODAY}</lastmod>",
            "    <changefreq>monthly</changefreq>",
            "    <priority>0.8</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Built {len(built)} article pages + sitemap.xml ({len(built) + 1} URLs)")
    for w in warnings:
        print(f"WARNING: {w}")
    no_date = [a["slug"] for a in built if not a["added"]]
    if no_date:
        print(f"NOTE: no data-added (sitemap lastmod=today, no dates in schema): "
              f"{', '.join(no_date)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
