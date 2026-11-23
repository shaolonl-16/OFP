# Local validation

The revised website was rendered and inspected in Chromium on 2026-11-23 after removing the university logos and project icon and reducing the displayed figure sizes. The existing browser and source-fidelity check completed again with **87 of 87 checks passing**, with no JavaScript errors, failed asset requests, or HTTP errors.

- All 120 mean/standard-deviation pairs in Tables 1–2 match the supplied paper PDF. The rendered table rows, NFE values, decimal precision, and order also match the extracted LaTeX data.
- All six bundled original figure PDFs are byte-identical to the source files. The served manuscript matches the author-supplied `OFP.pdf`.
- All three author destinations and the arXiv destination match the requested URLs. Clicking or keyboard-activating the ECCV 2026 button does not navigate.
- All six figure viewers load the intended image and original PDF. Zooming, restoring the full image, closing with Escape or the close button, and restoring keyboard focus were checked.
- Citation copying was checked against the exact provided BibTeX, including the fallback when clipboard access is denied.
- Layouts were checked at widths of 1440, 1024, 768, 760, 441, 440, 390, and 320 pixels. No page-wide horizontal overflow was found. Mobile tables scroll within their own regions, and enlarged figures fit the dialog with additional zoom available.
- Core content and figure links were checked with JavaScript disabled. All local assets resolve under the `/ofp/` project path used by GitHub Pages.
- Desktop, mobile, method, results, VLA, and citation screenshots were generated and visually inspected. A separate social-sharing image was generated from the original Figure 1.
- The author header now contains linked names and text affiliations only. The navigation uses plain OFP text, and the custom favicon declaration and unused icon files have been removed.
- Desktop figures use smaller width limits: 460 px for Figures 1 and 4, 850 px for Figures 2 and 5, 600 px for Figure 3, and 900 px for Figure 6. Figures retain their aspect ratios and high-resolution zoom views. Header spacing, section spacing, and mobile author alignment were adjusted accordingly.

The raw verification report and browser scripts are in the adjacent `ofp-project-page-preview/` working directory. They are not needed for deployment.

This is local validation of the static website. The GitHub repository and public Pages deployment have not been created or published by this task.
