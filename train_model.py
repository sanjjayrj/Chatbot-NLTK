import pandas as pd
import nltk
import re
import pickle
from nltk.stem import wordnet
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import pos_tag
from sklearn.metrics import pairwise_distances
from nltk import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime

tfdif = TfidfVectorizer()
data = pd.read_csv('traindata.csv', encoding='utf-8')
train_counter = 0

def text_normalize(text):
    global train_counter
    if train_counter % 10000 == 0:
        print(str(train_counter) + " sets lemmatized..., "+"Time now: " + str(datetime.now()))
    train_counter += 1
    text = str(text).lower()
    spl_char_text = re.sub(r'[^ a-z]', '', text)
    tokens = nltk.word_tokenize(spl_char_text)
    lema = wordnet.WordNetLemmatizer()
    tags_list = pos_tag(tokens, tagset = None)
    lema_words = []
    for token, pos_token in tags_list:
        if pos_token.startswith('V'):
            pos_value = 'v'
        elif pos_token.startswith('J'):
            pos_value = 'a'
        elif pos_token.startswith('R'):
            pos_value = 'r'
        else:
            pos_value = 'n'
        lema_token = lema.lemmatize(token, pos_value)
        lema_words.append(lema_token)
    return " ".join(lema_words)

if __name__ == '__main__':
    print("Time now: " + str(datetime.now()))
    print(data.info())
    print("\nData Imported...")
    print("----------------------------------------------------------------------------------------------------------")
    data['lemmatized text'] = data['Content'].apply(text_normalize)
    print("Training Data Lemmatized..., Time now: " + str(datetime.now()))
    data.to_csv('traindata.csv', encoding='utf-8', index = False)
    print(data['lemmatized text'])
    print(type(data['lemmatized text']))
    print("\nTraining data...")
    print("----------------------------------------------------------------------------------------------------------")