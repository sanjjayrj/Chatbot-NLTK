import sqlite3
import pandas as pd

timeframes = ['2015-05']

for timeframe in timeframes:
    connection = sqlite3.connect('{}.db'.format(timeframe))
    c = connection.cursor()
    limit = 5000
    last_unix = 0
    cur_length = limit
    counter = 0
    while cur_length == limit:
        df = pd.read_sql("SELECT  * FROM parent_reply WHERE unix > {} AND parent NOT NULL AND score > 0 ORDER BY UNIX ASC LIMIT {}".format(last_unix, limit), connection)
        last_unix = df.tail(1)['unix'].values[0]
        cur_length = len(df)
        with open("train.from", 'a', encoding = 'utf8') as f:
            for content in df['parent'].values:
                f.write(content+'\n')
        with open("train.to", 'a', encoding = 'utf8') as f:
            for content in df['comment'].values:
                f.write(content+'\n')

        counter+=1
        if counter % 20 == 0:
            print(counter*limit, " rows completed so far")
