#!/usr/bin/env python3

import sys
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import average_precision_score, accuracy_score
import numpy as np
from scipy.sparse import coo_matrix, hstack
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer


def main(args): 
    if len(args) != 1: 
        print("Usage: train.py [data set]")
        sys.exit(1)

    vectorizer = CountVectorizer(ngram_range=(1,3))
    transformer = TfidfTransformer()

    train = open(args[0])

    X = []
    y = []
    corpus = []
    times = []

    for line in train:
        label, chunk, time = line.rstrip().split("\t")
        label = int(label)

        for i in range(0, 1 + 8 * label):
            corpus.append(chunk)
            y.append(label)
            times.append(float(time))

    vectorizer.fit(corpus)
    
    X = vectorizer.transform(corpus)
    transformer.fit(X)
    X = transformer.transform(X)

    times = (np.array(times)).reshape((-1,1))
    X = hstack((X, times))

    # Split Data
    X_train, X_val, y_train, y_val, corpus_train, corpus_val = train_test_split(X,y,corpus, test_size=0.50)

    clf = LinearSVC(random_state=0)
    clf.fit(X_train,y_train)

    predictions = clf.predict(X_val)

    
    for p, chunk, truth in zip(predictions, corpus_val, y_val):
        if(p != truth):
            print("{} {} {}".format(p, chunk, truth))
    

    print("precision-recall: ", average_precision_score(y_val, predictions))
    print("Acc: ", accuracy_score(y_val, predictions))

    
    while True:
        test = input('Enter a chunk: ')
        test = [test] * 9
        test = vectorizer.transform(test)
        test = transformer.transform(test)
        test = hstack((test, np.linspace(0,1, num=9).reshape((-1,1))))

        print(test)
        print(clf.predict(test))
    


if __name__ == "__main__":
    main(sys.argv[1:])