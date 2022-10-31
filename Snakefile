configfile: "config/config.yml"


import pandas as pd

df_acc = pd.read_csv(config["accession"])
acc_list = df_acc["genbank_accession"].to_list()
species_to_acc = df_acc.groupby("species")["genbank_accession"].apply(list).to_dict()
species = config["species"]


wildcard_constraints:
    species=f"({'|'.join(species)})",


include: "rules/download.smk"
include: "rules/genomes_comparison.smk"
include: "rules/pangraph.smk"
