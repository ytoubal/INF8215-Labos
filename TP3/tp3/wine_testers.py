"""
 - Abstract class pour WineTester
 - Random Baseline pour WineTester
"""

from abc import ABC, abstractmethod
import random


class WineTester(ABC):
    """
    Abstract class for all predictors
    """
    @abstractmethod
    def train(self, X_train, y_train):
        """
        train the current model on train_data
        :param X_train: 2D array of data points.
                each line is a different example.
                each column is a different feature.
                the first column is the example ID.
        :param y_train: 2D array of labels.
                each line is a different example.
                the first column is the example ID.
                the second column is the example label.
        """
        raise NotImplementedError()

    @abstractmethod
    def predict(self, X_data):
        """
        predict the labels of the test_data with the current model
        and return a list of predictions of this form:
        [
            [<ID>, <prediction>],
            [<ID>, <prediction>],
            [<ID>, <prediction>],
            ...
        ]
        :param X_data: 2D array of data points.
                each line is a different example.
                each column is a different feature.
                the first column is the example ID.
        :return: a 2D list of predictions with 2 columns: ID and prediction
        """
        raise NotImplementedError()

    @staticmethod
    def get_accuracy(y_pred, y_gold):
        assert len(y_pred) == len(y_gold), \
            f"number of predictions ({len(y_pred)}) != number of examples ({len(y_gold)})"
        correct = 0
        for pred, true in zip(y_pred, y_gold):
            if int(pred[0]) != int(true[0]):
                print(f"[WARNING] prediction IDs not in order. pred: {pred} -vs- true: {true}")
            elif int(pred[1]) == int(true[1]):
                correct += 1
        return correct / len(y_gold)


class RandomWineTester(WineTester):
    """
    A random model
    """
    def __init__(self):
        self.class_probabilities = [0]*10

    def train(self, X_train, y_train):
        """
        train the current model on train_data
        :param X_train: 2D array of data points.
                each line is a different example.
                each column is a different feature.
                the first column is the example ID.
        :param y_train: 2D array of labels.
                each line is a different example.
                the first column is the example ID.
                the second column is the example label.
        """
        # reset stats
        self.class_probabilities = [0] * 10

        # get stats from y_train
        for _, quality in y_train:
            quality = int(quality)
            self.class_probabilities[quality - 1] += 1

    def predict(self, X_data):
        """
        predict the labels of the test_data with the current model
        and return a list of predictions of this form:
        [
            [<ID>, <prediction>],
            [<ID>, <prediction>],
            [<ID>, <prediction>],
            ...
        ]
        :param X_data: 2D array of data points.
                each line is a different example.
                each column is a different feature.
                the first column is the example ID.
        :return: a 2D list of predictions with 2 columns: ID and prediction
        """
        # predict random samples based on computed probabilities
        samples = random.choices(range(1, 11), weights=self.class_probabilities, k=len(X_data))
        # build the 2D list of "id", "target"
        predictions = []
        for idx, pred in enumerate(samples):
            predictions.append([int(X_data[idx][0]), pred])
        return predictions

    def __str__(self):
        return f"class counts: {self.class_probabilities}"
