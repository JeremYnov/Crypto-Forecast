from data_sources.bot_twitter import BotTwitter
from data_sources.cryptopanic import Cryptopanic
from sentiment_analysis.nltk_classification import NLTKClassifier
import pandas as pd
from nltk.corpus import stopwords

if __name__ == "__main__":
    classifier = NLTKClassifier()
    twitter_bot = BotTwitter('bitcoin')
    cryptopanic = Cryptopanic()
        
    tweets_df = twitter_bot.getTweets()
    cryptopanic_df = cryptopanic.getData()
    
    text_to_analyze = pd.concat([cryptopanic_df, tweets_df])
    predictions = []
    trained_model = classifier.train_model()
    wordcloud_text = ''
    for index, row in text_to_analyze.iterrows(): 
        prediction = classifier.predict(text = row["Text"],train_model=trained_model)
        predictions.append(prediction)
        wordcloud_text = wordcloud_text + row['Text']
        
    text_to_analyze['Sentiment'] = predictions
    print(text_to_analyze)
    
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    import numpy as np
    from PIL import Image
   
   
stop_words = stopwords.words('english') 
wordcloud = WordCloud(background_color = 'white', stopwords = stop_words, max_words = 50).generate(' '.join(text_to_analyze ['Text']))
plt.imshow(wordcloud)
plt.axis("off")
plt.show();