# %%
import pandas as pd
import numpy as np
import re

with open("results.txt", "r") as f:
    entries = []
    entry = []
    for l in f.readlines():
        if l == "\n":
            if len(entry) > 0:
                entries.append(entry)
            entry = []
        else:
            entry.append(l.strip())
    if len(entry) > 0:
        entries.append(entry)

# %%
df = []
for entry in entries:
    l1, l2, l3 = entry
    res = {}
    acc, GI = l3.split(" ")
    # accession number and index
    res["acc"] = acc
    # res["GI"] = GI.split(":")[1]
    res["idx"] = int(l1.split(" ")[0].rstrip("."))

    # length
    L = re.search(r"([\,\d]+) bp", l2).group(1)
    res["L"] = int(L.replace(",", ""))

    # name
    if l1.endswith("segment 4 hemagglutinin (HA) gene, complete cds"):
        l1 = l1.removesuffix("segment 4 hemagglutinin (HA) gene, complete cds")
    info = re.search("\((.+)\)", l1)
    if info is None:
        continue
    info = info.group(1)

    LI = len(info.split("/"))
    if LI == 5:
        rx = r"^(([^/]+)/([^/]+)/([^/]+)/([^/]+)/(\d+)).?\(([^)]+)\)$"
        sc = re.search(rx, info)
        if sc is None:
            continue
        _, tp, ht, ct, cld, yr, st = sc.groups()
        ht = ht.lower()
    elif LI == 4:
        rx = r"^(([^/]+)/([^/]+)/([^/]+)/(\d+)).?\(([^)]+)\)$"
        sc = re.search(rx, info)
        if sc is None:
            continue
        _, tp, ct, cld, yr, st = sc.groups()
        ht = None
    else:
        print(info)
        continue
        break

    st = st.upper()
    if ("?" in st) or ("X" in st) or ("N" not in st):
        continue

    res["flu type"] = tp
    res["host"] = ht
    res["location"] = ct.lower()
    res["clade"] = cld
    res["year"] = int(yr)
    res["strain"] = st
    res["flu"] = re.search("Influenza ([^ ]+) [vV]irus", l1).group(1)

    df.append(res)
df = pd.DataFrame(df)
df.set_index("idx", inplace=True)
df
# %%
print(df["host"].value_counts().reset_index().to_markdown())
# %%
print(df["flu"].value_counts().to_markdown())
# %%
N_top_hosts = 8
top_hosts = df["host"].value_counts().head(N_top_hosts)
print(top_hosts)
top_hosts = top_hosts.index

# %%

# select strains from top isolates
# np.random.seed(0)
# N_host = 10
# selected_ids = []
# for h in top_hosts:
#     sdf = df[df["host"] == h]
#     l = len(sdf)
#     order = list(range(l))
#     np.random.shuffle(order)
#     print(h)
#     selected_str = []
#     n_sel = 0
#     for i in order:
#         if n_sel == N_host:
#             break
#         row = sdf.iloc[i]
#         idx = sdf.index[i]
#         if row["strain"] in selected_str:
#             continue
#         selected_ids.append(idx)
#         selected_str.append(row["strain"])
#         n_sel += 1
# df.loc[selected_ids]

np.random.seed(0)
N_host = 5
STR = "H1N1"
selected_ids = []
for h in top_hosts:
    sdf = df[df["host"] == h]
    l = len(sdf)
    order = list(range(l))
    np.random.shuffle(order)
    print(h)
    n_sel = 0
    for i in order:
        if n_sel == N_host:
            break
        row = sdf.iloc[i]
        idx = sdf.index[i]
        if row["strain"] != STR:
            continue
        selected_ids.append(idx)
        n_sel += 1
df.loc[selected_ids]
# %%
sdf = df.loc[selected_ids].set_index("acc").drop(columns=["flu type"])
sdf.to_csv("flu_dataset.csv")

# %%
