from tkinter import *
import glob
import re
import nltk
import os
import numpy as np
import math
import json
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
stemmer=PorterStemmer()
lemmatizer = WordNetLemmatizer()
d1 = {}
df={}
idf={}
#open stop word file and read stopwords from file
f = open("Stopword-List.txt")
stopwords = f.read()
stopwords = word_tokenize(stopwords)
f.close()

#set pat of files
file_folder = 'Abstracts/*'

n=0
#for position index
for file in glob.glob(file_folder):
    f = open(file)
    #read content of file
    content = f.read()
    content = content.lower()
    # convert 1.txt to 1 because i want doc id only
    file = re.sub('[^0-9]', '', file)
    file=int(file)

    #remove puntuations
    content = re.sub('[^0-9a-z\s]', ' ', content)

    #make tokens
    i=0
    tokens = word_tokenize(content)

    # remove stopwords
    for word in tokens:
      if word in stopwords:
        tokens.remove(word)

    # #apply lemmatization
    j = 0
    for word in tokens:
        tokens[j] = lemmatizer.lemmatize(word)
        j = j + 1

    # # apply stemming
    # j = 0
    # for word in tokens:
    #     # apply stem on every token
    #     tokens[j] = stemmer.stem(word)
    #     j = j + 1

    #Position index
    k=0
    for word in tokens:
        if word not in d1:
            d1[word]={}
            d1[word][file]=[]
            d1[word][file].append(k)

        else:
            #new word in dic
            if file not in d1[word]:
                d1[word][file] = []
                d1[word][file].append(k)

            #exixisting word with same document
            else:
                d1[word][file].append(k)
        k=k+1
    n=n+1
    f.close()


#calculate df,idf and tf*idf for every term in a document
for item in d1:
    df[item]=len(d1.get(item))
    idf[item]=math.log(n/df[item])
    idf[item]=round(idf[item],4)
    for num in d1[item]:
        d1[item][num]=len(d1[item][num])*idf[item]
        d1[item][num]=round( d1[item][num],4)

#creating vector of all documents
vec={}
for doc in range(1,n+1):
    vec[doc]=[]
    for terms in d1:
        if doc in d1[terms]:
            vec[doc].append(d1[terms][doc])
        else:
            vec[doc].append(float(0.0))

#save vector in file
with open("doc_vector.json", "w") as infile1:
    json.dump(vec, infile1)

# save index in file
with open("index.json", "w") as infile2:
    json.dump(d1, infile2)

# save idf in file
with open("idf.json", "w") as infile3:
    json.dump(idf, infile3)


