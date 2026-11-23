# One-Step Flow Policy project page

A standalone, responsive academic website for **One-Step Flow Policy: Self-Distillation for Fast Visuomotor Policies** (ECCV 2026).

The page contains the author links and affiliations, university marks, arXiv link, a non-navigating ECCV 2026 button, the original abstract, Figures 1–6, Tables 1–2, and the author-provided BibTeX. Figures can be enlarged and opened as their original PDFs. Tables remain selectable text, with horizontal scrolling on small screens. Core content works without JavaScript.

All fonts, university marks, figures, and scripts are bundled locally. **No Node.js, framework, build step, or external CDN is required to publish.** Python dependencies are only needed if you regenerate the paper media.

## Preview locally

Download and extract the website ZIP, then open `index.html` in a browser. For the most reliable preview, including the clipboard button, serve the directory:

```bash
cd ofp-project-page
python3 -m http.server 8765 --bind 127.0.0.1
```

Open **http://localhost:8765/**. Stop the server with Ctrl+C. On Windows, `py -m http.server 8765` can be used instead.

If you run this command on a remote development server, forward port `8765` through your IDE before opening the localhost URL on your computer.

## Publish with GitHub Pages

Recommended repository: **`shaolonl-16/ofp`**.

Expected URL after deployment: **https://shaolonl-16.github.io/ofp/**.

This is the intended URL, not a claim that the site has already been published. Your existing personal homepage can stay in its own repository. A project repository adds the `/ofp/` path automatically. You do not need to purchase or separately register this URL.

1. Sign in to [GitHub](https://github.com/login) with your existing `shaolonl-16` account. If you do not have an account, use [Sign up](https://github.com/signup), verify your email, and substitute your username in the URLs below.
2. Open [New repository](https://github.com/new). Choose your account as **Owner**, enter **`ofp`** as the repository name, choose **Public**, and create the repository. If that name already exists, choose another name and use it in the project URL.
3. Extract the ZIP on your computer. On the empty repository page, select **uploading an existing file**. In a populated repository, use **Add file → Upload files**.
4. Upload the **contents inside** the extracted `ofp-project-page` folder, including `index.html`, `assets/`, `data/`, `scripts/`, and the documentation. Do not upload just the ZIP, and do not put an extra `ofp-project-page/` folder around the files. `index.html` must be directly at the repository root. Include `.nojekyll` if your file browser shows hidden files. Commit the upload to `main`.
5. Open the repository's **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, select **main** and **/(root)**, then **Save**.
6. Wait for the Pages deployment to complete. **Actions** shows the build/deployment status. Return to **Settings → Pages** and use **Visit site**. Deployment can take several minutes.
7. Open **https://shaolonl-16.github.io/ofp/**. Once published from this public repository, visitors can view the website without signing in to GitHub.

If the page returns 404, check that the deployment succeeded, `index.html` is at the root of `main`, and Pages is configured for `main` / `/(root)`. The repository URL (`github.com/shaolonl-16/ofp`) displays source files; the Pages URL (`shaolonl-16.github.io/ofp/`) displays the website.

If you choose a different account or repository name, update the `og:image` URL in `index.html` to match the final public address. The site's relative asset paths already work under different project subpaths.

Official instructions: [Create a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site) and [Configure a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Edit and update from your computer

After the first upload, clone the **website repository**, then make edits in that clone:

```bash
git clone https://github.com/shaolonl-16/ofp.git
cd ofp
python3 -m http.server 8765 --bind 127.0.0.1
```

| What to edit | File |
| --- | --- |
| Title, author URLs, affiliations, arXiv URL, explanations, citation | `index.html` |
| Colors, typography, spacing, mobile layouts | `assets/css/style.css` |
| Figure viewer and citation-copy behavior | `assets/js/main.js` |
| University marks | `assets/logos/` |
| Original PDF figures and browser previews | `assets/figures/` |
| Bundled manuscript | `assets/paper/OFP.pdf` |
| Exact table data and source LaTeX | `data/results.json`, `data/source-tables.tex` |
| Media provenance and PDF checksums | `data/asset-manifest.json`, `ASSET_SOURCES.md` |

The published tables live directly in `index.html`. Editing `data/results.json` alone does **not** update the website. Change the HTML table cells, or regenerate the tables from the updated manuscript with the script below. The ECCV badge is a `<button type="button">` with no navigation or click handler.

After previewing changes, push only the files you changed, for example:

```bash
git status --short
git add index.html assets/css/style.css assets/js/main.js
git diff --cached --stat
git commit -m "Update OFP project page"
git push origin main
```

GitHub Pages redeploys from `main`. For image or data changes, also stage the corresponding files under `assets/` or `data/`.

## Regenerate figures, abstract, and tables

The supplied LaTeX and PDF are the source of truth. The script renders all six original figure PDFs as 1200 px and 2400 px WebP files, preserves original figure PDFs, copies the supplied manuscript, extracts both tables without rounding, and updates the marked HTML blocks.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-media.txt
python scripts/prepare_assets.py --source /path/to/OFP --paper /path/to/OFP.pdf
```

Use an extracted LaTeX source directory containing `OFP.tex` and `figs/`. On Windows activate with `.venv\Scripts\activate`. The supplied source files are read only. Regeneration updates generated blocks in `index.html`, `data/`, and `assets/figures/`; it does not update manually written explanatory text or the social-sharing image.

## Content provenance

Results are taken from the author-supplied manuscript, not from new experiments. All reported evaluations are in simulation. The 56-task benchmark and the four-task RoboTwin integration study are separate evaluations. The reported 17.58 ms is the generation latency **per action chunk**. The speed comparison is against 100-step DP3 (3225.67 ms) and FM Policy (1865.72 ms), not a claim about the end-to-end latency of the entire VLA system.

The BibTeX follows the author's provided ECCV 2026 entry, including pages and organization. See `ASSET_SOURCES.md` for the mapping of paper figures to site assets and university-logo sources.
