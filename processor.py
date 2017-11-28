

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

str = "The problem is that this returns a matrix with n rows where n is the size of my doc string. I want it to return just a single vector representing the tf-idf for the entire string. How can I make this see the string as a single document, rather than each character being a document? Also, I am very new to text mining so if I am doing something wrong conceptually, that would be great to know. Any help is appreciated.".split()

dataset = fetch_20newsgroups(subset='test', categories=['comp.graphics'])

print(dataset)

#vectorizer = TfidfVectorizer(max_df=0.5, max_features=50,
#                               min_df=2, stop_words='english',
#                               use_idf="true")

#X = vectorizer.fit_transform(str)

#idf = vectorizer.idf_

#print dict(zip(vectorizer.get_feature_names(), idf))

# km = KMeans(n_clusters=4, init='k-means++', max_iter=100, n_init=1)
# km.fit(X)


# print(km)
