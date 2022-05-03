import re
import string
import random
from nltk import FreqDist, classify, NaiveBayesClassifier, download
from nltk.corpus import twitter_samples, stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

download('twitter_samples')
download('stopwords')
download('averaged_perceptron_tagger')
download('wordnet')
download('omw-1.4')
download('punkt')


class NLTKClassifier: 
    def __init__(self) -> None:
        pass
    
    def remove_noise(self,tweet_tokens, stop_words = ()):
        cleaned_tokens = []

        for token, tag in pos_tag(tweet_tokens):
            token = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
                    ,"", token)
            token = re.sub("(@[A-Za-z0-9_]+)","", token)

            if tag.startswith("NN"):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'

            lemmatizer = WordNetLemmatizer()
            token = lemmatizer.lemmatize(token, pos)

            if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
                cleaned_tokens.append(token.lower())
        return cleaned_tokens

    def get_all_words(self,cleaned_tokens_list):
        for tokens in cleaned_tokens_list:
            for token in tokens:
                yield token

    def get_tweets_for_model(self,cleaned_tokens_list):
        for tweet_tokens in cleaned_tokens_list:
            yield dict([token, True] for token in tweet_tokens)
            
    def load_data(self):
        stop_words = stopwords.words('english')

        positive_cleaned_tokens_list = []
        for tokens in twitter_samples.tokenized('positive_tweets.json'):
            positive_cleaned_tokens_list.append(self.remove_noise(tokens, stop_words))
        positive_dataset = [(tweet_dict, "Positive") for tweet_dict in self.get_tweets_for_model(positive_cleaned_tokens_list)]

        negative_cleaned_tokens_list = []
        for tokens in twitter_samples.tokenized('negative_tweets.json'):
            negative_cleaned_tokens_list.append(self.remove_noise(tokens, stop_words))
        negative_dataset = [(tweet_dict, "Negative") for tweet_dict in self.get_tweets_for_model(negative_cleaned_tokens_list)]

        return positive_dataset + negative_dataset
    
    def train_model(self):
        dataset = self.load_data()
        random.shuffle(dataset)
        train_data = dataset[:7000]
        test_data = dataset[7000:]
        classifier = NaiveBayesClassifier.train(train_data)
        print("Accuracy is:", classify.accuracy(classifier, test_data))
        return classifier
        
    def predict(self, text, train_model):
        return train_model.classify(
            dict([token, True] for token in self.remove_noise(word_tokenize(text)))
        )
        
        