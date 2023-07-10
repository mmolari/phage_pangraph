# %%

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

import pypangraph as pp

from Bio import Phylo

# %%
acc_list_file = "../config/accession_numbers.csv"
df = pd.read_csv(acc_list_file)
df.set_index("genbank_accession", inplace=True)
df

# %%
print(df.groupby("species")["phage_name"].count().to_markdown())
species = "myoviridae_tevenvirinae"


# %%
# load tree for strain order
tree_file = f"../results/pangraph/{species}/coretree-20-20-5.nwk"
tree = Phylo.read(tree_file, "newick")
tree.root_at_midpoint()
tree.ladderize()

leaves = [l.name for l in tree.get_terminals()]
# %%

pan_file = f"../results/pangraph/{species}/20-20-5-polished.json"
pan = pp.Pangraph.load_json(pan_file)
# %%

# extract stat df
bdf = pan.to_blockstats_df()

# choose cmap
cmap = mpl.cm.get_cmap("rainbow")
np.random.seed(1)

# assign color to blocks
bl_color = {}
for bid, row in bdf.iterrows():
    if row.core:
        bl_color[bid] = "k"
    elif row.count == 1:
        bl_color[bid] = "gray"
    else:
        bl_color[bid] = cmap(np.random.rand())


fig, axs = plt.subplots(
    1, 2, figsize=(10, 10), gridspec_kw={"width_ratios": [1, 3]}, sharey=True
)

ax = axs[0]
Phylo.draw(
    tree, axes=ax, do_show=False, label_func=lambda x: None, show_confidence=False
)


def plot_block(b, e, y, c, ax):
    ax.plot([b, e], [y, y], color=c, lw=10)


ax = axs[1]
for nl, l in enumerate(leaves[::-1]):
    p = pan.paths[l]

    B = p.block_ids
    Pb = p.block_positions
    Pe = np.roll(Pb, -1)

    for b, pb, pe in zip(B, Pb, Pe):
        if pb > pe:
            pe, pb = pb, pe
            L = len(pan.blocks[b])
            plot_block(0, pb, nl + 1, bl_color[b], ax)
            plot_block(pe, pe + L - pb, nl + 1, bl_color[b], ax)
        else:
            plot_block(pb, pe, nl + 1, bl_color[b], ax)

plt.tight_layout()
plt.show()
# %%
