#import "template.typ": *

#show: project.with(
  title: "E.coli phages dataset",
  authors: (
    "Marco Molari",
  ),
  abstract: [
    Description of diversity in the phage dataset.
  ],
  date: "July 10, 2023",
)

#outline()

= Dataset Preparation

I downloaded accession for phages from the _Basel collection_ @maffei2021systematic. This include both phages isolated from the Rhine river, and other related phages from NCBI, for a total of 284 genomes. They are divided in 10 different categories:


```
| species                                  |        count |
|:-----------------------------------------|-------------:|
| drexlerviridae                           |           51 |
| myoviridae_tevenvirinae                  |           44 |
| myoviridae_vequintavirinae_and_relatives |           35 |
| demerecviridae_markadamsvirinae          |           28 |
| autographiviridae                        |           24 |
| siphoviridae_dhillonvirus                |           16 |
| schitoviridae                            |           15 |
| siphoviridae_queuovirinae_seuratvirus    |           14 |
| myoviridae_ounavirinae                   |           13 |
| siphoviridae_queuovirinae_sonagvirus     |            8 |
```

= Workflow

For genomes in each cagegory, I run the following workflow:
+ estimate diversity with mash. This gives a rough estimate of the amount of shared genome and how diverged it is.
+ generate a pangenome graph using _pangraph_ with minimap2 kernel and options `-s 20 -a 20 -b 5`.
+ if core geneome is present, generate a core genome tree using `fasttree`.

= Results

== Drexlerviridae

This category includes very diverged genomes for which no common core sequences at less than 20% divergence can be found.

#figure(image("assets/n2/drexlerviridae/bandage.png", width: 50%), 
  caption: "Drexlerviridae pangenome graph, visualized using bandage"
)

#figure(image("assets/n2/drexlerviridae/mash_dist_simple.png", width: 70%), 
  caption: "mash distance matrix for Drexlerviridae. Some isolates have mash distance > 50%."
)

== Myoviridae Tevenvirinae

Genomes in this category have a common core backbone. Both the core-genome divergence and mash distance separates these genomes in two clades. Within-clade core-genome divergence is < 5%, while across-clade comparisons are around 20% divergence, with many differing fragments. Core genome is only a small fraction of the whole genome.

#figure(image("assets/n2/myoviridae_tevenvirinae/bandage.png", width: 50%), 
  caption: [
    Myoviridae Tevenvirinae pangenome graph, visualized using bandage. Genomes have a common core backbone.
  ]
)

#figure(image("assets/n2/myoviridae_tevenvirinae/mash_dist.png", width: 80%), 
  caption: "core-genome tree and mash distance matrix for Myoviridae Tevenvirinae."
)

#figure(image("assets/n2/myoviridae_tevenvirinae/mosaic.png", width: 100%), 
  caption: [
    linear representation for the Myoviridae Tevenvirinae pangenome graph. Black blocks are core, and blocks of the same kind have the same color.
  ]
)

== Myoviridae Vequintavirinae and relatives

Genomes in this category are divided in two main clades, without a shared common core backbone.

#figure(image("assets/n2/myoviridae_vequintavirinae_and_relatives/mash_dist_simple.png", width: 45%), 
  caption: "Myoviridae Vequintavirinae pangenome graph, visualized using bandage."
)

== Demerecviridae Markadamsvirinae

Genomes in this category have a common core backbone. Both the core-genome divergence and mash distance roughly separates these genomes in two clades, with inter-clade mash distances of $~15%$. A large fraction of sequence is core, with interspersed diversity.

#figure(image("assets/n2/demerecviridae_markadamsvirinae/bandage.png", width: 50%), 
  caption: "Demerecviridae Markadamsvirinae pangenome graph, visualized using bandage."
)

#figure(image("assets/n2/demerecviridae_markadamsvirinae/mash_dist.png", width: 80%), 
  caption: "core-genome tree and mash distance matrix for Demerecviridae Markadamsvirinae."
)

#figure(image("assets/n2/demerecviridae_markadamsvirinae/mosaic.png", width: 100%), 
  caption: "linear representation for the Demerecviridae Markadamsvirinae pangenome graph."
)

== Autographiviridae

No common core genome can be found for these genomes, within the sensitivity of pangraph.

#figure(image("assets/n2/autographiviridae/mash_dist_simple.png", width: 70%), 
  caption: "mash distance matrix for Autographiviridae."
)

== Siphoviridae Dhillonvirus

Genomes in this category show a large core-genome backbone, small sequence divergence (< 10% mash distance) and a small accessory genome.

#figure(image("assets/n2/siphoviridae_dhillonvirus/bandage.png", width: 50%), 
  caption: "Siphoviridae Dhillonvirus pangenome graph, visualized using bandage."
)

#figure(image("assets/n2/siphoviridae_dhillonvirus/mash_dist.png", width: 80%), 
  caption: "core-genome tree and mash distance matrix for Siphoviridae Dhillonvirus."
)

#figure(image("assets/n2/siphoviridae_dhillonvirus/mosaic.png", width: 100%), 
  caption: "linear representation for the Siphoviridae Dhillonvirus pangenome graph."
)

== Schitoviridae

No common core genome can be found for these genomes, within the sensitivity of pangraph. Isolates are divided in multiple clades, with across-clade mash distances up to $~50%$.

#figure(image("assets/n2/schitoviridae/mash_dist_simple.png", width: 70%), 
  caption: "mash distance matrix for Schitoviridae."
)

== Siphoviridae Queuovirinae Seuratvirus

These genomes have a large core backbone, with limited mash divergence (up to 7%). However, they have differences in accessory genome, with genomes having differences in length of 10 kbps or more.

#figure(image("assets/n2/siphoviridae_queuovirinae_seuratvirus/bandage.png", width: 50%), 
  caption: "Siphoviridae Queuovirinae Seuratvirus pangenome graph, visualized using bandage."
)

#figure(image("assets/n2/siphoviridae_queuovirinae_seuratvirus/mash_dist.png", width: 80%), 
  caption: "core-genome tree and mash distance matrix for Siphoviridae Queuovirinae Seuratvirus."
)

#figure(image("assets/n2/siphoviridae_queuovirinae_seuratvirus/mosaic.png", width: 100%), 
  caption: "linear representation for the Siphoviridae Queuovirinae Seuratvirus pangenome graph."
)

== Myoviridae Ounavirinae

A single isolate from this category has a high divergence from the rest, preventing the definition of a core backbone.

#figure(image("assets/n2/myoviridae_ounavirinae/mash_dist_simple.png", width: 70%), 
  caption: "mash distance matrix for Myoviridae Ounavirinae."
)

== Siphoviridae Queuovirinae Sonagvirus

These genomes have a large core backbone, with limited mash divergence (up to 6%).

#figure(image("assets/n2/siphoviridae_queuovirinae_sonagvirus/bandage.png", width: 50%), 
  caption: "Siphoviridae Queuovirinae Sonagvirus pangenome graph, visualized using bandage."
)

#figure(image("assets/n2/siphoviridae_queuovirinae_sonagvirus/mash_dist.png", width: 80%), 
  caption: "core-genome tree and mash distance matrix for Siphoviridae Queuovirinae Sonagvirus."
)

#figure(image("assets/n2/siphoviridae_queuovirinae_sonagvirus/mosaic.png", width: 100%), 
  caption: "linear representation for the Siphoviridae Queuovirinae Sonagvirus pangenome graph."
)


#bibliography("references.bib")