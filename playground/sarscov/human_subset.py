# %%
import pandas as pd
import numpy as np

df = pd.read_csv(
    "human_seqs.csv",
    parse_dates=["Collection_Date"],
)

cols = [
    "Accession",
    "Organism_Name",
    # "Submitters",
    # "Organization",
    # "Org_location",
    # "Release_Date",
    "Pangolin",
    # "PangoVersions",
    # "Random_Sampling",
    # "Isolate",
    # "Species",
    "Length",
    # "Nuc_Completeness",
    # "Geo_Location",
    "Country",
    # "USA",
    "Host",
    # "Isolation_Source",
    "Collection_Date",
]
# %%


# only keep rows with Host and Collection Date information
sdf = df[cols]
sdf = sdf[~sdf["Host"].isna()]
sdf = sdf[~sdf["Collection_Date"].isna()].copy()

# reshuflle but set seed
np.random.seed(42)
sdf = sdf.sample(frac=1)

# only select already present lineages
lineages = pd.read_csv("../../config/sarscov2_nonhuman.csv")["Pangolin"].unique()
mask = sdf["Pangolin"].isin(lineages)
sdf = sdf[mask]

# select one item per host / pango lineage
dset = sdf.groupby(["Host", "Pangolin"]).first()


dset.to_csv("sarscov2_human.csv")

# %%
