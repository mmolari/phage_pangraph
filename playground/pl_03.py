# %%

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from Bio import Phylo

import pathlib

fig_fld = pathlib.Path("figs/pl3")
fig_fld.mkdir(parents=True, exist_ok=True)

df = pd.read_csv("../config/sarscov2.csv", parse_dates=["Collection_Date"])
df.set_index("Accession", inplace=True)


# %%
fig, axs = plt.subplots(1, 3, figsize=(12, 4))

ax = axs[0]
N = df["Host"].value_counts().size
ax.hist(
    df["Host"].sort_values(ascending=False),
    orientation="horizontal",
    rwidth=0.8,
    bins=np.arange(N + 1) - 0.5,
)
ax.set_xlabel("Count")
ax.set_ylabel("Host")

ax = axs[1]
N = df["Country"].value_counts().size
ax.hist(
    df["Country"],
    orientation="horizontal",
    rwidth=0.8,
    bins=np.arange(N + 1) - 0.5,
)
ax.set_xlabel("Count")
ax.set_ylabel("Country")

ax = axs[2]
# sns.histplot(
#     df["Collection_Date"],
#     ax=ax,
# )
ax.hist(df["Collection_Date"], bins=15)
ax.set_xticks(ax.get_xticks()[::4])
ax.set_xlabel("Collection Date")
ax.set_ylabel("Count")

sns.despine()
plt.tight_layout()
plt.savefig(fig_fld / "dset_stats.png", dpi=300)
plt.show()
# %%

# laod tree
tree = Phylo.read("../results/scov/tree/coretree-20-20-5.nwk", "newick")
tree.root_at_midpoint()
tree.ladderize()
# %%
host_cmap = {
    "Homo sapiens": "k",
    "Felis catus": "C0",
    "Odocoileus virginianus": "C1",
    "Canis lupus familiaris": "C2",
    "Neogale vison": "C3",
    "Panthera leo": "C4",
    "Panthera tigris": "darkviolet",
    "Panthera pardus fusca": "violet",
    "Mesocricetus auratus": "C5",
    "Mustela lutreola": "cyan",
    "Mustela putorius furo": "C9",
    "Mus musculus": "C8",
    "Tadarida brasiliensis": "yellow",
}


fig, axs = plt.subplots(
    1, 2, figsize=(8, 10), gridspec_kw={"width_ratios": [3, 1]}, sharey=True
)

ax = axs[0]
Phylo.draw(tree, branch_labels=lambda c: None, axes=ax, do_show=False)
ax.grid(alpha=0.3)

ax = axs[1]
leaves = [l.name for l in tree.get_terminals()]
for i, l in enumerate(leaves):
    row = df.loc[l]
    color = host_cmap[row["Host"]]
    ax.scatter([0], [i + 1], c=color, s=40, marker="s")
    ax.text(0.02, i + 1, row["Pangolin"], va="center", ha="left", fontsize=8)
ax.set_xlim(-0.01, 0.1)
# create custom legend from dictionary
handles = []
for k, v in host_cmap.items():
    handles.append(plt.scatter([], [], c=v, s=40, marker="s", label=k))
ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1, 0.5))
ax.set_xticks([])


plt.tight_layout()
sns.despine()
plt.savefig(fig_fld / "scov_coretree.png", dpi=300)
plt.show()
# %%

mash_dist_file = "../results/scov/mash_dist.csv"

# load df and pivot
df = pd.read_csv(mash_dist_file, index_col=[0, 1])
df = df.pivot_table(index="strain_1", columns="strain_2", values="mash_dist")

# get leaves order
leaves = [l.name for l in tree.get_terminals()]
df = df.loc[leaves, leaves]

# %%
fig, axs = plt.subplots(1, 2, figsize=(9, 5.7), gridspec_kw={"width_ratios": [1, 4]})

ax = axs[0]
Phylo.draw(tree, axes=ax, do_show=False, show_confidence=False, label_func=lambda x: "")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax = axs[1]
ms = ax.matshow(df)
cbar = fig.colorbar(ms, ax=ax, label="mash distance", shrink=0.8)


plt.tight_layout()
plt.savefig(fig_fld / "mash_dist.png")
plt.show()
# %%
