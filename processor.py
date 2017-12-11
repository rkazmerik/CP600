#from sklearn.datasets import fetch_20newsgroups
from __future__ import print_function
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import metrics
import loader

### Get the tweet data sets from Elastic Search ######################
tweetSet1 = loader.getDataset("140set", 1000000)
tweetSet2 = loader.getDataset("280set", 1000000)

print("Tweet set 1 total: " + str(len(tweetSet1)))
print("Tweet set 2 total: " + str(len(tweetSet2)))
print()


### Load the datasets into the TF-IDF vectorizer #####################
noFeatures = 100
print("No. Features: " + str(noFeatures))

vectorizer = TfidfVectorizer(max_df=0.5, max_features=noFeatures,
  min_df=2, stop_words='english', use_idf="true")

t1 = vectorizer.fit_transform(tweetSet1)
idf1 = vectorizer.idf_

t2 = vectorizer.fit_transform(tweetSet2)
idf2 = vectorizer.idf_


### Run the kMeans clustering ######################################
noClusters=6
print("No. Clusters: " + str(noClusters))

km = KMeans(n_clusters=noClusters, init='k-means++', max_iter=50, n_init=1)

km.fit(t1)
print()
print("140set RESULTS: ")
print("Intertia = " + str(km.inertia_))
print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(t1, km.labels_, sample_size=1000))
print("Calinski-Harabaz Index: %0.3f" % metrics.calinski_harabaz_score(t1.toarray(), km.labels_))

km.fit(t2)
print()
print("280set RESULTS: ")
print("Intertia = " + str(km.inertia_))
print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(t2, km.labels_, sample_size=1000))
print("Calinski-Harabaz Index: %0.3f" % metrics.calinski_harabaz_score(t2.toarray(), km.labels_))

print()