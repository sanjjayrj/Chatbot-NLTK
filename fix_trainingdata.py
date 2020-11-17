import re
import os
from datetime import datetime
filein = 'train.from'
fileout = 'train.to'

blacklist_file = open('vocab_blacklist.txt', 'r')
blacklist = [line.rstrip() for line in blacklist_file]
blacklist_file.close()
counter = 0

def censor():
    global counter
    output1 = []
    output2 = []
    with open(filein, 'r') as fin, open(fileout, 'r') as fout:
        fin_read = fin.readlines()
        fout_read = fout.readlines()
        repair(fin_read)
        repair(fout_read)

        for (lin, lout) in zip(fin_read, fout_read):
            temp = 0
            for words in blacklist:
                if words in lin:
                    temp = 1
                elif words in lout:
                    temp = 1
            if temp == 0:
                lin.replace('newlinechar', '\n')
                output1.append(lin)
                output2.append(lout)
                if counter % 10000 == 0:
                    print(str(counter) + " sets fixed..., "+"Time now: " + str(datetime.now()))
                counter += 1

    new_from = open('train.from', 'w+')
    new_to = open('train.to', 'w+')
    new_from.writelines(output1)
    new_to.writelines(output2)
    new_from.close()
    new_to.close()

def repair(st):
    for i in st:
        a = str(i).lower()
        p = re.sub(r'[^a-z0-9]', ' ', a)

if __name__ == '__main__':
    censor()
