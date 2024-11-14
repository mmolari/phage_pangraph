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


fig, axs = plt.subplots(2, 1, figsize=(12, 5))


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
fig.savefig(fig_fld / "where_core.png")
plt.show()

# %%
