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
# from numpy import mean
# from numpy import std
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

class MyWineTester(WineTester):
    def __init__(self):
        # TODO: initialiser votre modèle ici:
        self.seed = 10
        #self.classifier = RandomForestClassifier(random_state=self.seed)
        #{'activation': 'tanh', 'hidden_layer_sizes': (11,), 'learning_rate_init': 0.01, 'solver': 'sgd'}
        self.classifier = MLPClassifier(hidden_layer_sizes=(11,), max_iter=50, activation='relu', solver='sgd', learning_rate_init=0.3, random_state=self.seed)

        
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

        # Convert training data into float (for correlation matrix)
        for i, attributes in enumerate(X_train):
            for j, attribute in enumerate(attributes):
                if j==1 or j==0: continue
                X_train[i][j] = float(attribute)
                
        # Get dataframes
        data_frame = pd.DataFrame(X_train)
        quality_frame = pd.DataFrame(y_train)
        
        # Prepare dataframes
        data_frame.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        quality_frame.columns = ['0', '1']
        data_frame['13'] = quality_frame['1'] # add quality to entire dataframe
        data_frame['1']=data_frame['1'].astype('category').cat.codes # convert wine color to number
        
        minmax=MinMaxScaler(feature_range=(0, 1), copy=True)
        print(data_frame)

        # Correlation matrix
        corr = data_frame.corr()
        print(corr)

        # Split data into training and test datasets
        y = data_frame['13']    
        X = data_frame.drop('13', axis=1)  # rest are features
        X = minmax.fit_transform(X)
        X = pd.DataFrame(X)
        print(y.shape, X.shape)
   
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=self.seed)
        
        # #test parameters
        # parameter_space = {
        #     'hidden_layer_sizes': [(10,), (11,), (12,), (13,)],
        #     'activation': ['tanh', 'relu'],
        #     'solver': ['sgd', 'adam'],
        #     'learning_rate_init': [0.001, 0.01, 0.1],
        # }

        # from sklearn.model_selection import GridSearchCV

        # clf = GridSearchCV(self.classifier, parameter_space, n_jobs=-1, cv=3)
        # clf.fit(X_train, y_train)

        # print('Best parameters found:\n', clf.best_params_)

        # # All results
        # means = clf.cv_results_['mean_test_score']
        # stds = clf.cv_results_['std_test_score']
        # for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        #     print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))

        # clf.fit(X_train, y_train)
        # prediction = clf.predict(X_test)
        # print(classification_report(y_test, prediction))
        #Perform predictions
        self.classifier.fit(X_train, y_train)
        prediction = self.classifier.predict(X_test)
        print(y_test)
        print(X_test)
        print(classification_report(y_test, prediction))

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
        #print(X_data)
        minmax=MinMaxScaler(feature_range=(0, 1), copy=True)
        data_frame = pd.DataFrame(X_data)

        data_frame.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        data_frame['1'] = data_frame['1'].astype('category').cat.codes # convert wine color to number
        data_frame = minmax.fit_transform(data_frame)
        data_frame = pd.DataFrame(data_frame)

        results = self.classifier.predict(data_frame)
        
        prediction = []
        for i, result in enumerate(results):
            prediction.append([i, result])
        
        return prediction