# chen thu vien
import pandas as pd
import numpy as np
import os

# load DT
from sklearn import tree
from sklearn import preprocessing
import os

# load dataset from csv file 
#data = pd.read_csv('../Data/weather.data')
data = pd.read_csv('../Data/weather.data', sep='\s+', engine='python', skipinitialspace=True)
data.columns = data.columns.str.replace('"', '')
data.head()

if data.empty:
    print("Error: DataFrame is empty after loading. Check the file content and path.")
    exit()

# chuyen kieu DL tu string/symbol sang numeric
le = preprocessing.LabelEncoder()
for column_name in data.columns:
    if data[column_name].dtype == object:
        data[column_name] = le.fit_transform(data[column_name])
    else:
        pass

# tach nhan tap du lieu
y = data['play']
X = data.iloc[:,0:4]

clf = tree.DecisionTreeClassifier(criterion="entropy")
clf = clf.fit(X, y)

# xuat model cay ra hinh
import graphviz 
from graphviz import Source

feature_names = data.columns[:4].tolist()
class_names = ['no', 'yes']

dot_data = tree.export_graphviz(
    clf, 
    out_file=None, 
    feature_names=feature_names,
    class_names=class_names, 
    filled=True, 
    rounded=True,
    special_characters=True
)
graph = graphviz.Source(dot_data) 
graph.render("dtree_weather_entropy")
