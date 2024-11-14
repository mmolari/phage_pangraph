# %%
import pypangraph as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pathlib
from Bio import SeqIO
import seaborn as sns

fig_fld = pathlib.Path("fig")
fig_fld.mkdir(exist_ok=True)

graph_fname = "../../results/pangraph/aionostat/20-0-0-polished.json"
pan = pp.Pangraph.load_json(graph_fname)
bdf = pan.to_blockstats_df()
ref_iso = {
    "hybrid_ref": "hybrid_ref",
    "MaxBurger": "MZ501093",
    "WalterGehring": "MZ501111",
}

N = len(pan.strains())

Ls = {}
for name, iso in ref_iso.items():
    fa_file = f"../../raw_data/fa/{iso}.fa"
    for record in SeqIO.parse(fa_file, "fasta"):
        Ls[name] = len(record.seq)
        break
# %%


def segment(ax, s, e, b):
    freq = bdf.loc[b, "n. strains"] / N
    dupl = bdf.loc[b, "duplicated"]
    core = (freq == 1) and (not dupl)

    color = {
        (True, False): "C0",
        (False, True): "red",
        (False, False): "C1",
    }.get((core, dupl), "black")

    ax.plot([s, e], [freq, freq], color=color, lw=1)

    # if core:
    #     ax.fill_between([s, e], 0, freq, color="C0", alpha=1, zorder=-2)


fig, axs = plt.subplots(3, 1, figsize=(15, 7.5))


for axi, (name, iso) in enumerate(ref_iso.items()):
    print(name, iso)
    ax = axs[axi]
    path = pan.paths[iso]
    B = path.block_ids
    P = path.block_positions

    for i, b in enumerate(B):
        s, e = P[i], P[i + 1]
        if e > s:
            segment(ax, s, e, b)
        else:
            for pair in ((s, Ls[name]), (0, e)):
                segment(ax, *pair, b)

    ax.set_title(name)
    ax.set_xlabel("genome position (bp)")
    ax.set_ylabel("block frequency")
    ax.set_ylim(0, 1)
    ax.set_xlim(0, Ls[name])
    ax.grid(axis="x", alpha=0.2)

sns.despine()
plt.tight_layout()
fig.savefig(fig_fld / "where_core.png", dpi=300)
plt.show()

# %%

fig, axs = plt.subplots(3, 1, figsize=(15, 7.5))

name = "hybrid_ref"
iso = ref_iso[name]
for axi, (x0, x1) in enumerate([(0, 1 / 3), (1 / 3, 2 / 3), (2 / 3, 1)]):
    x0, x1 = x0 * Ls["hybrid_ref"], x1 * Ls["hybrid_ref"]

    ax = axs[axi]
    path = pan.paths[iso]
    B = path.block_ids
    P = path.block_positions

    for i, b in enumerate(B):
        s, e = P[i], P[i + 1]
        if e > s:
            segment(ax, s, e, b)
        else:
            for pair in ((s, Ls[name]), (0, e)):
                segment(ax, *pair, b)

    ax.set_title(name)
    ax.set_xlabel("genome position (bp)")
    ax.set_ylabel("block frequency")
    ax.set_ylim(0, 1)
    ax.set_xlim(0, Ls[name])
    ax.grid(axis="x", alpha=0.2)
    ax.set_xlim(x0, x1)

sns.despine()
plt.tight_layout()
fig.savefig(fig_fld / "hybrid_ref_zoom.png", dpi=300)
plt.show()

# %%
