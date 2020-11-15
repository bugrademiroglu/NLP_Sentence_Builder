import nltk
import os
import random
import string
import ssl
import re
import math
from nltk.tokenize import sent_tokenize
import sys
import pandas as pd
from nltk.corpus import (
    gutenberg,
    genesis,
    inaugural,
    nps_chat,
    webtext,
    treebank,
    wordnet,
    PlaintextCorpusReader,
    brown,
    stopwords
)
from nltk.stem.porter import *
from nltk.text import Text
from nltk.probability import FreqDist
from nltk.util import bigrams
from nltk.util import tokenwrap, LazyConcatenation
from nltk.tokenize import word_tokenize
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

#Getting input from the user and applying language models to that input
def start():
    print("Enter the path of your corpus: ")
    #Getting text file location from terminal
    corpus = sys.argv[1]
    print(corpus)
    if(len(corpus) == None):
        print("Corpus cannot be zero")
    #User chooses which language model to use
    print("Which lanuage model do you want to work with ?")
    print("Unigram [1]")
    print("Bigram [2]")
    print("Trigram [3]")
    userInput = input("Enter your choose: ")

    # Calling the language model function according to the input received from the user
    if(userInput == "1"):
        unigramModel(corpus)
    elif(userInput == "2"):
        bigramModel(corpus)
    elif(userInput == "3"):
        trigramModel(corpus)
    else:
        print("Wrong Input")

# Unigram language model function
def unigramModel(corpus):
    print(corpus)

    # Creating a new corpus
    newcorpus = PlaintextCorpusReader(os.path.abspath(corpus),"nlp_project2_corpus.txt")
    newcorpus.raw("nlp_project2_corpus.txt")
    newcorpus.sents("nlp_project2_corpus.txt")
    # Getting Enwords from created corpus
    enwords = newcorpus.words("nlp_project2_corpus.txt")
    entext = newcorpus.raw("nlp_project2_corpus.txt")
    entokens = nltk.word_tokenize(entext)
    unigram = entokens
    enmodel = nltk.Text(word.lower() for word in enwords)
    unigram_freq = nltk.FreqDist(unigram)
    unigramCounter = 0
    ourTextArray = []
    unigramProb = 0

    #Creating unigram counter to find the total number of common words
    for l in unigram_freq.most_common():
        unigramCounter += 1
    # Iterating the most common sentences and appyling probabilities
    for i, j in unigram_freq.most_common():

        # Finding the probabilities
        unigramProb += (j / (unigramCounter)) / 10

        # The probability is higher than 0.80 then add that word into array
        if (unigramProb > 0.80):

            str1 = re.sub(r'[^a-zA-Z0-9_\s]+', '', i)
            ourTextArray.append(str1)
            if (len(ourTextArray) > 200):
                break
    # Creating and printing a new 300 word text using the unigram language model
    ourTextArray = list(set(ourTextArray))
    finalTextim = ""
    for i in range(len(ourTextArray)):
        finalTextim += " " + ourTextArray[i]
    print(finalTextim)


    entagged = nltk.pos_tag(entokens)

# Unigram language model function
def bigramModel(corpus):
    newcorpus = PlaintextCorpusReader(corpus,"nlp_project2_corpus.txt")

    newcorpus.raw("nlp_project2_corpus.txt")
    newcorpus.sents("nlp_project2_corpus.txt")
    enwords = newcorpus.words("nlp_project2_corpus.txt")
    entext = newcorpus.raw("nlp_project2_corpus.txt")
    entokens = nltk.word_tokenize(entext)
    # Applying bigram to sentence
    bigrams = nltk.bigrams(entokens)



    # With FreqDist we look at word frequency
    bigrams_freq = nltk.FreqDist(bigrams)

    ourTextArr = []
    bigramCounter = 0
    for i in bigrams_freq.most_common():
        bigramCounter += 1

    prob = 0
    for i, j in bigrams_freq.most_common():

        if (j > 2):

            prob += j / (bigramCounter / 10)
        if prob > 0.9:
            str1 = re.sub(r'[^a-zA-Z0-9_\s]+', '', i[0])
            str2 = re.sub(r'[^a-zA-Z0-9_\s]+', '', i[1])
            ourTextArr.append(str1 + " " + str2)
            if len(ourTextArr) > 200:
                break
    ourTextArr = list(set(ourTextArr))

    finalText = ""

    ourTextArr.reverse()
    # Creating and printing a new 300 word text using the bigram language model
    for i in range(len(ourTextArr)):
        finalText += " " + ourTextArr[i]
    print(finalText)


# Unigram language model function
def trigramModel(corpus):
    newcorpus = PlaintextCorpusReader(corpus,"nlp_project2_corpus.txt")

    newcorpus.raw("nlp_project2_corpus.txt")
    newcorpus.sents("nlp_project2_corpus.txt")
    enwords = newcorpus.words("nlp_project2_corpus.txt")
    entext = newcorpus.raw("nlp_project2_corpus.txt")
    entokens = nltk.word_tokenize(entext)
    # Applying trigram to sentence
    trigram = nltk.trigrams(entokens)

    trigrams_freq = nltk.FreqDist(trigram)
    ourTextArr2 = []
    counter = 0
    prob = 0
    trigramCounter = 0
    probBiGram = 0

    bigrams = nltk.bigrams(entokens)

    bigrams_freq = nltk.FreqDist(bigrams)

    ourTextArr = []
    bigramCounter = 0
    for i in bigrams_freq.most_common():
        bigramCounter += 1

    for i in trigrams_freq.most_common():
        trigramCounter += 1

    for i, j in trigrams_freq.most_common():

        if prob > 0.50:
            print("********PROBB****: ", prob)
        if (j > 0):

            for k, l in bigrams_freq.most_common():
                if (j > 2):
                    probBiGram += l / (bigramCounter / 10)

            prob += j / (trigramCounter / 10)
        prob = ((prob + probBiGram) - (prob * probBiGram)) / trigramCounter

        if prob > 0.45:
            str1 = re.sub(r'[^a-zA-Z0-9_\s]+', '', i[0])
            str2 = re.sub(r'[^a-zA-Z0-9_\s]+', '', i[1])
            str3 = re.sub(r'[^a-zA-Z0-9_\s]+', '', i[2])
            ourTextArr2.append(str1 + " " + str2 + " " + str3)
            if (len(ourTextArr2) > 200):
                break
    ourTextArr2 = list(set(ourTextArr2))
    finalText2 = ""
    counter3 = 0
    ourTextArr2.reverse()

    for i in range(len(ourTextArr2)):
        counter3 += 1
        finalText2 += " " + ourTextArr2[i]
    print(finalText2)


start()