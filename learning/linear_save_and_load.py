import numpy as np
import pandas as pd
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import os
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

def create_model():
    relative_path = "../data/student_data/student-mat.csv"
    path = os.path.join(os.path.dirname(__file__), relative_path)
    data = pd.read_csv(path, sep=";")
    data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]

    predict = "G3"  # We want to predict final grade
    x = np.array(data.drop([predict], 1))  # All data except the one we are trying to predict
    y = np.array(data[predict]) # Data we try to predict

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

    # Linear Regression Model
    lrm = linear_model.LinearRegression()
    lrm.fit(x_train, y_train)
    accuracy = lrm.score(x_test, y_test)

    print(accuracy)
    print('Coefficients: ', lrm.coef_)
    print('Intercept', lrm.intercept_)

    return lrm

def dump(obj: any, filename: str):
    """

    :param obj: the object to be dumped
    :param filename: string, relative_poath that should include filename
    """
    with open("student_model.pickle" "wb") as file:
        pickle.dump(obj, file)

def load_model(filename: str) -> any:
    """

    :param filename: string, relative_poath that should include filename
    :return: the loaded object
    """
    with open(filename, "rb") as file:
        return pickle.load(file)


def main():

    print("Initializing...")
    lrm = create_model()
    dump(lrm, os.path.join(os.path.dirname(__file__), "../data/student_data.pickle"))

    predictions = lrm.predict(x_test)

    for prediction, d, actual in zip(predictions, x_test, y_test):
        print(prediction, d, actual)



if __name__ == '__main__':
    main()
