from tweepy import Stream
from tweepy import OAuthHandler                      # No need to PIP THIS!!!!!!!!!!!!!!!
from tweepy.streaming import StreamListener
import MySQLdb
import time
import json
import main as m   # The function sentiment() in main.py returns sentiment_value and confidence

#Database config to save different users inputs/requests
                        #server,    MySQL username, mysql pwd, Database_name
conn = MySQLdb.connect("localhost", "useraccount", "saf_proj", "twitterfeedDB")
c = conn.cursor()


#consumer key, consumer secret, access token, access secret
#Authentication and authorisation to the public API

ckey = "UcRP1JNvVEk5AFQJ3kdc5u4BH"
csecret = "vkaFXRo0a4lIhxHP3FVpVZfrV0Ljk9UEwp9wBQW5Xzuo6bMgj7"
atoken = "745559408101433344-Pc8NDKQFyZx6I5CY8SGu3240h4QXbxY"
asecret = "42mQp7RDMsH4F5Ou4QaBmO8LKGRX5s74FUID1bkAgUCTj"

class listener(StreamListener):
    def on_data(self,data):
        try:
            all_data = json.loads(data)
            tweet = all_data["text"]
            username = all_data["user"]["screen_name"]
            c.execute("INSERT INTO Users_Table (time,username,tweet) VALUES (%S,%S,%S)",
                      (time.time(),username,tweet))
            conn.commit()
            print((username,tweet))
            #print((tweet))

            sentiment_value, confidence = m.sentiment(tweet)
            print (tweet, sentiment_value,confidence)

            if confidence*100 >= 70:              #This is aggregate/overall confidence level as reported by classifiers used
                output = open("twitter_results_to_plot.txt", "a")      #The confidence level above is saved in a text file
                output.write(sentiment_value)
                output.write('\n')
                output.close()

            return True
        except:
            return True

    def on_error(self, status):
        print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["safaricom blaze"])   #"key word" or "search topic"




