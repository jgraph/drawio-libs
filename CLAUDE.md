# CLAUDE.md — drawio-libs

Public draw.io/diagrams.net library collection. Files in `libs/` are mxlibrary
XML served raw via jgraph.github.io (from `main`) and loaded into the app with
`?clibs=U<encoded-url>`. This repo is also the **ingestion front door for icon
search**: the `drawio-icons` corpus (`~/dev/drawio-icons`) enumerates every
`libs/**/*.xml` here and builds the D1/Vectorize index behind
`icons.diagrams.net` / `app.diagrams.net/iconSearch2` (worker source:
`~/dev/mxgraph-gliffy-java/cf-workers/icon-search2`). A change here is not
finished until the server side is regenerated (see checklist below).

## Library format

Two entry types inside `<mxlibrary title="...">[JSON array]</mxlibrary>`:

- **Recolorable mono** (`xml` entries): uncompressed, entity-escaped
  mxGraphModel wrapping one image cell whose style carries
  `editableCssRules=.*` and a base64 SVG. The SVG embeds
  `<style type="text/css">.shape_fill{fill:#000000;}</style>` (or
  `.shape_outline{stroke:...}`, plus `.shape_solid{fill:...}` for solid detail
  paths in stroke sets) and wraps content in `<g class="...">`. The editor
  (`Graph.canonicalizeSvgCssRules`) lifts fill/stroke/stop-color from matching
  `<style>` rules into editable light-dark colors — **inline color attributes
  are invisible to it and must be stripped at build time**. Reference entries:
  `libs/hero-icons.xml`, `libs/tabler/tabler-outline.xml` (shape_solid example:
  the "Accessible" icon).
- **Color** (`data` entries): plain base64 SVG data URIs, artwork untouched.
  Reference: `libs/flat-color-icons.xml`, `libs/fluent-emoji/fluent-emoji.xml`.

## Building or refreshing a set

Use the committed pipeline — do not hand-roll conversions:

```
python3 tools/build_lib.py --mode mono-fill|mono-stroke|color \
  --src <flat-svg-dir> --out libs/<set>/<unique-name>.xml \
  --set-title "Pretty Name" --w 48 --h 48 [--title-map map.json] \
  [--strip-prefix/-suffix ...] [--exclude RE] [--expect N] [--report r.json]
python3 tools/validate_lib.py libs/<set>/*.xml --contact-sheet /tmp/sheet.html
```

Conventions (each learned the hard way):

- **Basename = corpus slug and must be globally unique across all of
  `libs/**`** (`build-libs.js` uses `basename(file, '.xml')` only). Use
  `tabler-outline.xml`, never `outline.xml` inside a folder.
- The `<mxlibrary title>` attribute feeds both the app's sidebar section name
  and the corpus set name. Always set it.
- **Every entry needs a human-readable `title`** — titles are the only search
  signal for these sets (FTS name column, weight 4.0; entries without titles
  are captured but unsearchable). Names must come from upstream metadata, not
  invention (e.g. flags use upstream `country.json`, format "Name (CODE)").
- One style per file; split sets over ~4,000 icons into per-style files
  (Fortinet-folder pattern). Mono entries average ~1.2–1.5 KB, color emoji
  ~4.5 KB; material-symbols at 4.9 MB and tabler-outline at 6 MB are the
  accepted size ceiling precedents.
- Successor/upstream-redesign sets get NEW filenames; old files stay for
  raw-URL stability. Same-set version bumps replace in place.
- Pin upstream exactly (npm pack version or git commit SHA) and record it in
  the README entry text with a date.
- MIT/Apache/ISC sets: copy the upstream license text to `libs/<set>/LICENSE`
  (redistribution condition). CC0/public-domain sets need no file.
- Trademark policy: brand glyphs *inside* general sets are kept (FA
  solid+brands precedent), but standalone logo collections are avoided, and
  vendor UI sets get curated (GitLab: tanuki + third-party marks like
  github/kubernetes/terraform/zoom excluded; also skip `file_icons/`-style
  third-party logo dirs).
- Stage downloads/extractions OUTSIDE the repo (temp/scratch dir); only
  `libs/**` and `tools/**` belong in git.

## After adding or updating a library — full checklist

1. **Validate**: `tools/validate_lib.py` must print OK (structure, decode,
   script/foreignObject/external-href bans, titles). Eyeball the contact
   sheet.
2. **README.md**: add/update the entry in the house HTML-list format — clibs
   link (jgraph.github.io URL, URL-encoded; multi-file sets get multi-U
   links), icon count, "recolorable" where true, license, upstream link,
   version/commit + date. Add caveat sub-bullets where needed.
3. **Commit + push both branches**: `git push origin main main:review`
   (review==main is the resting state; PRs from others target `review`;
   jgraph.github.io serves `main`). Push early, per set — don't batch at
   session end.
