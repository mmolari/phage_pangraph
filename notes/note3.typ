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

== Different sequence types

I searched NCBI nucleotide (7/09/23) for the keyword `influenza segment 4 hemagglutinin complete cds` with `genomic DNA/RNA` constraint and length between 300 and 3000 bp. This gives 141938 results. I download the summary file from NCBI.

I parse this file and extract host and type information. For the 8 prevalent hosts, I select at most random 10 sequences with the constraint that they must all belong to different sequence types. 

```
MW345940.1
OR044145.1
MW186796.1
MW186804.1
LC339531.1
FJ432770.1
LC367498.1
GQ257448.1
EU743167.1
KF424178.1
KF424258.1
MH597471.1
MH597495.1
MH502868.1
MH546347.1
MH341798.1
MH503005.1
MH134849.1
MW132351.1
MK237430.1
MT197120.1
```
```

KY681473.1
KJ195788.1
KX232477.1
MH546987.1
MW811345.1
MW855419.1
MW855413.1
MW855511.1
MH546995.1
MW855538.1
OP433195.1
KP186072.1
KP288100.1
MW240531.1
FJ357104.1
CY025002.1
EU735794.2
```