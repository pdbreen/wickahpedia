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
     world — Steve the email squirrel, Dr. Ambrose Molar, Mark (the
     founder, pre-cell-phones), Lord Thaddeus P.
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
7. **Round-two apparatus (mandatory since 2026-10-20):** every article also
   carries:
   - a **Last edited** line under the title (absurd editor + edit summary)
     and a **Read in another language** line (Louder English · Greg ·
     Topiary · Squirrel) followed by an empty `<div class="lang-note">`;
   - one **red link** in its See also list — a title from
     `content/articles/` that is *not* yet a live article, in this form:
     `<a href="#" class="red-link" data-title="…" data-conclusion="…">Title</a>`
     where the conclusion is the unwritten article's already-settled
     one-line verdict. Also add the same red link to the "Settled but
     Unwritten" list on the All Articles page;
   - a **Talk** section: two short fake editor comments (the second one
     closes the argument) in a `talk-box`, ending with the line "Editors
     who cite sources on talk pages are asked to leave.";
   - an **Improve this article** button + empty `improve-status` line
     (the site's JS handles it — clicking only raises Certainty);
   - a **Categories** line: 2–3 categories as `cat-link` anchors, reusing
     existing category names where they fit (the category page is built
     automatically from these links);
   - a **quality rating** shown next to its All Articles link, derived
     from Certainty: 99.0%+ = Doctrine; 98.0–98.9% = Fact (Wickahpedia);
     97.0–97.9% = Claim; under 97% = Rumor, Stated Loudly.
8. **Round-three apparatus (mandatory since 2026-10-20):** every article
   also carries, in this order and markup:
   - a **Read aloud** button right after the `lang-note` div:
     ```html
     <p><button class="readaloud-btn text-sm text-blue-700 hover:underline">Read aloud, confidently</button> <span class="text-sm text-gray-500">&mdash; narrated by a man who has never doubted anything.</span></p>
     ```
     (the site's JS handles the narration; no per-article configuration);
   - a **Cite this page** button + empty `cite-status` line in the toolbox
     next to the Improve button (the JS builds the citation from the
     article's title and Certainty — again, no per-article configuration);
   - a **View history** block right after the Escalation log, seeded with
     three fake revisions:
     ```html
     <details class="history-box mt-4 mb-2">
         <summary>View history</summary>
         <ul class="history-list text-sm text-gray-600 space-y-1 mt-2">
             <li><date> &mdash; <editor> created this article, confidently. The confidence has only grown.</li>
             <li><date> &mdash; <editor> escalated a claim (see Escalation log). The article thanked them.</li>
             <li><date> &mdash; A fact attempted to enter this article. It was shown the door.</li>
         </ul>
     </details>
     ```
     (the JS appends real entries when readers click Improve);
   - **On This Day:** the Front Page's On This Day box is driven by the
     `MONTHLY_OTD` array in the page script (one entry per month). If the
     new article suits a month, you MAY add or replace that month's entry
     in the array, in the existing format — keep the array at exactly 12
     entries.

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
                <p class="last-edited text-sm text-gray-500 mb-1">Last edited <when> by <Fake Editor> (talk) &mdash; edit summary: &lsquo;<joke>&rsquo;</p>
                <p class="text-sm text-gray-500 mb-4">Read in another language: <a href="#" class="lang-link" data-lang="louder">Louder English</a> &middot; <a href="#" class="lang-link" data-lang="greg">Greg</a> &middot; <a href="#" class="lang-link" data-lang="topiary">Topiary</a> &middot; <a href="#" class="lang-link" data-lang="squirrel">Squirrel</a></p>
                <div class="lang-note" style="display:none"></div>
                <p><button class="readaloud-btn text-sm text-blue-700 hover:underline">Read aloud, confidently</button> <span class="text-sm text-gray-500">&mdash; narrated by a man who has never doubted anything.</span></p>
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
                <details class="history-box mt-4 mb-2">
                    <summary>View history</summary>
                    <ul class="history-list text-sm text-gray-600 space-y-1 mt-2">
                        <li><date> &mdash; <editor> created this article, confidently. The confidence has only grown.</li>
                        <li><date> &mdash; <editor> escalated a claim (see Escalation log). The article thanked them.</li>
                        <li><date> &mdash; A fact attempted to enter this article. It was shown the door.</li>
                    </ul>
                </details>
                <h3 class="text-2xl font-bold section-heading mt-6 mb-3">Talk</h3>
                <div class="talk-box">
                    <p class="mb-2 leading-relaxed"><strong><Editor 1> (talk):</strong> <Objection></p>
                    <p class="mb-2 leading-relaxed"><strong><Editor 2> (talk):</strong> <Rebuttal that closes the matter></p>
                    <p class="text-sm text-gray-500">Editors who cite sources on talk pages are asked to leave.</p>
                </div>
                <div class="mt-6">
                    <button class="improve-btn bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200">Improve this article</button>
                    <p class="improve-status text-sm text-gray-600 mt-2"></p>
                    <button class="cite-btn bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200 ml-2">Cite this page</button>
                    <p class="cite-status text-sm text-gray-600 mt-2"></p>
                </div>
                <p class="cat-line text-sm border-t border-gray-200 pt-3 mt-6">Categories: <a href="#" class="cat-link" data-cat="<Category>"><Category></a> &middot; <a href="#" class="cat-link" data-cat="Settled Forever">Settled Forever</a></p>
            </section>
   ```
   (The See also list in the full template above must also include the one
   red link required by rule 7.)
   Use today's date (America/New_York) for `data-added` — the "Today's
   Nonsense" page lists articles newest-first by this attribute.

5. **Update the Front Page's Featured Article box** so it showcases the new
   article. In `index.html`, find the `front-box` whose `<h3>` reads
   "Featured Article" and replace its first `<p>` with:
   ```html
   <p class="leading-relaxed mb-3"><a href="#" class="wiki-link internal-link" data-page="<slug>"><Title></a> &mdash; <one confident, hilarious, entirely false sentence summarizing the article's premise>. Certainty: <X>%.</p>
   ```
   Use the new article's real title, slug, and Certainty percentage, and
   keep the box's second paragraph ("All other articles are also featured,
   in private…") exactly as it is. No hedging, per the Confidence Standard.

6. **Add the link** to the All Articles list in `index.html`, immediately
   after the `<!-- NEW ARTICLE LINKS GO HERE -->` marker, **with its
   quality rating** (see rule 7):
   ```html
                    <li><a href="#" class="wiki-link internal-link" data-page="<slug>"><Title></a> <span class="text-sm text-gray-500">&mdash; <Rating></span></li>
   ```
   Also add the article's red link to the "Settled but Unwritten" list on
   the All Articles page (same `red-link` markup as in its See also).

7. **Verify**: the new section's `id`, the link's `data-page`, and the image
   path all use the same slug; no `placehold.co` references remain; the
   article contains no banned hedging words (see the Confidence Standard);
   Certainty rows, the protection banner for its tier (if any), See also
   (including its red link), 3 References, the Escalation log, the seeded
   View history, Last edited + language lines, the Read aloud button,
   Talk, the Improve and Cite buttons, Categories, the rated All
   Articles link, and the updated Featured Article box are all present.

8. **Publish**: `git add -A && git commit -m "New article: <Title>" && git push`.
   Then report the new article's title and the fact that it's live at
   wickahpedia.com in the run's final message.

9. **Email the new article** to Patrick's Wickahpedia mailing list:
   pdbreen@gmail.com, jimforbush67@gmail.com, fupoon55@gmail.com, and
   mwick@wickone.com (Mark — the inspiration for the whole site).
   Send from Patrick's connected Gmail account:
   - Subject: `New from Wickahpedia: <Title>`
   - Body: the article's title, its one-line premise, and the full article
     text (the paragraphs, the expert quote, and its Certainty %), plus the
     link https://wickahpedia.com — the site is a single-page app, so
     readers find the new article via search or the All Articles list.
   - You MAY add a short, funny satirical aside for Mark when it fits the
     article. He is the site's inspiration: the pre-cell-phone family
     vacation where his confident table declaration became true because
     nobody could check. Keep it affectionate, never mean, and in the
     house style (confident, no hedging).
   If sending fails, report it plainly in the run's final message instead
   of claiming it went out.
