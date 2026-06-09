# Nhập thư viện cần thiết cho mô hình Random Forest
from sklearn.ensemble import RandomForestClassifier
# Nhập thư viện cho các chỉ số đánh giá
from sklearn.metrics import accuracy_score, classification_report
# Import Matplotlib cho việc vẽ biểu đồ
import matplotlib.pyplot as plt
# Import pandas 
import pandas as pd 
# Import train_test_split 
from sklearn.model_selection import train_test_split 

# Tách tập dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.20, # 20% dữ liệu dùng để kiểm tra
    random_state=42, # Đặt seed để đảm bảo tính tái lập
    stratify=y # Đảm bảo tỷ lệ lớp trong tập train và test là như nhau
)

# --- Phần Khởi tạo Mô hình Random Forest ---
# Khởi tạo mô hình Random Forest
rf_classifier = RandomForestClassifier(
    n_estimators=100, # Số lượng cây quyết định là 100
    oob_score=True, # Kích hoạt tính toán điểm ngoài túi (OOB Score)
    random_state=42 # Đặt seed để đảm bảo tính tái lập
)

# --- Phần Huấn luyện và Đánh giá ---
# Huấn luyện mô hình Random Forest trên tập huấn luyện
rf_classifier.fit(X_train, y_train)

# Tính toán và in độ chính xác OOB (Out-of-Bag Score)
# OOB Score ước tính hiệu suất trên dữ liệu chưa thấy
oob_accuracy = rf_classifier.oob_score_
print("--- Model Performance Metrics (Random Forest) ---")
print("OOB Accuracy (Out-of-Bag Score): {:.4f}".format(oob_accuracy))
# Dự đoán nhãn trên tập kiểm tra
y_pred = rf_classifier.predict(X_test)
# Tính toán độ chính xác tổng thể trên tập kiểm tra
accuracy = accuracy_score(y_test, y_pred)
print("Test Accuracy (Random Forest Ensemble): {:.4f}".format(accuracy))

# In kết quả chi tiết của tập kiểm tra
print("\n--- Detailed Test Results ---")
print(f"Number of test data points: {len(X_test)}")
print("Ground Truth (Actual Labels):\n", y_test.reset_index(drop=True))
print("Predicted Labels (Model Output):", y_pred)
# In báo cáo phân loại chi tiết
print('\n--- Classification Report ---')
print("Note: '0' corresponds to 'no', '1' corresponds to 'yes' for the 'play' target.")
print(classification_report(y_test, y_pred, zero_division=0))


# --- Phần Phân tích Độ quan trọng của Đặc trưng (Feature Importance) ---
# Lấy độ quan trọng của từng đặc trưng từ mô hình đã huấn luyện
feature_importance = rf_classifier.feature_importances_
# Tạo DataFrame để hiển thị độ quan trọng một cách rõ ràng
importance_df = pd.DataFrame(
    {'Feature': X.columns, 'Importance': feature_importance}
)
# Sắp xếp các đặc trưng theo thứ tự độ quan trọng giảm dần
importance_df = importance_df.sort_values(by='Importance', ascending=False)
print("\n--- Feature Importance ---")
print(importance_df)
# --- Phần Trực quan hóa Độ quan trọng của Đặc trưng ---
# Khởi tạo figure cho biểu đồ
plt.figure(figsize=(10, 6))

# Vẽ biểu đồ thanh (Bar chart)
importance_df.plot(
    kind="bar", 
    x="Feature", 
    y="Importance", 
    color="lightblue",
    legend=False,
    ax=plt.gca() # Sử dụng axes hiện tại
)
plt.title("Random Forest Feature Importance for Weather Data")
plt.ylabel("Importance Score")
plt.xlabel("Features")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Hiển thị biểu đồ
plt.show()