"""
Team:
<<<<< les dindons >>>>>
Authors:
<<<<< Yanis Toubal – 1960266 >>>>>
<<<<< Yuhan Li – 1947497 >>>>>
"""

from wine_testers import WineTester
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
class MyWineTester(WineTester):
    def __init__(self):
        self.seed = 23
        self.classifier = RandomForestClassifier(n_estimators=1000, oob_score= True, random_state=self.seed)
        self.columns = ['id', 'color', 'fixed acidity', 'volatile acidity', 'citric acid',
                        'residual sugar', 'chlorides', 'free sulfur dioxide',
                        'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol',
                       ]
        
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
                
        # Get dataframes
        data_frame = pd.DataFrame(X_train)
        quality_frame = pd.DataFrame(y_train)
        
        # Prepare dataframes
        data_frame.columns = self.columns
        quality_frame.columns = ['id', 'quality']
        data_frame['quality'] = quality_frame['quality'] # add quality to entire dataframe
        data_frame['color'] = data_frame['color'].astype('category').cat.codes # convert wine color to number

        # Split data into features (X) and label (Y)
        y = data_frame['quality']    
        X = data_frame.drop(['quality'], axis=1)  # rest are features
        
        # Using the whole dataset as a training set 
        X_train, y_train = X,y
        
        # Perform training of the classifier
        self.classifier.fit(X_train, y_train)

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
        # Create the dataframe
        data_frame = pd.DataFrame(X_data)    

        # Prepare the dataframe
        data_frame.columns = self.columns
        data_frame['color'] = data_frame['color'].astype('category').cat.codes # convert wine color to number

        # Predict the label from the features
        results = self.classifier.predict(data_frame)
        
        # Format the output
        prediction = []
        for i, result in enumerate(results):
            prediction.append([i, result])
        
        return prediction


from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
class MyWineTesterNN(WineTester):
    def __init__(self):
        self.seed = 10
        self.classifier = MLPClassifier(hidden_layer_sizes=(11,), max_iter=50, activation='relu', solver='sgd', learning_rate_init=0.3, random_state=self.seed)
        self.columns = ['id', 'color', 'fixed acidity', 'volatile acidity', 'citric acid',
                        'residual sugar', 'chlorides', 'free sulfur dioxide',
                        'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol',
                       ]
        
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

        # Convert training data into float (for correlation matrix)
        for i, attributes in enumerate(X_train):
            for j, attribute in enumerate(attributes):
                if j==1 or j==0: continue
                X_train[i][j] = float(attribute)
                
        # Get dataframes
        data_frame = pd.DataFrame(X_train)
        quality_frame = pd.DataFrame(y_train)
        
        # Prepare dataframes
        data_frame.columns = self.columns
        quality_frame.columns = ['id', 'quality']
        data_frame['quality'] = quality_frame['quality'] # add quality to entire dataframe
        data_frame['color'] = data_frame['color'].astype('category').cat.codes # convert wine color to number

        # Split data into features (X) and label (Y)
        y = data_frame['quality']    
        X = data_frame.drop('quality', axis=1)  # rest are features
        
        # Normalizing the features
        minmax=MinMaxScaler(feature_range=(0, 1), copy=True)
        X = pd.DataFrame(minmax.fit_transform(X)) #normalize data
        
        # Split data into training and test datasets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=self.seed)
    
        # Training the dataset
        self.classifier.fit(X_train, y_train)

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

        # Create the dataframe
        data_frame = pd.DataFrame(X_data)

        # Prepare the dataframe
        data_frame.columns = self.columns
        data_frame['color'] = data_frame['color'].astype('category').cat.codes # convert wine color to number
        
        # Normalize the features
        minmax=MinMaxScaler(feature_range=(0, 1), copy=True)
        data_frame = pd.DataFrame(minmax.fit_transform(data_frame))

        # Predict the label from the features
        results = self.classifier.predict(data_frame)
        
        # Format the output
        prediction = []
        for i, result in enumerate(results):
            prediction.append([i, result])
        
        return prediction