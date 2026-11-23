#!/usr/bin/env python3
"""Render original paper figures and regenerate static tables/abstract. No build is needed to publish."""
import argparse
import hashlib
import html
import json
import re
import shutil
from pathlib import Path

import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FIGURES = {1: "fig_freq", 2: "fig_overview", 3: "fig_warmstart", 4: "fig_demo", 5: "fig_pi05", 6: "fig_rbt"}
DESCRIPTIONS = {
    1: "Success rate versus inference time across 56 simulated tasks. OFP combines the highest average success rate with one-step inference.",
    2: "OFP self-distillation overview: self-consistency training matches interval-averaged velocities, while self-guided training sharpens action predictions.",
    3: "Warm-start action generation: shift the unexecuted action suffix, pad with the terminal action, add noise, and condition the next prediction on a new observation.",
    4: "DexArt Faucet data scaling: OFP success rates are 32.7, 39.3, 45.7, and 51.0 percent with 20, 50, 100, and 150 demonstrations.",
    5: "RoboTwin 2.0 integration with pi 0.5. OFP uses one generation step and achieves 94.7 percent average success across four tasks.",
    6: "Four RoboTwin 2.0 simulation tasks: Handover Mic, Place Empty Cup, Adjust Bottle, and Beat Block Hammer.",
}


def replace_block(document, name, content):
    pattern = rf"(<!-- BEGIN {name} -->).*?(<!-- END {name} -->)"
    result, count = re.subn(pattern, lambda m: m[1] + "\n" + content + "\n" + m[2], document, flags=re.S)
    if count != 1:
        raise ValueError(f"Expected one {name} block, found {count}")
    return result


def read_table(tex, label, columns):
    block = next(b for b in re.findall(r"\\begin\{table\*\}.*?\\end\{table\*\}", tex, re.S) if f"\\label{{{label}}}" in b)
    rows = []
    for line in block.splitlines():
        if not re.match(r"(?:DP3?|FM Policy|CP|OneDP|MP1|\\textbf\{OFP)", line):
            continue
        cells = line.split(" & ")
        method = re.sub(r"\\textbf\{(.*?)\}", r"\1", cells[0])
        values = []
        for cell in cells[2:]:
            mean, std = re.search(r"([\d.]+)\$\\pm\$([\d.]+)", cell).groups()
            values.append({"mean": mean, "std": std, "highlight": "cellcolor" in cell})
        assert len(values) == len(columns) - 2
        rows.append({"method": method, "nfe": int(cells[1]), "values": values})
    assert len(rows) == 8
    return {"columns": columns, "rows": rows}, block


def table_html(data, number):
    lines = [f'<table id="results-table-{number}">', f'<caption class="sr-only">Table {number}. Success rate in percent, mean ± standard deviation over three random seeds.</caption>', '<thead><tr>']
    for i, column in enumerate(data["columns"]):
        # Task count remains readable on a separate line in the 3D table.
        label = html.escape(column)
        label = re.sub(r" \((\d+)\)$", r"<small>\1 tasks</small>", label)
        lines.append(f'<th scope="col">{label}</th>')
    lines.append('</tr></thead><tbody>')
    for i, row in enumerate(data["rows"]):
        classes = "ours" if row["method"].startswith("OFP") else ("group-start" if i == 4 else "")
        lines.append(f'<tr class="{classes}"><th scope="row">{html.escape(row["method"])}</th><td>{row["nfe"]}</td>')
        for value in row["values"]:
            content = f'{value["mean"]}<span class="uncertainty"> ± {value["std"]}</span>'
            if value["highlight"]:
                content = f'<strong>{content}</strong>'
            lines.append(f'<td class="{"best" if value["highlight"] else ""}">{content}</td>')
        lines.append('</tr>')
    lines.append('</tbody></table>')
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True, help='Directory containing OFP.tex and figs/')
    parser.add_argument('--paper', type=Path, required=True, help='Author-supplied paper PDF')
    args = parser.parse_args()
    tex = (args.source / 'OFP.tex').read_text()
    document = (ROOT / 'index.html').read_text()
    for name in ['assets/figures', 'assets/paper', 'data']:
        (ROOT / name).mkdir(parents=True, exist_ok=True)
    manifest = {'paper_sha256': hashlib.sha256(args.paper.read_bytes()).hexdigest(), 'figures': {}}
    shutil.copy2(args.paper, ROOT / 'assets/paper/OFP.pdf')
    for number, name in FIGURES.items():
        source = args.source / 'figs' / (name + '.pdf')
        dest = ROOT / 'assets/figures' / f'figure-{number}'
        shutil.copy2(source, dest.with_suffix('.pdf'))
        with pymupdf.open(source) as pdf:
            page = pdf[0]
            for width in [1200, 2400]:
                pix = page.get_pixmap(matrix=pymupdf.Matrix(width / page.rect.width, width / page.rect.width), alpha=False)
                im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
                im.save(str(dest) + f'-{width}.webp', quality=92, method=6)
            w, h = im.size
        manifest['figures'][str(number)] = {'source': f'figs/{name}.pdf', 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'width': w, 'height': h}
        loading = 'eager' if number == 1 else 'lazy'
        sizes = '(max-width: 760px) 94vw, 580px' if number in [1, 4] else '(max-width: 1160px) 94vw, 1100px'
        figure = f'''<a class="figure-zoom" href="assets/figures/figure-{number}-2400.webp" data-figure="{number}" aria-label="Enlarge Figure {number}">
  <img src="assets/figures/figure-{number}-1200.webp" srcset="assets/figures/figure-{number}-1200.webp 1200w, assets/figures/figure-{number}-2400.webp 2400w" sizes="{sizes}" width="{w}" height="{h}" alt="{DESCRIPTIONS[number]}" loading="{loading}" decoding="async">
  <span class="zoom-hint" aria-hidden="true">↗</span>
</a>'''
        document = replace_block(document, f'FIGURE_{number}', figure)
    abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S)[1].strip()
    abstract = html.escape(abstract).replace('$100\\times$', '100×').replace('$\\pi_{0.5}$', 'π<sub>0.5</sub>')
    document = replace_block(document, 'ABSTRACT', '<p>' + abstract + '</p>')
    tables = {}
    source_blocks = []
    for number, label, columns in [
        (1, 'tab:2d_results', ['Method', 'NFE', 'Door', 'Hammer', 'Pen', 'Bucket', 'Faucet', 'Laptop', 'Toilet', 'Average']),
        (2, 'tab:3d_results', ['Method', 'NFE', 'Adroit (3)', 'DexArt (4)', 'MetaWorld Easy (28)', 'MetaWorld Medium (11)', 'MetaWorld Hard (5)', 'MetaWorld Very Hard (5)', 'Average']),
    ]:
        data, source_block = read_table(tex, label, columns)
        tables[str(number)] = data
        source_blocks.append(source_block)
        document = replace_block(document, f'TABLE_{number}', table_html(data, number))
    (ROOT / 'index.html').write_text(document)
    (ROOT / 'data/results.json').write_text(json.dumps(tables, indent=2) + '\n')
    (ROOT / 'data/source-tables.tex').write_text('\n\n'.join(source_blocks) + '\n')
    (ROOT / 'data/asset-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared 6 original figures, 2 tables (16 rows), the abstract, and the paper PDF.')


if __name__ == '__main__':
    main()
