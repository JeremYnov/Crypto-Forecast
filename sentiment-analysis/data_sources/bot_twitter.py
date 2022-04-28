import csv
import os
from tweepy.errors import TweepyException
from tweepy import OAuthHandler, Cursor, API
import pandas as pd
import re
import time 


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root


class BotTwitter:
    def __init__(
        self,
        search_term,
        path_to_login=os.path.join(ROOT_DIR, "credentials", "twitter_login.csv"),
        language="en",
    ):
        self.search_term = search_term
        self.path_to_login = path_to_login
        self.language = language

    # Get tokens
    def getTokens(self):
        credentials = []
        with open(self.path_to_login, "r") as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                credentials.append(row)
        # Don't return headers
        return credentials[1]

    def authentication(self):
        tokens = self.getTokens()
        try:
            self.auth = OAuthHandler(
                consumer_key=tokens[0],
                consumer_secret=tokens[1],
                access_token=tokens[2],
                access_token_secret=tokens[3],
            )
            self.api = API(self.auth, wait_on_rate_limit=True)
        except:
            print("Error : Authentication failed")

    def getTweets(self):
        self.authentication()
        tweets = []
        try:
            for tweet in Cursor(
                self.api.search_tweets,
                q=self.search_term,
                lang=self.language,
                tweet_mode="extended",
            ).items(10):
                tweets.append(
                    {
                    'Text':tweet.full_text,
                    'Created_at':tweet.created_at.strftime("%d-%b-%Y")
                    }
                    )
        except TweepyException as e:
            print("Error : " + str(e))
        print(tweets)
        if tweets:
            self.df = pd.DataFrame(tweets)
            self.cleanTweets()
            print(f"tweets after be cleaned = {self.df}")
            return self.df
        else:
            print("Error : Tweets recovery failed. Retry")

    def cleanTweets(self):
        for _, row in self.df.iterrows():
            row["Text"] = re.sub("http\S+", "", row["Text"])
            row["Text"] = re.sub("#\S+", "", row["Text"])
            row["Text"] = re.sub("@\S+", "", row["Text"])
            row["Text"] = re.sub("\\n", "", row["Text"])
            row["Text"] = re.sub("RT", "", row["Text"])
            row["Text"] = re.sub(" +", " ", row["Text"])
            row["Text"] = re.sub(r"[^\x00-\x7F]+", " ", row["Text"])
            row["Text"] = row["Text"].lstrip()