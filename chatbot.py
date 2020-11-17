import pandas as pd
import nltk
import re
from nltk.stem import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk import pos_tag
from nltk import word_tokenize
from datetime import datetime

print("Time now: "+str(datetime.now()))
hvect = HashingVectorizer(input= "content", ngram_range=(1, 2))
data = pd.read_csv('traindata.csv', encoding='utf-8')
print("Train data loaded...")
print("Time now: "+str(datetime.now()))

def text_normalize(text):
    text = str(text).lower()
    spl_char_text = re.sub(r'[^ a-z]', '', text)
    tokens = nltk.word_tokenize(spl_char_text)
    lema = wordnet.WordNetLemmatizer()
    tags_list = pos_tag(tokens, tagset=None)
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

def chat(text):
    lemma = text_normalize(text)
    hvec = hvect.fit_transform([lemma])
    tf = TfidfTransformer(use_idf=True).fit(hvec)
    tf_chat = tf.transform(hvec)
    cos = cosine_similarity(tf_chat, x_tf)
    index = cos.argmax()
    if index != 0:
        return(data.iloc[index]["Replies"])
    else:
        return "Sorry, I don't know what to say."

if __name__ == '__main__':
    print("----------------------------------------------------------------------------------------------------------")
    print("Time now: "+str(datetime.now()))
    print(data.info())
    print("Time now: "+str(datetime.now()))
    print(type(data['lemmatized text']))
    print("----------------------------------------------------------------------------------------------------------")
    print("Loading Model..., Time now: "+str(datetime.now()))
    hashv = hvect.fit_transform(data['lemmatized text'].values.astype('U'))
    tfdif = TfidfTransformer(use_idf=True).fit(hashv)
    x_tf = tfdif.transform(hashv)
    df_tfdif = pd.DataFrame(x_tf, columns=hvect.get_stop_words())
    print(df_tfdif)
    print("Model Loaded..., Time now: "+str(datetime.now()))
    print("----------------------------------------------------------------------------------------------------------")
    exit_commands = ("quit", "pause", "exit",
                     "goodbye", "bye", "later", "stop")
    user = input("\nEnter Your Name: ")
    botname = "Watson"
    print("Hey "+user+"! I'm "+botname+", a chatbot trained on random data!\n")
    while True:
        request = input(user+': ')
        if request.lower() in exit_commands:
            print(botname, ': Bye, Have a nice day!')
            break
        elif request.lower().endswith("your name") or request.lower().endswith("your name?"):
            print(botname, ": I've already told you it's " + botname + ".\n")
        elif request.lower().endswith("the time now?") or request.lower().endswith("the time?") or request.lower().endswith("the time"):
            print(botname, ": It's " + str(datetime.now()) + ".\n")
        else:
            response = chat(request)
            response = response.replace('newlinechar', '\n').replace('2015','2020')
            print(botname, ':', response, "\n")
