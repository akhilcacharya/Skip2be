#!/usr/bin/env python3

import sys
import os
from sklearn.svm import LinearSVC
from sklearn.metrics import average_precision_score, accuracy_score
import numpy as np
from sklearn.model_selection import train_test_split
from gensim.models import KeyedVectors
from gensim.utils import simple_preprocess
import numpy as np


def get_sentence_vec(words, vectorizer):
    sentence_vec = np.zeros(300)
    for word in words:
        try:
            sentence_vec += vectorizer.get_vector(word)
        except KeyError:
            sentence_vec += np.ones(300)
    if len(words) > 0:
        return sentence_vec/len(words)
    return sentence_vec


def main(args): 
    
    if len(args) != 1: 
        print("Usage: train.py [data set]")
        sys.exit(1)

    print("Loading word2vec!")
    vectorizer = KeyedVectors.load_word2vec_format('crawl-300d-2M.vec')

    train = open(args[0], encoding="ISO-8859-1")

    X = []
    y = []
    times = []
    corpus = []

    # Load in all of the data
    for line in train:
        label, chunk, time = line.rstrip().split("\t")
        label = int(label)
        # Normalize data
        for _ in range(0, 1 + 5 * label):
            corpus.append(chunk)
            X.append((get_sentence_vec(simple_preprocess(chunk), vectorizer)))
            y.append(label)
            times.append(float(time))

    X = np.array(X)
    times = (np.array(times)).reshape((-1,1))
    X = np.hstack((X, times))

    # Split Data
    X_train, X_val, y_train, y_val, corpus_train, corpus_val = train_test_split(X,y,corpus, test_size=0.20)

    # Train SVM
    print("Training SVM!")
    clf = LinearSVC()
    clf.fit(X_train,y_train)

    # Make predictions
    predictions = clf.predict(X_val)

    # Print the failure cases in the validation set
    for p, chunk, truth in zip(predictions, corpus_val, y_val):
        if(p != truth):
            print("{} {} {}".format(p, chunk, truth))

    # Print some metrics
    print("precision-recall: ", average_precision_score(y_val, predictions))
    print("Acc: ", accuracy_score(y_val, predictions))

    # Let user input examples
    while True:
        test = input('Enter a chunk: ')
        test = [test] * 9
        test = get_sentence_vec(simple_preprocess(chunk), vectorizer)
        test = np.hstack((test, np.linspace(0,1, num=9).reshape((-1,1))))

        print(test)
        print(clf.predict(test))
    
if __name__ == "__main__":
    main(sys.argv[1:])