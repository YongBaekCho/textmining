import string, pandas as pd, numpy as np
from sklearn.feature_extraction import stop_words
from nltk.stem import SnowballStemmer
import math
'''
Name: YongBaek Cho
Description:Text Mining and Cosine Similarity
'''
def dot_product(v1, v2):
# this function takes two dictionaries representing vectors and returns their dot products.
    return sum(v1[key]*v2.get(key, 0) for key in v1)

def magnitude(v):
#  this function takes a dictionary representing a vector and returns its magnitude
    inside = 0
    for key in v:
        inside += v[key]**2
    return math.sqrt(inside)

def cosine_similarity(v1,v2):
# this function takes two dictionaries representing vectors and returns their cosine similarity. 
    return dot_product(v1,v2) / (magnitude(v1)*magnitude(v2))

def get_text(filename):
#this function takes a filename and returns a cleaned-up version of the contents of the file as a single string.  Get rid of all occurrences of the substring "n't".
    file = open(filename,"r").read().lower().replace("n't","")
    digit = '0123456789'

    for ch in string.punctuation:
        file = file.replace(ch,"")
    for num in digit:
        file = file.replace(num,"")
    return file

def vectorize(filename,stop_words_dict,stemmer_object):
#  this function takes a filename, a stop_words dictionary, and a stemmer, and returns a dictionary representing a wordcount vector mapping cleaned words from the file to wordcounts. 
    v = {}
    file = get_text(filename).split()

    for word in file:
        word = stemmer_object.stem(word)
        if not word in stop_words_dict:
            if not word in v.keys():
                v[word] = 1
            else:
                v[word] += 1
    return v

def get_doc_freqs(v_list):
#this function takes a list of wordcount vectors and returns a dictionary that maps each of the keys from all of the vectors to the number of documents that contained the given key.
    v = {}

    for dictionary in v_list:
        for key in dictionary.keys():
            if key not in v.keys():
                v[key] = 1
            else:
                v[key] += 1

    return v

def tfidf(v_list):
# this function takes a list of wordcount vectors (dictionaries, one for each document) and replaces all of the wordcounts with TFIDF's.
    doc_freqs = get_doc_freqs(v_list)
    scale = 1 if len(v_list) > 100 else 100 / len(v_list)
    for wc_vector in v_list:
        for key in wc_vector:
            wc_vector[key] *= 1 + math.log2(scale * len(v_list) / doc_freqs[key]) 

def get_similarity_matrix(file_list,stop_words_dict,stemmer):
# this function takes a list of filenames, a stop_words dictionary, and a stemmer, and returns a matrix of similarities (a DataFrame
    v_list = []
    df = pd.DataFrame(index=file_list,columns=file_list)

    for file in file_list:
        v = vectorize(file,stop_words_dict,stemmer)
        v_list.append(v)
    tfidf_ = tfidf(v_list)

    for i in range(len(df.index)):
        for j in range(len(df.columns)):
            if i == j:
                df.iloc[i,j] = 1
            else:
                df.iloc[i,j] = cosine_similarity(v_list[i],v_list[j])
    return df

def matrix_pretty_string(matrix):
# this function takes a similarity matrix and returns a string representing the matrix that prints prettily.
    ans = "".ljust(7," ")
    for col in matrix.columns:
        if not len(col) > 7:
            ans += "|" + col.replace(".txt","").ljust(7," ")
        else:
            ans += "|" + col.replace(".txt","").ljust(7," ")[:7]
    ans += "\n"
    ans += "-------|" + "---------------------------------------------------\n"

    for row in matrix.index:
        if not len(row) > 7:
            ans += row.replace(".txt","").ljust(7," ")
        else:
            ans += row.replace(".txt","").ljust(7," ")[:7]
        for col in matrix.columns:
            ans +=  "|" + str(round(matrix.loc[row,col],3)).rjust(7," ")
        ans += "\n"

    return ans

def main():
    a_list = ['gotg2a.txt', 'gotg2b.txt', 'gotg1.txt', 'aaou.txt', 'gw.txt', 'saguaro.txt']
    stop_words_list = list(stop_words.ENGLISH_STOP_WORDS) + ['did','gone','ca']
    stop_words_aa = []
    
    for word in stop_words_list:
        stop_words_aa == None
    stemmer_object = SnowballStemmer("english")
    stop_words_set = (k for k in stop_words.ENGLISH_STOP_WORDS)
    
    print(matrix_pretty_string)
     
main()

