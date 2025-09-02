### Introduction

This is a repo that contains scripts for the copy number variation project.
The goal is the following: to check if tumor suppressor have an increased copy number in the genomes of different species, particularly those with cancer resistance. The motivation for this study has come from [this paper](https://elifesciences.org/articles/11994) where the authors have reported that elephants have an increased copy number of P53 - the guardian of the genome.

Here, we investigate if the same is true for PTEN - another vital tumor suppressor gene.

Briefly, we extract the TOGA-annotated sequences of P53 and PTEN from TOGA annotations for different species. We also download the genomes of 120 placental mammals and then query the protein sequences using BLAT against the corresponding genome. The query is the protein sequence.

We use P53 as a positive control here. If the pipeline works as expected, we should see several P53 hits from the elephant genome.

### Dependencies

1. The most important tool that we need here is the BLAT binary/executable that is available from UCSC tools for download. The BLAT binary is available [here](https://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/blat/)

Download the blat tool, make it executable i.e
```
chmod +x
``` 

and move this to a directory that is in your PATH.


2. A python library that is needed is Biopython - which can be installed using pip.
More specifically, do the following in your terminal

```
pip3.11 install biopython --user
```

#### TODO:
1. Add a graphic showing the workflow.  
2. Add links to the twoBit/fasta files.   