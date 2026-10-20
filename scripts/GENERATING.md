# How to add a new Wickahpedia article (procedure for the automated generator)

Site architecture: a single static `index.html` (Wikipedia parody SPA). Each
article is a `<section class="page-content" data-article="true">` inside
`<main>`. There is no build step — editing `index.html` and pushing to the
`main` branch publishes via GitHub Pages (wickahpedia.com).

## The Confidence Standard (house style — mandatory since 2026-10-20)

Wickahpedia's satire is that **confidence matters more than fact**. Every
article, new or old, must follow these rules:

1. **No hedging. Ever.** Banned words/phrases in article prose: *allegedly,
   reportedly, purportedly, might, may have, some say, critics argue, it is
   believed, possibly, perhaps, unconfirmed.* State every falsehood in a flat,
   academic, declarative tone. If a sentence sounds unsure, rewrite it until
   it sounds settled forever.
2. **Certainty apparatus.** Every infobox ends with four rows: `Certainty:`
   (a precise percentage between 96.0% and 99.9% — never 100%, that would be
   showing off), `Fact-checked:` (a joke refusal: "No", "Declined", "Steve
   was busy"…), `Peer review:` (an absurd reviewer), and `Hedging: None
   detected`.
3. **Protection tiers (not every article gets a banner).** An article's
   banner, placed right after the `<h2>` title, follows its Certainty %:
   - **99.0% and up — Protected** (full banner):
     ```html
     <div class="certainty-notice"><strong>Protected.</strong> This article has been locked to prevent the addition of facts. It may only be edited to become more confident.</div>
     ```
   - **98.0–98.9% — Semi-protected**:
     ```html
     <div class="certainty-notice"><strong>Semi-protected.</strong> This article may be edited only by editors who have not read it. Facts may knock, but they will not be let in.</div>
     ```
   - **Under 98.0% — no banner.** It hasn't earned protection yet.
4. **Fake scholarship.** Every article ends with, in this order:
   - a **See also** section linking to 2–3 *existing* Wickahpedia articles
     (use their real `data-page` slugs) — this is how the canon cross-proves
     itself;
   - a **References** section with exactly 3 fake citations (invented
     journals, books, archives, artifacts, or personal communications; at
     least one should cite an existing Wickahpedia character or article's
     world — Steve the email squirrel, Dr. Ambrose Molar, Lord Thaddeus P.
     Whimsy, Barty Cogsworth, the shrubs, etc.);
   - an **Escalation log** box (never a "correction"): one line recording
     how the claim was previously weaker and has now been *upgraded*:
     ```html
     <div class="escalation-box"><strong>Escalation log.</strong> Originally … Now …</div>
     ```
     Wickahpedia does not retract. It escalates.
5. **Required ingredients per article:** at least one hyper-precise number
   (a percentage, a count, a date to the day or minute — precision is not
   accuracy and does not need to be), at least one fake expert quote or
   named fake authority, and at least one callback to the existing canon.
6. **Editorial Policy (from the About page) governs all disputes:** we do
   not hedge; we do not correct, we escalate; citations are required,
   sources are optional; if two articles disagree, both are right.

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

   <One or two confident, hilarious, entirely false paragraphs. No hedging.>

   > “<Fake quote>.” — <Fake expert>, <Fake title>

   ## Citation
   1. <Fake citation>
   2. <Fake citation>
   3. <Fake citation>
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
   paragraph, infobox with 3–4 subject rows **plus the four Certainty rows**,
   the protection banner matching its Certainty tier (see rule 3 — under
   98.0%, omit the banner entirely), and the See also / References /
   Escalation log ending required by the Confidence Standard):
   ```html
            <section id="page-<slug>" class="page-content" data-article="true" data-added="YYYY-MM-DD">
                <h2 class="text-4xl font-extrabold mb-4 text-gray-900 leading-tight"><Title></h2>
                <!-- protection banner here IF Certainty >= 98.0% — see rule 3 for the two texts -->
                <div class="infobox float-right ml-6 mb-6 p-4 rounded-lg w-full sm:w-80 shadow-sm">
                    <h4 class="font-bold text-center text-xl mb-3 border-b pb-2"><Title></h4>
                    <img src="images/<slug>.jpg" alt="<Funny literal description of the image>" class="w-full h-auto rounded-md mb-3">
                    <table class="w-full text-sm">
                        <tr><td class="font-semibold pr-2 py-1"><Key>:</td><td class="py-1"><Value></td></tr>
                        <tr><td class="font-semibold pr-2 py-1">Certainty:</td><td class="py-1"><96.0–99.9>%</td></tr>
                        <tr><td class="font-semibold pr-2 py-1">Fact-checked:</td><td class="py-1"><Joke refusal></td></tr>
                        <tr><td class="font-semibold pr-2 py-1">Peer review:</td><td class="py-1"><Absurd reviewer></td></tr>
                        <tr><td class="font-semibold pr-2 py-1">Hedging:</td><td class="py-1">None detected</td></tr>
                    </table>
                </div>
                <p class="mb-4 leading-relaxed"><Opening paragraph></p>
                <p class="mb-6 leading-relaxed"><Second paragraph></p>
                <h3 class="text-2xl font-bold section-heading mt-6 mb-3"><Section heading></h3>
                <p class="mb-4 leading-relaxed"><Closing paragraph></p>
                <h3 class="text-2xl font-bold section-heading mt-6 mb-3">See also</h3>
                <ul class="list-disc list-inside mb-4 leading-relaxed">
                    <li><a href="#" class="wiki-link internal-link" data-page="<existing-slug>"><Existing Title></a></li>
                </ul>
                <h3 class="text-2xl font-bold section-heading mt-6 mb-3">References</h3>
                <ol class="list-decimal list-inside mb-4 leading-relaxed text-sm text-gray-700 space-y-1">
                    <li><Fake citation 1></li>
                    <li><Fake citation 2></li>
                    <li><Fake citation 3></li>
                </ol>
                <div class="escalation-box"><strong>Escalation log.</strong> <Originally weaker claim. Now upgraded claim.></div>
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
   path all use the same slug; no `placehold.co` references remain; the
   article contains no banned hedging words (see the Confidence Standard);
   Certainty rows, the protection banner for its tier (if any), See also,
   3 References, and the Escalation log are all present.

7. **Publish**: `git add -A && git commit -m "New article: <Title>" && git push`.
   Then report the new article's title and the fact that it's live at
   wickahpedia.com in the run's final message.
