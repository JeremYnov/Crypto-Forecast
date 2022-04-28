from sentiment_analysis.tf_rnn_classification import RNNClassifier
from data_sources.bot_twitter import BotTwitter
import pandas as pd
from os import path
import tensorflow as tf 

if __name__ == "__main__":
    classifier = RNNClassifier()
    twitter_bot = BotTwitter('bitcoin')
    
    if not path.exists("trained_model/rnn_trained_model"):
        classifier.define_model()
        
    tweets_df = twitter_bot.getTweets()
    # defined_model = classifier.define_model()
    # classifier.two_layers_model_prediction('This is my best test text')
    predictions = []
    for index, row in tweets_df.iterrows(): 
        prediction = classifier.two_layers_model_prediction(row["Text"])
        predictions.append(prediction[0][0])
        
    print(predictions)
        # print(row["Text"])
    # tweets_df['sentiment_analysis'] = tweets_df.apply(classifier.two_layers_model_prediction(tweets_df['Text']))
    
    # print(tweets_df)