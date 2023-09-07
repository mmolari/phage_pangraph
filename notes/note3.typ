#import "template.typ": *

#show: project.with(
  title: "Influenza A hemagglutinin dataset",
  authors: (
    "Marco Molari",
  ),
  abstract: [
    Notes.
  ],
  date: "August 14, 2023",
)

= Influenza A Hemagglutinin

I searched NCBI nucleotide (7/09/23) for the keyword `influenza A segment 4 hemagglutinin complete cds` with `genomic DNA/RNA` constraint and length between 300 and 3000 bp. This gives 141938 results. I download the summary file from NCBI.

I parse this file and extract host and type information. For the 8 prevalent hosts, I select at most random 10 sequences with the constraint that they must all belong to different sequence types.

These sequence types are however too diverged to be merged into a single graph.

#figure(image("assets/n3/flu_all_mash.png", width: 80%), 
  caption: [mash distance matrix between isolates in the dataset.]
)
#figure(image("assets/n3/flu_all_bandage.png", width: 60%), 
  caption: [flu bandage graph.]
)

Therefore I restrict the dataset to sequences of type `H1N1` and sample 10 random sequences per host. Sequences are divided in two large clades. Sequences from the different clades are again highly diverged, and separated in two different paths.

#figure(image("assets/n3/flu_mash_h1n1.png", width: 70%), 
  caption: [mash distance matrix between isolates in the `H1N1` dataset.]
)

If we restrict the graph to the first clade, we get a graph composed of a single block, and a core-genome tree compatible with the mash distance matrix.

#figure(image("assets/n3/flu_coretree_clade.png", width: 60%), 
  caption: [core-genome .]
)