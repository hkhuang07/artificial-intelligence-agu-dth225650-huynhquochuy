#Importing required libraries
import pandas as pd
from sklearn.model_selection import KFold 
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import accuracy_score
 
# load DT
from sklearn import tree

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import preprocessing


# load dataset from csv file 
data = pd.read_csv('../Data/segmentation.test', sep=',') 
data.head()

le = preprocessing.LabelEncoder()
for column_name in data.columns:
    if data[column_name].dtype == object:
        if column_name == data.columns[0]:
            le_y = le
        data[column_name] = le.fit_transform(data[column_name])
    else:
        pass

#n = len(data.columns) 
n = len(data.iloc[1,:]) 
y = data.iloc[:,0]
X = data.iloc[:, 1:n] 


 
#Implementing cross validation
 
k = 10
kf = KFold(n_splits=k, random_state=None)
model = DecisionTreeClassifier()
 
acc_score = []
 
for train_index , test_index in kf.split(X):
    X_train , X_test = X.iloc[train_index,:],X.iloc[test_index,:]
    y_train , y_test = y[train_index] , y[test_index]
     
    model.fit(X_train,y_train)
    pred_values = model.predict(X_test)
     
    acc = accuracy_score(pred_values , y_test)
    acc_score.append(acc)
     
avg_acc_score = sum(acc_score)/k
 
print('accuracy of each fold - {}'.format(acc_score))
print('Avg accuracy : {}'.format(avg_acc_score))
