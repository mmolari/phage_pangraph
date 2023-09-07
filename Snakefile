configfile: "config/config.yml"


import pandas as pd

df_acc = pd.read_csv(config["accession"])
acc_list = df_acc["genbank_accession"].to_list()
species_to_acc = df_acc.groupby("species")["genbank_accession"].apply(list).to_dict()
species_to_acc["basel"] = df_acc[df_acc["basel_collection"]][
    "genbank_accession"
].to_list()
species = config["species"]

# accession numbers of coronaviridae
df_covid = pd.read_csv(config["accession-covid"])
cov_accnums = df_covid["acc"].to_list()
cov_genus_acc = df_covid.groupby("genus")["acc"].apply(list).to_dict()
cov_genus_acc["all"] = cov_accnums

# accession numbers of non-human sarscov2
df_scov = pd.read_csv(config["accession-sarscov"])
scov_accnums = df_scov["Accession"].to_list()

# accession numbers of flu
df_flu = pd.read_csv(config["accession-flu"])
flu_accnums = df_flu["acc"].to_list()


wildcard_constraints:
    species=f"({'|'.join(species)})",


include: "rules/download.smk"
include: "rules/pangraph.smk"
include: "rules/coronaviridae.smk"
include: "rules/sarscov2.smk"
include: "rules/flu.smk"
