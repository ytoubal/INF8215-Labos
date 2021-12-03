"""
Team:
<<<<< TEAM NAME >>>>>
Authors:
<<<<< NOM COMPLET #1 - MATRICULE #1 >>>>>
<<<<< NOM COMPLET #2 - MATRICULE #2 >>>>>
"""

from wine_testers import WineTester
#Use Random Forest Classifier to train a prediction model
# evaluate random forest algorithm for classification
from numpy import mean
from numpy import std

class MyWineTester(WineTester):
    def __init__(self):
        # TODO: initialiser votre modèle ici:
        pass

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
        # TODO: entrainer un modèle sur X_train & y_train
        #print(X_train) #id et attributs, sans la colonne quality
        
        for attributes in X_train:
            if len(attributes) < 13: print("Il en manque")
        RF_clf = RandomForestClassifier(random_state=seed)
        raise NotImplementedError()

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
        # TODO: make predictions on X_data and return them
        raise NotImplementedError()
