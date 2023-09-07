# %%
import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt

df = pd.read_csv("../../results/flu/mash_dist.csv")
D = df.pivot(index="strain_1", columns="strain_2", values="mash_dist")
# %%

# find order using hierarchical clustering
dist = sch.distance.pdist(D)
linkage = sch.linkage(dist, method="complete")
order = sch.leaves_list(linkage)
strains = D.index.to_numpy()
str_order = strains[order]

D = D.loc[str_order, str_order]
plt.matshow(D)
plt.show()

# %%

beg, end = 1, 31
plt.matshow(D.iloc[beg:end, beg:end])
plt.show()

selected_str = str_order[beg:end]

str_df = pd.read_csv("../../config/flu_dataset.csv")
str_df["selected"] = str_df["acc"].isin(selected_str)
str_df.to_csv("flu_dataset_selected.csv")
# %%
