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
    parser.add_argument("--circular", action="store_true")
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
    cmap = mpl.cm.get_cmap("jet")
    np.random.seed(1)
    bl_color = {}
    for bid, row in bdf.iterrows():
        if row.core:
            bl_color[bid] = "k"
        elif row.count == 1:
            bl_color[bid] = "gray"
        else:
            bl_color[bid] = cmap(np.random.rand())

    # anchor on longest core block
    anchor_bid = None
    if args.circular:
        anchor_bid = bdf[bdf.core].sort_values("len", ascending=False).index[0]

    # plot
    def plot_block(b, e, y, c, ax):
        ax.plot([b, e], [y, y], color=c, lw=10)

    fig, axs = plt.subplots(
        1, 2, figsize=(12, 10), gridspec_kw={"width_ratios": [1, 4]}, sharey=True
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
    ax.grid(alpha=0.3)

    ax = axs[1]
    for nl, l in enumerate(leaves):
        p = pan.paths[l]

        B = p.block_ids
        Pb = p.block_positions
        Pe = np.roll(Pb, -1)

        if anchor_bid is not None:
            idx = list(B).index(anchor_bid)
            s = p.block_strands[idx]
            L = Pb.max() + len(pan.blocks[Pb.argmax()]) - Pb.min()
            if s:
                x = Pb[idx]
                Pb = (Pb - x) % L
                Pe = (Pe - x) % L
            else:
                # center on end of core block in question
                x = Pe[idx]
                Pb = (Pb - x) % L
                Pe = (Pe - x) % L
                # flip
                Pb, Pe = (-Pe) % L, (-Pb) % L

        for b, pb, pe in zip(B, Pb, Pe):
            if pb > pe:
                pe, pb = pb, pe
                L = len(pan.blocks[b])
                plot_block(0, pb, nl + 1, bl_color[b], ax)
                plot_block(pe, pe + L - pb, nl + 1, bl_color[b], ax)
            else:
                plot_block(pb, pe, nl + 1, bl_color[b], ax)
    ax.set_xlabel("genome position (bp)")
    ax.set_yticks(np.arange(len(leaves)) + 1)
    ax.set_yticklabels(leaves)

    plt.tight_layout()
    plt.savefig(args.fig)
    plt.close(fig)
