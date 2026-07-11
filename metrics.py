import numpy as np

def calculate_accuracy(actual, predicted):

    actual = np.array(actual)
    predicted = np.array(predicted)

    # avoid divide by zero
    actual = np.where(actual == 0, 1, actual)

    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    accuracy = 100 - mape

    return round(accuracy, 2), round(mape, 2)