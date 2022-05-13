from tkinter import *
import glob
import re
import nltk
import os
import numpy as np
from numpy import dot
from numpy.linalg import norm
import math
import json
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()

from nltk.tokenize import sent_tokenize, word_tokenize
stemmer=PorterStemmer()
output=[]
#if Click on Search button
def search():
    global stopwords
    q_vec=[]
    global doc_vec
    global dic
    global idf
    q_mag=0
    doc_mag=0
    cosine_value={}
    output_docs=[]
    query = screen.get()
    query = query.lower()

    # remove puntuations
    query = re.sub('[^0-9a-z\s]', ' ', query)

    # Make token if query
    query = word_tokenize(query)

    # remove stopwords
    for word in query:
        if word in stopwords:
            query.remove(word)

    # #Apply lemmatization
    j = 0
    for word in query:
        query[j] = lemmatizer.lemmatize(word)
        j = j + 1

    # j = 0
    # # Apply Stemming on queuery
    # for word in query:
    #     query[j] = stemmer.stem(word)
    #     j = j + 1

    #assign weights in query
    for terms in dic:
        if(terms in query):
            q_vec.append(idf[terms])
            #magnitude of query
            q_mag=q_mag+(idf[terms]*idf[terms])
        else:
            q_vec.append(0.0)

    #cosine similarity
    for docs in doc_vec:
        #finding dot product and magnitue for cosine value
        value=dot(doc_vec[docs],q_vec) / (norm(doc_vec[docs]) * norm(q_vec))
        cosine_value[docs]=value
        if(value>0.001):
            output_docs.append(docs)

    print(output_docs)

    global output
    output = Label(root, text="", font=("Helvetica", 13), wraplength=700)
    output.place(x=30, y=300)
    global tx
    tx = Label(root, text="Retrieved Documents: ", font=("Helvetica", 18))
    tx.place(x=10, y=250)
    if (len(output_docs) > 0):
        # print output
        output = Label(root, text=output_docs, font=("Helvetica", 13), wraplength=1100)
        output.place(x=30, y=300)
        return None
    else:
        print("none")


#open stop word file and read stopwords from file
f = open("Stopword-List.txt")
stopwords = f.read()
stopwords = word_tokenize(stopwords)
f.close()

with open('doc_vector.json', 'r') as infile1:
    # Reading from json file
    doc_vec = json.load(infile1)

with open('index.json', 'r') as infile2:
    # Reading from json file
    dic = json.load(infile2)

with open('idf.json', 'r') as infile3:
    # Reading from json file
    idf = json.load(infile3)


root = Tk()
#Set size and background-color of window of Application
root.geometry("900x600")
root.configure(background='#6666ff')
root.title("Boolean Retrievel Model")

text = Label(root, text="Search Query: ", font=('Helvetica 22 bold'))
text.place(x=50,y=60)

# clear query and output
def clear_text():
    global output
    screen.delete(0,END)
    output.destroy()

#Create SearchBox for Input Queuery
screen=Entry(root, font="lucida 20" , bg='#33FFFF' ,bd="4",width=55 )
screen.place(x=50,y=100)

#Create button for search
b1=Button(root,text="Search",command=search,font='Helvetica', bg='#0000CC', height=2, width=12,fg='white')
b1.place(x=80,y=170)

#create button for clearing
b2=Button(root,text="Clear",command=clear_text,font='Helvetica', bg='#0000CC', height=2, width=12,fg='white')
b2.place(x=230,y=170)

root.mainloop()