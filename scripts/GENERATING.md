# How to add a new Wickahpedia article (procedure for the automated generator)

Site architecture: a single static `index.html` (Wikipedia parody SPA). Each
article is a `<section class="page-content" data-article="true">` inside
`<main>`. There is no build step — editing `index.html` and pushing to the
`main` branch publishes via GitHub Pages (wickahpedia.com).

## Each run adds exactly ONE new article

1. **Pick a topic.** Historical event, scientific concept, or everyday object
   — treated with total, confident wrongness in an academic tone. Check
   `content/articles/` and the existing `data-page` links in `index.html` so
   the topic (and slug) is new. Slug = lowercase, words joined by `-`,
   short (e.g. `traffic-lights-are-suggestions`).

2. **Write the markdown twin** at `content/articles/<slug>.md`, matching the
   existing entries' format:
   ```
   # <Title>

   <One or two confident, hilarious, entirely false paragraphs.>

   > “<Fake quote>.” — <Fake expert>, <Fake title>

   ## Citation
   1. <Fake citation>
   ```

3. **Generate the image** with the media image tool (one call):
   prompt = "Vintage encyclopedia plate illustration, faded etching/engraving
   style, serious scientific textbook presentation of an absurd subject:
   <one-line description of the article's central false claim, visualized>."
   Landscape. Then save it as `images/<slug>.jpg`, resized to max width
   900px, JPEG quality 80 (the other article images are ~150–200 KB).

4. **Insert the article section** into `index.html` immediately after the
   `<!-- NEW ARTICLES GO HERE -->` marker comment, using this template
   (2 paragraphs minimum, one `##`-style section heading with a third
   paragraph, infobox with 3–4 rows):
   ```html
            <section id="page-<slug>" class="page-content" data-article="true" data-added="YYYY-MM-DD">
                <h2 class="text-4xl font-extrabold mb-4 text-gray-900 leading-tight"><Title></h2>
                <div class="infobox float-right ml-6 mb-6 p-4 rounded-lg w-full sm:w-80 shadow-sm">
                    <h4 class="font-bold text-center text-xl mb-3 border-b pb-2"><Title></h4>
                    <img src="images/<slug>.jpg" alt="<Funny literal description of the image>" class="w-full h-auto rounded-md mb-3">
                    <table class="w-full text-sm">
                        <tr><td class="font-semibold pr-2 py-1"><Key>:</td><td class="py-1"><Value></td></tr>
                    </table>
                </div>
                <p class="mb-4 leading-relaxed"><Opening paragraph></p>
                <p class="mb-6 leading-relaxed"><Second paragraph></p>
                <h3 class="text-2xl font-bold section-heading mt-6 mb-3"><Section heading></h3>
                <p class="mb-4 leading-relaxed"><Closing paragraph></p>
            </section>
   ```
   Use today's date (America/New_York) for `data-added` — the "Today's
   Nonsense" page lists articles newest-first by this attribute.

5. **Add the link** to the All Articles list in `index.html`, immediately
   after the `<!-- NEW ARTICLE LINKS GO HERE -->` marker:
   ```html
                    <li><a href="#" class="wiki-link internal-link" data-page="<slug>"><Title></a></li>
   ```

6. **Verify**: the new section's `id`, the link's `data-page`, and the image
   path all use the same slug; no `placehold.co` references remain.

7. **Publish**: `git add -A && git commit -m "New article: <Title>" && git push`.
   Then report the new article's title and the fact that it's live at
   wickahpedia.com in the run's final message.
