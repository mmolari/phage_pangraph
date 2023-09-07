import argparse

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import pypangraph as pp

from Bio import Phylo
from collections import defaultdict


def parse_args():
    parser = argparse.ArgumentParser(
        description="""
        Given a backbone joints pangraph and the core-genome tree, it groups identical
        paths in categories and displays the categories in a figure, along with the
        tree.
        """
    )
    parser.add_argument("--pangraph", type=str)
    parser.add_argument("--tree", type=str)
    parser.add_argument("--fig", type=str)
    parser.add_argument("--len_filt", type=int, default=0)
    return parser.parse_args()


class Node:
    """Combination of block id and strandedness"""

    def __init__(self, bid: str, strand: bool) -> None:
        self.id = bid
        self.strand = strand

    def invert(self) -> "Node":
        return Node(self.id, not self.strand)

    def __eq__(self, other: object) -> bool:
        return self.id == other.id and self.strand == other.strand

    def __hash__(self) -> int:
        return hash((self.id, self.strand))

    def __repr__(self) -> str:
        s = "+" if self.strand else "-"
        return f"[{self.id}|{s}]"

    def to_str_id(self):
        s = "f" if self.strand else "r"
        return f"{self.id}_{s}"

    @staticmethod
    def from_str_id(t) -> "Node":
        bid = t.split("_")[0]
        strand = True if t.split("_")[1] == "f" else False
        return Node(bid, strand)


class Path:
    """A path is a list of nodes"""

    def __init__(self, nodes=[]) -> None:
        self.nodes = nodes

    def add_left(self, node: Node) -> None:
        self.nodes.insert(0, node)

    def add_right(self, node: Node) -> None:
        self.nodes.append(node)

    def invert(self) -> "Path":
        return Path([n.invert() for n in self.nodes[::-1]])

    def __eq__(self, o: object) -> bool:
        return self.nodes == o.nodes

    def __hash__(self) -> int:
        return hash(tuple(self.nodes))

    def __repr__(self) -> str:
        return "_".join([str(n) for n in self.nodes])

    def __len__(self) -> int:
        return len(self.nodes)

    def to_list(self):
        return [n.to_str_id() for n in self.nodes]

    @staticmethod
    def from_list(path_list) -> "Path":
        return Path([Node.from_str_id(nid) for nid in path_list])


class Edge:
    """Oriented link between two nodes/paths"""

    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def invert(self) -> "Edge":
        return Edge(self.right.invert(), self.left.invert())

    def __side_eq__(self, o: object) -> bool:
        return self.left == o.left and self.right == o.right

    def __eq__(self, o: object) -> bool:
        return self.__side_eq__(o) or self.__side_eq__(o.invert())

    def __side_hash__(self) -> int:
        return hash((self.left, self.right))

    def __hash__(self) -> int:
        return self.__side_hash__() ^ self.invert().__side_hash__()

    def __repr__(self) -> str:
        return f"{self.left} <--> {self.right}"

    def to_str_id(self) -> list:
        return "__".join([self.left.to_str_id(), self.right.to_str_id()])

    @staticmethod
    def from_str_id(t) -> "Edge":
        left, right = t.split("__")
        return Edge(Node.from_str_id(left), Node.from_str_id(right))


def pangraph_to_path_dict(pan):
    """Creates a dictionary isolate -> path objects"""
    res = {}
    for path in pan.paths:
        name = path.name
        B = path.block_ids
        S = path.block_strands
        nodes = [Node(b, s) for b, s in zip(B, S)]
        res[name] = Path(nodes)
    return res


def filter_paths(paths, keep_f):
    """Given a filter function, removes nodes that fail the condition from
    the path dictionaries."""
    res = {}
    for iso, path in paths.items():
        filt_path = Path([node for node in path.nodes if keep_f(node.id)])
        res[iso] = filt_path
    return res


