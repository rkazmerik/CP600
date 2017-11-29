from datetime import datetime
from elasticsearch import Elasticsearch
import json

### Return an array of tweets #######################################
def getDataset(indexName, noItems):
  es = Elasticsearch()
  results = []

  tweets = es.search(
      index=indexName,
      size=noItems,
      _source_include="message",
      body={
          "query": {
            "match_all": {}
          }
      }
  )

  for hit in tweets['hits']['hits']:
      source = hit["_source"]
      results.append(source["message"])

  return results

### Split the main trump index into two smaller indexes ##############
def splitDataset():
  es = Elasticsearch()

  #Delete the data set indexes before loading them
  es.indices.delete(index='140set', ignore=[400, 404])
  es.indices.delete(index='280set', ignore=[400, 404])

  #Find all the tweets from the trump index
  authors = es.search(
      index="trump",
      size=10000,
      _source_include="user",
      body={
          "query": {
            "match_all": {}
          }
      }
  )

  #Iterate through the authors of the tweets
  clicker = 0
  for hit in authors['hits']['hits']:
      source = hit["_source"]
      author = source["user"]

      #Find 2 tweets by the same author
      tweets = es.search(
          index="trump",
          size=2,
          body={
              "query": {
                  "term": {
                      "user": author
                  }
              }
          }
      )

      count = tweets['hits']['total']
      if count >= 2:
        
        #Create two different tweets
        t1 = tweets['hits']['hits'][0]
        t2 = tweets['hits']['hits'][1]

        #Insert tweet 1 into the 140set index
        op1 = es.create(
          id=t1['_id']+str(datetime.now()),
          index="140set",
          doc_type="doc",
          body={ 
            'author': t1['_source']['user'], 
            'message': t1['_source']['message']
          },
          ignore=[403]
        )

        #Insert tweet 2 (including the message of t1) into the 280set index
        op2 = es.create(
          id=t2['_id']+str(datetime.now()),
          index="280set",
          doc_type="doc",
          body={ 
            'author': t2['_source']['user'], 
            'message': t1['_source']['message']+' '+t2['_source']['message']
          },
          ignore=[403]
        )

        #Every 100 tweets generated, print a message
        clicker+=1
        if (clicker % 100) == 0:
          print("Generating tweet sets...")