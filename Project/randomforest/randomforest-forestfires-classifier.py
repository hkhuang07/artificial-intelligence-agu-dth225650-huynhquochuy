import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

import matplotlib.pyplot as plt
import os

file_path = '../Data/forestfires.csv'

try:
    data = pd.read_csv(file_path, sep=',') 
except FileNotFoundError:
    print(f"Error: File not found at {file_path}. Please check the path.")
    exit()

if data.empty:
    print("Error: DataFrame is empty after loading.")
    exit()

# Mã hóa các cột phân loại (tháng và ngày)
le = preprocessing.LabelEncoder()
for column_name in ['month', 'day']:
    if column_name in data.columns:
        data[column_name] = le.fit_transform(data[column_name])


# Dữ liệu Forestfires.csv ban đầu là HỒI QUY (dự đoán area).
# Để dùng RandomForestClassifier, ta phải chuyển nó thành bài toán PHÂN LOẠI.
# Tạo biến mục tiêu nhị phân 'is_large_fire':
# Ở đây ta dùng cách đơn giản: area > 0 (Đã cháy hay chưa)

# Tính median (trung vị) của area (chỉ lấy các giá trị > 0) để xác định ngưỡng "lớn"
area_median = data[data['area'] > 0]['area'].median()
# Nếu không có mẫu cháy, đặt ngưỡng là 1
if pd.isna(area_median):
    area_median = 1

# Tạo biến mục tiêu mới (1: Cháy Lớn/Có cháy, 0: Cháy Nhỏ/Không cháy)
# Sử dụng 0.0 để phân biệt có cháy và không cháy.
data['is_large_fire'] = np.where(data['area'] > 0, 1, 0)
# Hoặc nếu muốn phân loại Cháy Lớn/Cháy Nhỏ:
# data['is_large_fire'] = np.where(data['area'] > area_median, 1, 0)


# Định nghĩa lại X và y
y = data['is_large_fire']  # Biến mục tiêu phân loại mới
X = data.drop(['area', 'is_large_fire'], axis=1) # Loại bỏ 'area' và biến mục tiêu mới

print(f"Dataset loaded. Number of unique classes in target (0/1): {np.unique(y)}")
print(f"Class distribution:\n{y.value_counts()}")


# --- 3. Splitting Data ---
X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.20, 
    random_state=42, 
    # stratify=y bây giờ hoạt động vì các lớp (0 và 1) đã có đủ mẫu.
    stratify=y 
)

# --- 4. Random Forest Model Training ---
rf_classifier = RandomForestClassifier(
    n_estimators=100, 
    oob_score=True, 
    random_state=42,
    class_weight='balanced' # Thường hữu ích nếu các lớp 0/1 không cân bằng
)

print("\n--- Training Random Forest Classifier ---")
rf_classifier.fit(X_train, y_train)

# --- 5. Model Evaluation and Prediction ---
# Calculate and print OOB accuracy
oob_accuracy = rf_classifier.oob_score_
print("--- Model Performance Metrics (Random Forest) ---")
print("OOB Accuracy (Out-of-Bag Score): {:.4f}".format(oob_accuracy))

y_pred = rf_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Test Accuracy (Random Forest Ensemble): {:.4f}".format(accuracy))

print("\n--- Detailed Test Results ---")
print(f"Number of test data points: {len(X_test)}")

print('\n--- Classification Report ---')
print("Note: '0' corresponds to 'No Fire/Small Fire', '1' corresponds to 'Fire Occurred/Large Fire'.")
print(classification_report(y_test, y_pred, zero_division=0))

# --- 6. Feature Importance Visualization ---
feature_importance = rf_classifier.feature_importances_

importance_df = pd.DataFrame(
    {'Feature': X.columns, 'Importance': feature_importance}
)

importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("\n--- Feature Importance ---")
print(importance_df)

plt.figure(figsize=(10, 6))
importance_df.plot(
    kind="bar", 
    x="Feature", 
    y="Importance", 
    color="darkorange",
    legend=False,
    ax=plt.gca() 
)
plt.title("Random Forest Feature Importance for Forest Fire Prediction")
plt.ylabel("Importance Score")
plt.xlabel("Features")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()