#Importing required libraries
import pandas as pd
import numpy as np 
from sklearn.model_selection import KFold 
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn import preprocessing


# load dataset from csv file 
data = pd.read_csv('../Data/forestfires.csv', sep=',') 
data.head()

le = preprocessing.LabelEncoder()
for column_name in data.columns:
	if data[column_name].dtype == object:
		data[column_name] = le.fit_transform(data[column_name])
	else:
		pass


n = len(data.columns) 
# Lấy cột 'area' gốc
y_area = data.iloc[:,-1]
X = data.iloc[:, 0:n-1] 

# Tạo nhãn mới: 1 nếu diện tích cháy > 0 (Fire), 0 nếu diện tích cháy = 0 (No Fire)
# Đây là bài toán phân loại nhị phân (Binary Classification)
y_binned = np.where(y_area > 0, 1, 0)
y = pd.Series(y_binned, name='fire_class') # 

# y = y.astype(int)
  
k = 10
# Cần thêm shuffle=True và random_state cho KFold để đảm bảo tính ngẫu nhiên
kf = KFold(n_splits=k, random_state=42, shuffle=True) 
model = DecisionTreeClassifier()
 
acc_score = []
 
for train_index , test_index in kf.split(X):
    X_train , X_test = X.iloc[train_index,:],X.iloc[test_index,:]
    y_train , y_test = y.iloc[train_index] , y.iloc[test_index]
    model.fit(X_train,y_train)
    pred_values = model.predict(X_test)
      
    acc = accuracy_score(pred_values , y_test)
    acc_score.append(acc)
      
avg_acc_score = sum(acc_score)/k
 
print('accuracy of each fold - {}'.format(acc_score))
print('Avg accuracy : {}'.format(avg_acc_score))