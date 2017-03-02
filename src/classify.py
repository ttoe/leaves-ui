import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# reading the precomputed data, that was saved as csv
data = pd.read_csv("../out/leaf_morphometrics_4beeeb7.csv", sep=";", decimal=",")

# selected species for which the assignment will be done
species = [ "abies_concolor", "acer_palmatum", "acer_saccharinum", "aesculus_glabra"
          , "amelanchier_arborea", "betula_populifolia", "juglans_nigra"
          , "metasequoia_glyptostroboides", "robinia_pseudo-acacia", "zelkova_serrata"]

# extracting the rows specified by 'species'
selected_species = data.loc[data["species"].isin(species)]

# calculating the medians of the morphometric descriptors per species
selected_species_medians = selected_species.groupby("species").median()

# selecting the data of the first single leaf of the species
# those will be used to try and match them to their species 
unknown_species = selected_species.groupby("species").first()

# some data munging to satisfy pandas for later
unknown_species["species"] = unknown_species.index

# calculates the euclidian distance in 4d between the points given by
# the median values for each species' descriptors and the 
# values of the descriptors of a single leaf
# add_dist_column :: DataFrame -> DataFrame -> DataFrame
def add_dist_columns(unknown_species_df, species_centerpoints_df):
    uk = unknown_species_df.copy()
    gms = species_centerpoints_df.copy()
    
    for row in uk.iterrows():
        s = row[1] # get df object out of tuple
        gms[s.species] = np.sqrt( (gms.eccentricity-s.eccentricity)**2 
                                + (gms.extent-s.extent)**2 
                                + (gms.solidity-s.solidity)**2
                                + (gms.roundness-s.roundness)**2 ) / 2 # normalize to 1 (max is otherwise 2)
    return gms.iloc[:,4:]
    

# compute the result dataframe using the function defined above
res = add_dist_columns(unknown_species, selected_species_medians)

# round numbers for plotting
data = res.round(2)

# set aesthetics
sns.set()
sns.set_context("paper")
plt.figure(figsize=(8, 6))

# plot heatmap
ax = sns.heatmap(data.T, annot=True)

# turn the axis label
for item in ax.get_yticklabels():
    item.set_rotation(0)

for item in ax.get_xticklabels():
    item.set_rotation(90)

# save figure
plt.savefig("../out/distances_heat.pdf", bbox_inches='tight')
