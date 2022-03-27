import pandas as pd
import os
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn import linear_model, preprocessing
import sklearn


def main():
    path = os.path.join(os.path.dirname(__file__), "../data/car/car.data")
    data = pd.read_csv(path)

    print(data)

    le = preprocessing.LabelEncoder()

    # These are numpy arrays
    buying = le.fit_transform(list(data["buying"]))
    maint = le.fit_transform(list(data["maint"]))
    door = le.fit_transform(list(data["door"]))
    persons = le.fit_transform(list(data["persons"]))
    lug_boot = le.fit_transform(list(data["lug_boot"]))
    safety = le.fit_transform(list(data["safety"]))
    cls = le.fit_transform(list(data["class"]))

    predict = "class"

    x = list(zip(buying, maint, door, persons, lug_boot, safety))
    y = list(cls)

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

    neigbor_count = 9
    model = KNeighborsClassifier(n_neighbors=neigbor_count)

    model.fit(x_train, y_train)

    accuracy = model.score(x_test, y_test)
    print(accuracy)

    predicted = model.predict(x_test)
    names = ["unacc", "acc", "good", "vgood"]
    for i in range(len(x_test)):
        print(f"P:{names[predicted[i]]}, Data:{x_test[i]}, Actual:{names[y_test[i]]}")
        n = model.kneighbors([x_test[i]], neigbor_count, True) # Get neighbors


if __name__ == '__main__':
    main()