4. **In-app spot check** via the raw URL (available immediately, no Pages
   delay):
   `https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fjgraph%2Fdrawio-libs%2Fmain%2Flibs%2F<path>`
   — sidebar section name correct, icons render, and for mono sets select a
   shape and confirm the `.shape_fill`/`.shape_outline` swatch appears in
   Format → Style and recolors (values are light-dark pairs; on a dark canvas
   the dark value renders).
5. **Regenerate the server side** (`~/dev/drawio-icons`, runbooks in
   `corpus/README.md` and `cf-workers/icon-search2/README.md` — follow those;
   summary of the non-obvious parts):
   - Run the six-builder chain; review `derived/libs-report.json` for expected
     counts and zero unwrap errors.
   - Upload staged R2 assets and regenerated libraries/site BEFORE the new
     index goes live; never probe an icons.diagrams.net URL before its object
     is uploaded (pre-upload 404s get edge-pinned).
   - **Any libs change shifts enumeration-ordered icon ids → re-embed and
     re-upsert ALL vectors** (delete `corpus/derived/vectors/checkpoint.json`
     first).
   - Load a FRESH D1 database, bump `INDEX_VERSION`, `wrangler deploy`.
6. If the set closes or affects a GitHub issue, comment/close it.

## License bar and vetted landmines (verified against primary sources 2026-07-19)

Only add sets whose assets are CC0/public-domain/Unlicense/MIT/ISC/BSD/
Apache-2.0. CC-BY(-SA/-ND), OFL, GPL family, link-back and custom licenses
fail. The ASSET license governs, not the repo/npm code license.

Known traps (do not re-litigate without re-checking, licenses change):
- **Remix Icon**: relicensed 2026-01-25; new terms ban standalone icon-pack
  redistribution (≤ v4.6.x stays Apache-2.0). css.gg, Iconscout Unicons,
  PrimeIcons (new), Iconsax, Line Awesome ("Good Boy License"), Solar (no
  license), Geist (no license) — all fail.
- CC-BY family fails: VS Code Codicons, Twemoji, OpenMoji (SA), Game Icons,
  Salesforce SLDS icons (npm says BSD-3 but that's code-only; icons are
  CC-BY-ND), UN-OCHA "Humanitarian Icons 2026" (v.02 stays CC0), Reactome.
- **Arcticons is CC-BY-SA, not CC0** as widely claimed. Sargam's LICENSE is a
  modified MIT with distribute/sell removed. Shopify Polaris is
  Shopify-restricted MIT. Elastic EUI is SSPL/Elastic-2.0.
- Surprise passes: Hugeicons free tier is MIT (ships as JS data, not SVGs);
  Adobe Spectrum workflow icons and Atlassian's npm `@atlaskit/icon` are
  genuinely Apache-2.0.
- Sets already requested in issues (don't duplicate as "candidates"): Simple
  Icons (#24), opencontainers artwork (#3), DevOps tool logos (#8),
  bioicons (#11).

## Technical gotchas learned building the 2026-07 wave

- Mono conversion must strip fill/stroke colors from attributes AND `style`
  attrs, but **preserve `fill="none"`** (cutouts) and opacity attributes
  (Phosphor duotone = same color at `opacity="0.2"` — one editable color).
- Stroke sets can hide solid detail paths (`fill="currentColor"` — 49 Tabler
  outline icons); the builder auto-assigns them `.shape_solid` so they stay
  recolorable. Watch the builder's residual-colour warnings for anything else.
- Color mode must NOT strip `class` attrs or `<style>` elements — color SVGs
  may style via classes.
- Multi-size upstreams (Fluent: `<name>_<size>_<style>.svg`): pick 24px,
  fall back nearest (20/28/32/16/48/12/10). Multi-size dirs (Carbon svg/32
  master + 9 root-only 16px strays): prefer largest, take strays.
- Emoji-scale repos: use `git clone --depth 1 --filter=blob:none --sparse`
  with targeted patterns (fluentui-emoji full checkout is huge; Flat-only is
  14 MB). Big single-repo tarballs can carry 170+ MB of site assets
  (healthicons) — extract selectively.
- Flag SVGs with coats of arms are huge (Serbia 237 KB); expected, keep.
- Upstream duplicate filenames across category dirs are real (healthicons
  `fever` in devices AND emotions) — rename + title-map "(Category)".
- circle-flags ships ~200 symlink alias files — dedupe by content, and don't
  derive ISO codes from language-dir aliases (Sami ≠ Sweden).
- Meteocons "line" style is multicolored artwork, not mono — shipped as color.
- drawio quirks: the editor only checks `documentElement.nodeName ==
  'mxlibrary'`, so the `title` attribute is safe everywhere; entry `w`/`h` is
  the default drop size (icons scale from viewBox — 48 is the house default,
  30 for map pins, 64 for pictograms).
