import pandas as pd
import numpy as np
import scipy as sc
from sklearn.cluster import KMeans

### For the purposes of this example, we store feature data from our
### dataframe `df`, in the `f1` and `f2` arrays. We combine this into
### a feature matrix `X` before entering it into the algorithm.

df=pd.read_csv('dataset.csv', sep='\t')

f1 = df['Distance_Feature'].values
f2 = df['Speeding_Feature'].values

matrix = np.matrix(list(zip(f1,f2)))

kmeans = KMeans(n_clusters=4).fit(matrix)

print(kmeans.labels_)
print(kmeans.inertia_)
print(kmeans.cluster_centers_)