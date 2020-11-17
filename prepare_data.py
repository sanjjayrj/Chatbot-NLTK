import pandas as pd
import re

data = pd.DataFrame()

def read_data():
    with open('train.from', 'r') as fin, open('train.to','r') as fout:
        fin_read = [readin.rstrip() for readin in fin]
        fout_read = [readout.rstrip() for readout in fout]
    data['Content'] = fin_read
    data['Replies'] = fout_read

def fix(ch):
    for i in ch:
        a = str(i).lower()
        p = re.sub(r'[^a-z0-9]',' ', a)

if __name__ == '__main__':
    read_data()
    fix(data['Content'])
    fix(data['Replies'])
    print("Data read into the dataframe...\n")
    print(data.info())
    print("----------------------------------------------------------------------------------------------------------")
    print(data.head())
    print("----------------------------------------------------------------------------------------------------------")
    print(data.tail())
    print("----------------------------------------------------------------------------------------------------------")
    data.to_csv('traindata.csv', index = False)