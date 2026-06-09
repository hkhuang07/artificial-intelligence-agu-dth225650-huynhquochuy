# chen thu vien
import pandas as pd
import numpy as np
import os

# load DT
from sklearn import tree

# load dataset from csv file 
data = pd.read_csv('weather.csv')
data.head()

# chuyen kieu DL tu string sang numeric
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
for column_name in data.columns:
	if data[column_name].dtype == object:
		data[column_name] = le.fit_transform(data[column_name])
	else:
		pass

# tach nhan tap du lieu
y = data['play']
X = data.ix[:, "outlook":"windy"]

clf = tree.DecisionTreeClassifier(criterion="entropy")
clf = clf.fit(X, y)
