# chen thu vien
import pandas as pd
import numpy as np
import os

# Thêm thư viện cần thiết cho xử lý giá trị thiếu
from sklearn.impute import SimpleImputer 
from sklearn.naive_bayes import GaussianNB # Bayesian Model
# Khối import gốc: from sklearn import tree 

# load dataset from csv file 
data = pd.read_csv('../Data/breast-cancer-wisconsin.data', header=None) 
data.head()

from sklearn import preprocessing
le = preprocessing.LabelEncoder()

for column_name in data.columns:
	if data[column_name].dtype == object:
		# Bước 1: Thay thế '?' bằng NaN
		data[column_name] = data[column_name].replace('?', np.nan) 
		# Bước 2: Chuyển đổi nhãn (nếu cột chứa object/NaN)
		# NOTE: Chúng ta chỉ cần làm việc này sau khi imputation, nếu không sẽ chuyển NaN thành chuỗi 'nan'
		pass # Bỏ qua LabelEncoder ở đây

# tach nhan tap du lieu
y = data.iloc[:,-1]
X = data.iloc[:,1:10]


# 1. Khởi tạo Imputer (điền bằng giá trị phổ biến nhất/mode)
imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent')

# 2. Áp dụng Imputation lên tập đặc trưng X
X = imputer.fit_transform(X)
X = pd.DataFrame(X, columns=data.columns[1:10])

# 3. Chuyển đổi kiểu dữ liệu về số nguyên (Bắt buộc sau Imputation)
X = X.astype(int)

# --- KHẮC PHỤC LỖI THAY THẾ DTree bằng Bayesian ---
from sklearn.naive_bayes import GaussianNB 
gnb = GaussianNB()
gnb.fit(X, y) # Huấn luyện mô hình