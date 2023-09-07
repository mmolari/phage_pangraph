#import "template.typ": *

#show: project.with(
  title: "Notes",
  authors: (
    "Marco Molari",
  ),
  abstract: [
    Notes.
  ],
  date: "August 14, 2023",
)

= Notes

- Add human SARS-CoV-2 genomes to the dataset.
- HIV-like, more cross-species examples?
- Flu virus crosses species boundary. How is the diversity in its genome? Are the genes in the same order?

= Influenza workflow

I searched NCBI nucleotide (7/09/23) for the keyword `influenza segment 4 hemagglutinin complete cds` with `genomic DNA/RNA` constraint and length between 300 and 3000 bp. This gives 141938 results. I download the summary file from NCBI.