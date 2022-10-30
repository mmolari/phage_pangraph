configfile: "config/config.yml"


import pandas as pd

df_acc = pd.read_csv(config["accession"])
acc_list = df_acc["genbank_accession"].to_list()


include: "rules/download.smk"
include: "rules/genomes_comparison.smk"
