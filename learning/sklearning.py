import sklearn
from sklearn import svm, datasets, metrics
from sklearn.neighbors import KNeighborsClassifier
import numpy as np


def main():
    cancer = datasets.load_breast_cancer()

    x = cancer.data
    y = cancer.target

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
        x, y, test_size=0.2)

    classes = ['malignant' 'benign']

    clf = svm.SVC(kernel='linear', C=2)
    #clf = KNeighborsClassifier(n_neighbors=9)
    clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)

    print(accuracy)


if __name__ == '__main__':
    main()
