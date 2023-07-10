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

= Dataset Preparation

I downloaded accession for phages from the _Basel collection_ @maffei2021systematic. This include both phages isolated from the Rhine river, and other related phages from NCBI, for a total of 284 genomes. They divided in 10 different categories:


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
+ estimate diversity with mash
+ generate a pangenome graph using _pangraph_ with minimap2 kernel and options `-s 20 -a 20 -b 5`.
+ if core geneome is present, generate a core genome tree using `fasttree`.

= Todo

- compare trees with paper. Mash distance vs core genome distance. The rest comes from diversity in DNA.
- tree vs infected bacterium?
- mosaic plot with blocks. Do a script.
- pangraph pictures and trees
- rearrangements

#bibliography("references.bib")