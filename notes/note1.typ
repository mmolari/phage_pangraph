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

#figure( image("assets/n1/dset_stats.png", width: 100%))

I generate a pangraph with minimap kernel and options `-a 20 -b 5`. The graph is almost completely alignable, except for some short overhangs missing in one strain (`MW064259`) around the edges.

#figure( image("assets/n1/pangraph_export.png", width: 30%))