def path_categories(paths):
    """Returns a list of touples, one per non-empty path, with the following info:
    (count, path, [list of isolates])"""
    iso_list = defaultdict(list)
    n_paths = defaultdict(int)
    nodes = {}
    for iso, path in paths.items():
        if len(path.nodes) > 0:
            n_paths[path] += 1
            iso_list[path].append(iso)
            nodes[path] = path.nodes

    # sort by count
    path_cat = [(count, nodes[path], iso_list[path]) for path, count in n_paths.items()]
    path_cat.sort(key=lambda x: x[0], reverse=True)
    return path_cat


def plot_row(ax, nodes, y, colors, block_df):
    x = 0
    for node in nodes:
        color = colors[node.id]
        l = block_df["len"][node.id]
        h = block_df["duplicated"][node.id] * 0.2 + 0.4
        core = block_df["core"][node.id]
        edge_color = "black" if node.strand else "red"
        ax.barh(
            y,
            l,
            height=h,
            left=x,
            color=color,
            edgecolor=edge_color,
            hatch="." if core else None,
        )
        x += l


def plot_categories(path_categories, block_df, tree_file):
    # load tree
    tree = Phylo.read(tree_file, "newick")
    tree.ladderize()
    leaves = [n for n in tree.get_terminals()]

    # assign colors to leaves
    C = len(path_categories)

    if C <= 10:
        path_colors = mpl.cm.get_cmap("tab10")(np.arange(C))
    elif C <= 20:
        path_colors = mpl.cm.get_cmap("tab20")(np.arange(C))
    else:
        path_colors = mpl.cm.get_cmap("jet")(np.linspace(0, 1, C))

    strain_color = defaultdict(lambda: "white")
    for i, (_, _, isolates) in enumerate(path_categories):
        for iso in isolates:
            strain_color[iso] = path_colors[i]

    # assign color to blocks
    N_blocks = len(block_df)
    colors = mpl.cm.get_cmap("rainbow")(np.linspace(0, 1, N_blocks))
    np.random.shuffle(colors)
    block_color = {block: colors[i] for i, block in enumerate(block_df.index)}

    fig, axs = plt.subplots(
        1, 2, figsize=(20, 15), gridspec_kw={"width_ratios": [1, 3]}
    )

    ax = axs[0]
    Phylo.draw(
        tree,
        axes=ax,
        do_show=False,
        show_confidence=False,
        label_func=lambda x: x.name if x in leaves else "",
        label_colors=lambda x: strain_color[x],
    )
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    ax = axs[1]
    for i, (count, nodes, isolates) in enumerate(path_categories):
        plot_row(ax, nodes, -i, block_color, block_df)
        ax.text(
            0,
            -i + 0.45,
            f"path {i+1} | n = {count}",
            color=path_colors[i],
            fontsize=20,
        )

    ax.set_yticks([])
    ax.set_ylim(-len(path_categories) + 0.5, 0.5)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("position")

    plt.tight_layout()
    return fig, axs


if __name__ == "__main__":
    args = parse_args()

    # extract edge name
    edge = args.pangraph.split("/")[-1].split(".")[0]

    # load pangraph
    pan = pp.Pangraph.load_json(args.pangraph)
    bdf = pan.to_blockstats_df()
    block_len = bdf["len"].to_dict()
    is_core = bdf["core"].to_dict()
    is_dupl = bdf["duplicated"].to_dict()

    # build paths
    paths = pangraph_to_path_dict(pan)

    # optional: clean up paths
    if args.len_filt > 0:
        paths = filter_paths(paths, lambda x: block_len[x] >= args.len_filt)
        bdf = bdf[bdf["len"] >= args.len_filt].copy()

    # subdivide paths into categories
    path_cat = path_categories(paths)

    # plot
    fig, axs = plot_categories(path_cat, bdf, args.tree)
    axs[1].set_title(f"{edge}")
    plt.savefig(args.fig, facecolor="w")
    plt.close(fig)
