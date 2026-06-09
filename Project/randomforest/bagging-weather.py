#Import library to work with file
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

#Baggging Ensemble Learing Using Decision Tree
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import os

#Tài và tiền xử lý dữ liệu 
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
    
#Tách tập dữ liệu
y = data['play']
X = data.iloc[:,0:4]

X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.20, # 20% test
    random_state=42, 
    stratify=y 
)
#Sử dụng giải thuật học máy là Decision Tree
base_elf = DecisionTreeClassifier(random_state = 42)

#Khởi tạo mô hình bagging 100 Decission Tree sử dụng OOB hoặc không
bg_elf = BaggingClassifier(base_elf, n_estimators=100,oob_score=True, random_state=42)
#bg_elf = BaggingClassifier(base_elf, n_estimators=100, random_state=42)

#Fit dữ liệu vào vào 2 tập huấn luyện
bg_elf.fit(X_train,y_train)

oob_accuracy = bg_elf.oob_score_
print("Accuracy of OOB (Out-of-Bag Score): {}".format(oob_accuracy))

#Dự đoán trên tập kiểm tra
y_pred = bg_elf.predict(X_test)

# Đánh giá độ chính xác
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy (Bagging Ensemble): {:.4f}".format(accuracy))

print("\n--- Detailed Test Results ---")
print(f"Number of test data points: {len(X_test)}")
print("Ground Truth (Actual Labels):\n", y_test.reset_index(drop=True))
print("Predicted Labels (Model Output):", y_pred)

print('\n--- Classification Report ---')
print("Note: '0' corresponds to 'no', '1' corresponds to 'yes' for the 'play' target.")
print(classification_report(y_test, y_pred, zero_division=0))