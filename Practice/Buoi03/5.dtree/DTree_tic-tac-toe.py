#File tic-tac-toe

# chen thu vien
import pandas as pd
import numpy as np
import os

# load DT
from sklearn import tree

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn import preprocessing


# load dataset from csv file 
data = pd.read_csv('../Data/tic-tac-toe.data', sep=',', header=None) 
data.head()

data_encoded = data.copy()
le_dict = {}

for column_name in data_encoded.columns:
    if data_encoded[column_name].dtype == object:
        le_col = preprocessing.LabelEncoder()
        data_encoded[column_name] = le_col.fit_transform(data_encoded[column_name])
        le_dict[column_name] = le_col 

data = data_encoded

n = len(data.columns) 
y = data.iloc[:,-1]
X = data.iloc[:, 0:n-1] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

print("Training size: %d" % len(y_train))
print("Test size    : %d" % len(y_test))

from sklearn.tree import DecisionTreeClassifier
clf= DecisionTreeClassifier(criterion="gini")
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print("Print results for 2 test data points:")
print("Predicted labels: ", y_pred[15:35])
print("Ground truth    : ", y_test[15:35])

print("Accuracy of Decision tree: %.2f %%" % ( 100 * accuracy_score(y_test, y_pred)))
print('Classification Report:\n{}\n'.format(classification_report(y_test,clf.predict(X_test))))
