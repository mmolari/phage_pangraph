#import "template.typ": *

#show: project.with(
  title: "SarsCov2 dataset",
  authors: (
    "Marco Molari",
  ),
  abstract: [
    Description of sars-cov-2 dataset selection, processing and results.
  ],
  date: "July 10, 2023",
)

= Dataset Preparation

I ran a search on the #link("https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&VirusLineage_ss=SARS-CoV-2,%20taxid:2697049&HostLineage_ss=NOT%20Homo%20sapiens%20(human),%20taxid:NOT%209606&Completeness_s=complete&LabHost_s=exclude&QualNum_i=10")[NCBI SARS-Cov-2 data hub] for covid sequences with the following requirements:
- complete genome
- not human host
- max 10 ambiguous bases

This resulted in 451 sequences. I then excluded the ones without host identification, and selected one random sample per unique host/pango-lineage pairing. This resulted in 56 different sequences.

I also manually curated annotations, removing slighlty ambiguous `ON966106` (_Canis lupus_), `MT628700` (_Feliformia_), `OL913104` (_Rodentia_). I simplified `Panthera leo persica` into `Pandthera leo`. I removed `MT365033` (_Panthera tigris jacksoni_, already present as _Panthera tigris_). This leaves us with 52 isolates.

#figure( image("assets/n1/dset_stats.png", width: 100%))

= Pangraph Generation and Core Genome Tree

I generate a pangraph with minimap kernel and options `-a 20 -b 5`. The graph is almost completely alignable, except for some short overhangs missing in one strain (`MW064259`) around the edges. The core genome has a size of $~29$ kbp.

#figure( image("assets/n1/pangraph_export.png", width: 30%))

Using the aligned core genome, which corresponds to almost the full genome, I build a core-genome tree, displayed in @fig_coretree. Very similar isolates can infect different hosts.

#figure( image("assets/n1/scov_coretree.png", width: 80%),
    caption: [
        Core-genome tree of 52 SARS-Cov-2 isolates from different-non human host. For each isolate we report the host and the corresponding pango lineage.
    ]
) <fig_coretree>

The mash distance for all of the isolates remains below 0.5%.

#figure( image("assets/n1/mash_dist.png", width: 80%))