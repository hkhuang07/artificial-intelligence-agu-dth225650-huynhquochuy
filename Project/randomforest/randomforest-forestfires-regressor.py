import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

# *** SỬ DỤNG GIẢI THUẬT HỒI QUY ***
from sklearn.ensemble import RandomForestRegressor 
# *** CHỈ SỐ ĐÁNH GIÁ HỒI QUY ***
from sklearn.metrics import mean_squared_error, r2_score 

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

# --- 1. Tiền xử lý Dữ liệu ---
# Mã hóa các cột phân loại (tháng và ngày)
le = preprocessing.LabelEncoder()
for column_name in ['month', 'day']:
    if column_name in data.columns:
        data[column_name] = le.fit_transform(data[column_name])

# --- 2. Định nghĩa Đặc trưng và Mục tiêu (Hồi quy) ---

# Biến mục tiêu là 'area' (diện tích cháy - giá trị liên tục)
y = data['area'] 
X = data.drop('area', axis=1) # Loại bỏ 'area' khỏi các đặc trưng

print(f"Dataset loaded. Mục tiêu: 'area' (Regression).")
print(f"Số lượng đặc trưng: {len(X.columns)}")

# --- 3. Tách tập dữ liệu ---
X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.20, 
    random_state=42
    # Bỏ stratify vì đây là Hồi quy
)

# --- 4. Huấn luyện Mô hình Hồi quy Random Forest ---
rf_regressor = RandomForestRegressor(
    n_estimators=100, 
    oob_score=True, # Tính OOB Score (R-squared)
    random_state=42,
    # Thêm siêu tham số đặc trưng cho Hồi quy
    min_samples_leaf=1 
)

print("\n--- Training Random Forest Regressor ---")
rf_regressor.fit(X_train, y_train)

# --- 5. Đánh giá Mô hình Hồi quy ---

y_pred = rf_regressor.predict(X_test)

# 5.1. Chỉ số R-squared và OOB
# R2 (R-squared Score): Đo lường mức độ phù hợp của mô hình (càng gần 1 càng tốt)
r2 = r2_score(y_test, y_pred)
oob_r2_score = rf_regressor.oob_score_

# 5.2. Sai số
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse) # RMSE (Root Mean Squared Error): Càng gần 0 càng tốt

print("\n--- Model Performance Metrics (Random Forest Regressor) ---")
print(f"OOB R-squared Score (Đánh giá nội tại): {oob_r2_score:.4f}")
print(f"Test R-squared (R2 Score): {r2:.4f}")
print(f"Test Root Mean Squared Error (RMSE): {rmse:.4f}")

print("\n--- Detailed Test Results (First 5 Predictions) ---")
print(f"Number of test data points: {len(X_test)}")
results = pd.DataFrame({'Actual Area': y_test, 'Predicted Area': y_pred}).head()
print(results)

# --- 6. Feature Importance Visualization ---
feature_importance = rf_regressor.feature_importances_

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
    color="darkgreen",
    legend=False,
    ax=plt.gca() 
)
plt.title("Random Forest Feature Importance for Forest Fire Area Prediction (Regression)")
plt.ylabel("Importance Score")
plt.xlabel("Features")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()