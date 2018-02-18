from flask import Flask,json,jsonify,request
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from flask_tweepy import Tweepy
#from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_pymongo import PyMongo
import json
#from mongokit import Connection, Document
from pymongo import MongoClient
import csv
from dateutil.parser import *

app=Flask(__name__)


client = MongoClient()
db = client.tweet_db1
tweet_collection = db.tweet_collection
app.config['Mongo_DB_Name']= 'tweet_db1'
t1=db.t1

#mongo=PyMongo(app)
#json=FlaskJSON(app)
CONSUMER_KEY      = "jT7ygfi2QveQVUrE4KKExo8T3" 
CONSUMER_SECRET   = "0tG1mJZwEMVtYdV6qKBMN7MWHWwIZAyLMTUj4OgMOFrBQcvAwG" 
ACCESS_TOKEN_KEY      = "3540331633-nJ7THtWAs8aViG54b3FSk7ko4TDCBgrTOHseawi" 
ACCESS_TOKEN_SECRET= "HixobJ8UlrMHt4Wlgrtbx8BuSG1nSOp0GJdXoQid5QnBu"
auth = tweepy.OAuthHandler('CONSUMER_KEY', 'CONSUMER_SECRET')
auth.set_access_token('ACCESS_TOKEN_KEY','ACCESS_TOKEN_SECRET')
api = tweepy.API(auth)
    
class MyStreamListener(StreamListener): 
    def on_status(self, status):
        try:
             tweet_collection.insert(status._json)
             #t1.insert(status._json)
        except:
             pass
  
    def on_error(self, status_code):
        if status_code == 420:
             return False
            
@app.route('/tweet_stream/<name>',methods=['GET'])                                                             #1
def display_streaming_tweets(name):
   
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track=[name],async=True)
    tweet_cursor = tweet_collection.find()

    res=[]
    for document in tweet_cursor:
        eDict ={
                    "id":document["id"],
                    "name":document["user"]["name"],
                    "Date_Time":document["created_at"],
                    "tweet":document["text"],
                    "followers_count":document["user"]["followers_count"],
                    "screen_name":document["user"]["screen_name"],
                    "favourites_count":document["user"]["favourites_count"]
                  }
        res.append(eDict)
        
    
    return jsonify(result=res)
   

@app.route('/stored_tweets/<tweet>/<date1>/<date2>/uname',methods=['GETS'])                #'''enter in format 2017-04-20T10:37:46.569Z '''#2 &3
def return_tweets(tweet,date1,date2):
    
    cursor=db.tweet_collection.find({"text": "tweet",
                                     date.util["created_at"]: {'$gte': ISODate("date1"),
                                                               '$lt': ISODate("date2"), },
                                     "user":{"name": "uname"}
                                    })
    csvFile = open('result.csv', 'a')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["id","name","Date_of_creation"])
    res=[]
    for document in cursor:
        eDict ={
                    "id":document["id"],
                    "name":document["user"]["name"],
                    "Date_Time":document["created_at"],
                    "tweet":document["text"],
                    "followers_count":document["user"]["followers_count"],
                    "screen_name":document["user"]["screen_name"],
                    "favourites_count":document["user"]["favourites_count"]
                  }
        csvWriter.writerow([document["id"], document["user"]["name"],document["created_at"]])
        res.append(eDict)
        
    csvFile.close()      
    return jsonify(result=res)
        #csvFile.close()         
    

if __name__== "__main__":
    app.run(debug=True)
      
