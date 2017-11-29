#from sklearn.datasets import fetch_20newsgroups
from __future__ import print_function
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import metrics
import json
import loader

### Get the tweet data sets from Elastic Search ######################
tweetSet1 = loader.getDataset("140set", 1800)
tweetSet2 = loader.getDataset("280set", 1800)

print("Tweet set 1 total: " + str(len(tweetSet1)))
print("Tweet set 2 total: " + str(len(tweetSet2)))
print()


### Load the datasets into the TF-IDF vectorizer #####################
vectorizer = TfidfVectorizer(max_df=0.5, max_features=20,
  min_df=2, stop_words='english', use_idf="true")

t1 = vectorizer.fit_transform(tweetSet1)
idf1 = vectorizer.idf_

t2 = vectorizer.fit_transform(tweetSet2)
idf2 = vectorizer.idf_

print("140set Features: ")
print(json.dumps(dict(zip(vectorizer.get_feature_names(), idf1)), indent=4, sort_keys=True))

print("280set Features: ")
print(json.dumps(dict(zip(vectorizer.get_feature_names(), idf2)), indent=4, sort_keys=True))
print()


### Run the kMeans clustering ######################################
noClusters=4
km = KMeans(n_clusters=noClusters, init='k-means++', max_iter=50, n_init=1, verbose=1)

km.fit(t1)
print()
print("140set RESULTS: ")
print("Intertia = " + str(km.inertia_))
print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(t1, km.labels_, sample_size=1000))
print("Calinski-Harabaz Index: %0.3f" % metrics.calinski_harabaz_score(t1.toarray(), km.labels_))
print("Top terms: ")

order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(noClusters):
    print("Cluster %d:" % i, end='')
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind], end='')
    print()

print()

km.fit(t2)
print()
print("280set RESULTS: ")
print("Intertia = " + str(km.inertia_))
print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(t2, km.labels_, sample_size=1000))
print("Calinski-Harabaz Index: %0.3f" % metrics.calinski_harabaz_score(t2.toarray(), km.labels_))
print("Top terms: ")

order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(noClusters):
    print("Cluster %d:" % i, end='')
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind], end='')
    print()
print()