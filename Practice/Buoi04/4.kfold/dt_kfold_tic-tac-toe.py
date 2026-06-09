#Importing required libraries
import pandas as pd
from sklearn.model_selection import KFold 
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import accuracy_score
 
# load DT
from sklearn import tree
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
