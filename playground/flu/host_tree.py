# %%

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from Bio import Phylo

import pathlib

fig_fld = pathlib.Path("figs")
fig_fld.mkdir(parents=True, exist_ok=True)

df = pd.read_csv("../../config/flu_dataset.csv", parse_dates=["year"])
df.set_index("acc", inplace=True)

# %%

# laod tree
tree = Phylo.read("../../results/flu/tree/coretree-20-20-5.nwk", "newick")
tree.root_at_midpoint()
tree.ladderize()
# %%
host_cmap = {
    "human": "C0",
    "swine": "C1",
    "chicken": "C2",
    "duck": "C3",
    "mallard": "C4",
    "ruddy turnstone": "C5",
    "environment": "C6",
    "turkey": "C7",
}

str_cmap = {acc: host_cmap[row["host"]] for acc, row in df.iterrows()}


fig, ax = plt.subplots(1, 1, figsize=(6, 9))

Phylo.draw(
    tree,
    branch_labels=lambda c: None,
    axes=ax,
    do_show=False,
    label_colors=lambda n: str_cmap[n],
)
# ax.grid(alpha=0.3)

# leaves = [l.name for l in tree.get_terminals()]
# for i, l in enumerate(leaves):
#     row = df.loc[l]
#     color = host_cmap[row["host"]]
#     ax.scatter([0], [i + 1], c=color, s=40, marker="s")
# ax.set_xlim(-0.01, 0.1)
# create custom legend from dictionary
handles = []
for k, v in host_cmap.items():
    handles.append(plt.scatter([], [], c=v, s=40, marker="s", label=k))
ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1, 0.5))
# ax.set_xticks([])


plt.tight_layout()
sns.despine()
plt.savefig(fig_fld / "flu_coretree.png", dpi=300)
plt.show()
# %%
