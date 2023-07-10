import argparse
import numpy as np

import pypangraph as pp

from Bio import SeqIO, Seq
from collections import defaultdict


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pangraph", type=str)
    parser.add_argument("--aln", type=str)
    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()

    # load graph
    pan = pp.Pangraph.load_json(args.pangraph)

    # get core blocks
    df = pan.to_blockstats_df()
    CB = df[df["core"]].index.to_list()

    # build alignments
    alns = defaultdict(str)
    for bid in CB:
        b = pan.blocks[bid]
        aln, occs = b.alignment.generate_alignments()

        for a, o in zip(aln, occs):
            strain = o[0]
            alns[strain] += a

    # verify that all lines have the same length
    Ls = [len(a) for a in alns.values()]
    assert np.all(np.array(Ls) == Ls[0])

    # export alignment
    recs = []
    for k, a in alns.items():
        recs.append(SeqIO.SeqRecord(Seq.Seq(a), id=k, description=""))
    SeqIO.write(recs, args.aln, "fasta")
