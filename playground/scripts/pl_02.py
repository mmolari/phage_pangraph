# %%
from Bio import SeqIO
import re
import pandas as pd
# %%
acc_file = "../../config/covid_acc_nums.txt"
accs = pd.read_csv(acc_file).to_numpy().flatten()
# %%
df = []
for a in accs:
    gbk_file = f"../../raw_data/gbk/{a}.gbk"
    gbk = SeqIO.read(gbk_file, format="genbank")
    org = gbk.annotations["organism"].replace(",", "_")
    tax = gbk.annotations["taxonomy"]
    tax = "/".join(tax)
    cat = re.search(r"Orthocoronavirinae/([^/]+)", tax).group(1)
    print(a, cat, org)

    df.append({
        "acc" : a,
        "genus" : cat,
        "organism" : org
    })

df = pd.DataFrame(df)
# %%
df.sort_values(["genus", "acc"]).to_csv("covid_dataset.csv", index=False)
# %%
