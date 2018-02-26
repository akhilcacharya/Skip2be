#!/usr/bin/env python3

import sys
import os
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import average_precision_score, accuracy_score, recall_score
import numpy as np
from scipy.sparse import coo_matrix, hstack
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix

def build_vectorizor(corpus):
    vectorizer = TfidfVectorizer(analyzer="word", ngram_range=(1,2))
    vectorizer.fit(corpus)
    return vectorizer


def main(args): 
    if len(args) != 1: 
        print("Usage: train.py [data set]")
        sys.exit(1)

    train = open(args[0], encoding="ISO-8859-1")

    X = []
    y = []
    corpus = []
    times = []


    for line in train:
        label, chunk, time = line.rstrip().split("\t")
        label = int(label)

        for _ in range(0, 1 + 0*label):
            corpus.append(chunk)
            y.append(label)
            times.append(float(time))

    vectorizer = build_vectorizor(corpus)
    X = vectorizer.transform(corpus)
    times = (np.array(times)).reshape((-1,1))
    X = hstack((X, times))

    # Split Data
    X_train, X_val, y_train, y_val, corpus_train, corpus_val = train_test_split(X,y,corpus, test_size=0.50)

    # Train SVM
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
    print("recall: ", recall_score(y_val, predictions))
    print("Acc: ", accuracy_score(y_val, predictions))
    print(confusion_matrix(y_val, predictions))


    print("Saving Model!")
    joblib.dump(vectorizer, 'vectorizer.pkl')
    joblib.dump(clf, 'trained_svm.pkl')


    # Let user input examples
    while True:
        test = input('Enter a chunk: ')
        test = [test] * 9
        test = vectorizer.transform(test)
        test = hstack((test, np.linspace(0,1, num=9).reshape((-1,1))))

        print(test)
        print(clf.predict(test))
    
if __name__ == "__main__":
    main(sys.argv[1:])
