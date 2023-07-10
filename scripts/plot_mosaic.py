import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import pypangraph as pp
import argparse
from Bio import Phylo


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tree", type=str)
    parser.add_argument("--pan", type=str)
    parser.add_argument("--fig", type=str)
    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()

    # load tree
    tree = Phylo.read(args.tree, "newick")
    tree.root_at_midpoint()
    tree.ladderize()

    # list of leaves
    leaves = [l.name for l in tree.get_terminals()]

    # load pangraph
    pan = pp.Pangraph.load_json(args.pan)

    # assign colors to blocks
    bdf = pan.to_blockstats_df()
    cmap = mpl.cm.get_cmap("rainbow")
    np.random.seed(1)
    bl_color = {}
    for bid, row in bdf.iterrows():
        if row.core:
            bl_color[bid] = "k"
        elif row.count == 1:
            bl_color[bid] = "gray"
        else:
            bl_color[bid] = cmap(np.random.rand())

    # plot
    def plot_block(b, e, y, c, ax):
        ax.plot([b, e], [y, y], color=c, lw=10)

    fig, axs = plt.subplots(
        1, 2, figsize=(10, 10), gridspec_kw={"width_ratios": [1, 3]}, sharey=True
    )

    ax = axs[0]
    Phylo.draw(
        tree,
        axes=ax,
        do_show=False,
        label_func=lambda x: None,
        show_confidence=False,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

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
    ax.set_xlabel("genome position (bp)")

    plt.tight_layout()
    plt.savefig(args.fig)
    plt.close(fig)
