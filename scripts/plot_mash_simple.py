import argparse
import pandas as pd
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from Bio import Phylo


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fig", type=str)
    parser.add_argument("--mash", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # load df and pivot
    df = pd.read_csv(args.mash, index_col=[0, 1])
    df = df.pivot_table(index="strain_1", columns="strain_2", values="mash_dist")

    # find order using hierarchical clustering
    dist = sch.distance.pdist(df)
    linkage = sch.linkage(dist, method="complete")
    order = sch.leaves_list(linkage)
    strains = df.index.to_numpy()
    str_order = strains[order]

    df = df.loc[str_order, str_order]

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    ms = ax.matshow(df)
    cbar = fig.colorbar(ms, ax=ax, label="mash distance", shrink=0.8)

    # strain labels
    ax.set_xticks(range(len(str_order)))
    ax.set_yticks(range(len(str_order)))
    ax.set_xticklabels(str_order, rotation=90)
    ax.set_yticklabels(str_order)

    plt.tight_layout()
    plt.savefig(args.fig, dpi=300)
    plt.close(fig)
