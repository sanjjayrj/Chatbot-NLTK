# **NLTK based Chatbot**
## **Table of Contents**
---
1. **Introduction**
2. **Dataset Description**
3. **Packages Used**
4. **Steps Involved**
5. **Working**
6. **Demo-Screenshot**
---
## Introduction
---
This Chatbot is trained on reddit comments from May,2015. It is a purely conversational chatbot. And since it has been trained on reddit  data the replies can be less formal. It was developed as part of my college project, and can be modified to work with other datasets too.

## Dataset Description
---
Database Torrent Link: [1.7 billion comments](https://www.reddit.com/r/datasets/comments/3bxlg7/i_have_every_publicly_available_reddit_comment/?st=j9udbxta&sh=69e4fee7)
The databaase file is downloadable in .bz2 format(5gb).
The database has one table, May2015, with the following fields:
- created_utc
- ups
- subreddit_id
- link_id
- name
- score_hidden
- authorflaircss_class
- authorflairtext
- subreddit
- id
- removal_reason
- gilded
- downs
- archived
- author
- score
- retrieved_on
- body
- distinguished
- edited
- controversiality
- parent_id

The dataset has a lot of NSFW stuff so to filter those comments, if needed you can include your blacklist words in the vocab_blacklist.txt file. Totally upto you!
## Packages Used
---
> **Pandas<br>
> Numpy<br>
> nltk (word_tokenize, pos_tag)<br>
> nltk.stem (wordnet)<br>
> sklearn.feature_extraction.text(TfidfVectorizer, TfidfTransformer, HashingVectorizer)<br>
> sqlite3<br>
> json<br>
> re<br>**
## **Steps Involved**
---
Download the dataset and extract it, ideally using 7-zip. After extracting the file should be named **"RC_2015-5"**. If not then change the file name in the database extractor file respectively. The whole process of completion might take quite a bit of time.
Order of running files:
* database_extractor.py
* create_trainingdata.py
* fix_trainingdata.py
* prepare_data.py
* train_model.py
* chatbot. py
## **Working**
---
Install all packages before running the files.
1. **database_extractor.py**
You will have to update the location of your database file in this line.
`with open(".......RC_{}".format(timeframe), buffering = 1000) as f:`
Since most of the data will be garbage data, we will pick out comments and replies that have a good score. In this case, I've picked out comments with score > 2.
Using sql commends we check if comment is large or within as specified length by using function acceptable.
`if len(data.split(' ')) > 50 or len(data) < 1`
Then we check if a given comment has another comment with the same parent id that has a higher score, if yes we will replace that comment with a new comment, depending on whether it has a parent comment or not.
This can take hours to run.
2. **create_trainingdata.py**
We have our shorter and updated database we extracted using database extractor. Using sql commands we create two files **train.from and train. to** which essentially has the input comment and reply comment to a query.
We take all comments that has a score above 0(ie it exists) and has a parent comment.
3. **fix_trainingdata.py**
We import the two 'from and to' files. Now we can filter the comments based on it's content. Include words in the **vocab_blacklist.txt** file line-by-line, which should be censored to the bot. I have pre-inserted 'http' & 'https' to get rid of any comment and reply that has a link in it. Using re package we can remove unwanted symbols in the data.
`re.sub(r'[^a-z0-9]', ' ', a)`
Finally the same train.from and train. to files are overwritten with the new data.
4. **prepare_data.py**
Using pandas the data in the files are entered into a dataframe and stored in a csv file.
**Note: Storing values in csv in preffered over xls files, since it's easier to organize large amounts of data.**
The contenst of from file is stored in column **'Content'**, and that of to file is stored in **'Replies'**.
5. **train_model.py**
The csv file containing the comment and reply is read into a DataFrame.
We define a function **text_normalize(text)** and pass individual strings of 'comments' from the dataframe into this function, which returns the lemmatized text back.
`data['lemmatized text'] = data['Content'].apply(text_normalize)`
The text is tokenized using nltk.stem package. And the lemmatizer check if the word is an Adjective, Adjerb, Verb,etc and converts it into it's simplest form word-by-word.
The final lemmatized text is formed and returned back into the dataframe in a new column 'lemmatized text'
6. **chatbot. py**
Traditionally one would use **TfidfVectorizer, Bag of Words** or **CountVectorizer** for text classification, but those methods have proved to be very slow and memory consuming. This is solved using HashVectorizer. A hashing vectorizer is a variation on the count vectorizer that sets out to be faster and more scalable, at the cost of interpretability and hashing collisions. **We perform hashvectorizing on the 'lemmatized text'. The hashing vectorizer gave us counts of the 1- and 2-grams in the text, in other words, singleton and consecutive pairs of words (tokens) in the articles. We then apply a tf-idf transformer to give appropriate weights to the counts that the hashing vectorizer gave us. We end up with a large sparse matrix which contains the occurrences of 1- and 2-grams in the texts, weighted by importance. This method uses mucch lesser memory than CountVectorizer and TfidfVectorizer.**
`hashv = hvect.fit_transform(data['lemmatized text'].values.astype('U'))`
`tfdif = TfidfTransformer(use_idf=True).fit(hashv)`
`x_tf = tfdif.transform(hashv)`
Then input from the user is also lemmatized & hash vectorized. We then find the similarity between the input and each line of 'lemmatized text' by finding the cosine similarity between the 2 sparse matrixes formed.
`cos = cosine_similarity(tf_chat, x_tf)`
And then we can get an index number to find the location of the reply in the dataframe using the argmax() function of cosine similarity.
`index = cos.argmax()`
Finally we can return the reply, `return(data.iloc[index]["Replies"])`
## **Demo**
---
Chatbot Conversation via terminal
![demo](https://user-images.githubusercontent.com/40771653/99419858-93c94480-2922-11eb-802b-e0c0a3eac877.png)
### Reference
For extracting dataset(Deatiled Explanation): [Sentdex youtube playlist](https://www.youtube.com/watch?v=dvOnYLDg8_Y&list=PLQVvvaa0QuDdc2k5dwtDTyT9aCja0on8j)
