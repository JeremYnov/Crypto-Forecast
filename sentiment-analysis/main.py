import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud
from nltk.corpus import stopwords

from data_sources.bot_twitter import BotTwitter
from data_sources.cryptopanic import Cryptopanic
from sentiment_analysis.nltk_classification import NLTKClassifier


if __name__ == "__main__":
    classifier = NLTKClassifier()        
    tweets_df = BotTwitter('bitcoin').getTweets()
    cryptopanic_df = Cryptopanic().getData()
    
    text_to_analyze = pd.concat([cryptopanic_df, tweets_df])
    predictions = []
    wordcloud_text = ''
    for index, row in text_to_analyze.iterrows(): 
        predictions.append(
            classifier.predict(text = row["Text"],train_model=classifier.train_model())
        )
        wordcloud_text = wordcloud_text + row['Text']
        
    text_to_analyze['Sentiment'] = predictions
    print(text_to_analyze)

    plt.imshow(
        WordCloud(background_color = 'white', stopwords = stopwords.words('english') , max_words = 50).generate(' '.join(text_to_analyze ['Text']))
    )
    plt.axis("off")
    plt.show()