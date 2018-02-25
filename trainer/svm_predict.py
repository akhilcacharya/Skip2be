import sklearn
from sklearn.externals import joblib
import numpy as np
from scipy.sparse import coo_matrix, hstack

clf = joblib.load('trained_svm.pkl')
vectorizer = joblib.load('vectorizer.pkl')


def predict(chunk, time):
    v = vectorizer.transform([chunk])
    v = hstack((v, np.array([[time]])))
    return clf.predict(v)[0]


if __name__ == "__main__":
    print(predict("video description", 0.1))
    print(predict("the quick brown fox jumped over the lazy dog", 0.1))

    print(sklearn.__version__)