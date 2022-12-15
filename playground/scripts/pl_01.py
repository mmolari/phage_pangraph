# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from scipy.cluster.hierarchy import dendrogram
from scipy.cluster import hierarchy

# %%
mash_dist = "../../results/covid/mash_dist.csv"
# mash_dist = "../../results/mash_triangle/autographiviridae.csv"
df = pd.read_csv(mash_dist)
df = df.pivot(index="strain_1", columns="strain_2", values="mash_dist")
accs = df.columns.to_numpy()
accs.sort()
df = df[accs].loc[accs]
dist = df.to_numpy()
# %%
plt.matshow(dist)
# %%
# setting distance_threshold=0 ensures we compute the full tree.
Z = hierarchy.linkage(dist, method="ward", optimal_ordering=True)
dendrogram(Z, leaf_label_func=lambda k: accs[k])

plt.title("Hierarchical Clustering Dendrogram")
# plot the top three levels of the dendrogram
# plt.xlabel("Number of points in node (or index of point if no parenthesis).")
plt.show()


# %%
order = hierarchy.leaves_list(Z)

plt.matshow(dist[order][:,order])
plt.colorbar()
plt.show()
# %%
