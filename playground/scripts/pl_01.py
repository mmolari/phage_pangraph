# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering


def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

# %%
mash_dist = "../../results/covid/mash_dist.csv"
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
model = AgglomerativeClustering(distance_threshold=0., n_clusters=None, linkage="complete")

model = model.fit(1-dist)
plt.title("Hierarchical Clustering Dendrogram")
# plot the top three levels of the dendrogram
plot_dendrogram(model, truncate_mode="level", p=3)
plt.xlabel("Number of points in node (or index of point if no parenthesis).")
plt.show()

# %%
order = model.labels_

plt.matshow(dist[order][:,order])
plt.colorbar()
plt.show()
# %%
