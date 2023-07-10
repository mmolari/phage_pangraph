import argparse
import pandas as pd
import matplotlib.pyplot as plt
from Bio import Phylo

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fig",type=str)
    parser.add_argument("--mash",type=str)
    parser.add_argument("--tree",type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # load df and pivot
    df = pd.read_csv(args.mash, index_col=[0, 1])
    df = df.pivot_table(index="strain_1", columns="strain_2", values="mash_dist")

    # load tree
    tree = Phylo.read(args.tree, "newick")
    tree.root_at_midpoint()
    tree.ladderize()

    # get leaves order
    leaves = [l.name for l in tree.get_terminals()]
    df = df.loc[leaves, leaves]

    fig, axs = plt.subplots(1, 2, figsize=(9, 5.7), gridspec_kw={"width_ratios": [1, 4]})

    ax = axs[0]
    Phylo.draw(tree, axes=ax, do_show=False, show_confidence=False, label_func=lambda x: "")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axs[1]
    ms = ax.matshow(df)
    cbar = fig.colorbar(ms, ax=ax, label="mash distance", shrink=0.8)


    plt.tight_layout()
    plt.savefig(args.fig, dpi=300)
    plt.close(fig)
