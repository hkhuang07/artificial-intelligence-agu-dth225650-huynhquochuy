import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns # Thêm thư viện seaborn để vẽ Confusion Matrix

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree # Thêm DecisionTreeClassifier và plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# --- 1. Data Loading and Preprocessing ---
file_path = '../Data/winequality-red.csv'

try:
    data = pd.read_csv(file_path, sep=';') 
except FileNotFoundError:
    print(f"Error: File not found at {file_path}. Please check the path.")
    exit()

if data.empty:
    print("Error: DataFrame is empty after loading.")
    exit()

# Mã hóa các cột phân loại (nếu có, giữ lại cho tính tổng quát)
le = preprocessing.LabelEncoder()
for column_name in data.columns:
    if data[column_name].dtype == object:
        data[column_name] = le.fit_transform(data[column_name])

# Định nghĩa X và y
y = data['quality'] 
X = data.drop('quality', axis=1) 

# Tách tập dữ liệu
X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.20, 
    random_state=42, 
    stratify=y 
)

# --- 2. Huấn luyện Mô hình: Random Forest (RF) ---
rf_classifier = RandomForestClassifier(
    n_estimators=100, 
    oob_score=True, 
    random_state=42,
    class_weight='balanced' # Hỗ trợ cân bằng các lớp quality
)

rf_classifier.fit(X_train, y_train)

# --- 3. Huấn luyện Mô hình So sánh: Decision Tree (DT) ---
dt_classifier = DecisionTreeClassifier(
    max_depth=10, # Giới hạn độ sâu để tránh quá khớp
    random_state=42
)
dt_classifier.fit(X_train, y_train)


# --- 4. Đánh giá Mô hình RF ---
print("="*60)
print("             💎 RANDOM FOREST RESULTS 💎")
print("="*60)

# Tính toán OOB accuracy (Đặc tính của RF)
oob_accuracy = rf_classifier.oob_score_
print("--- Model Performance Metrics (Random Forest) ---")
print("OOB Accuracy (Out-of-Bag Score): {:.4f}".format(oob_accuracy))

y_pred_rf = rf_classifier.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)

print("Test Accuracy (Random Forest Ensemble): {:.4f}".format(accuracy_rf))

print('\n--- Classification Report (Random Forest) ---')
# Cập nhật ghi chú cho phù hợp với dữ liệu Wine Quality
print("Note: Classification is based on Wine Quality scores (e.g., 5, 6, 7).")
print(classification_report(y_test, y_pred_rf, zero_division=0))


# --- 5. So sánh với Decision Tree Đơn lẻ ---
y_pred_dt = dt_classifier.predict(X_test)
accuracy_dt = accuracy_score(y_test, y_pred_dt)

print("="*60)
print("             🌳 BASELINE: DECISION TREE RESULTS 🌳")
print("="*60)
print("Test Accuracy (Single Decision Tree): {:.4f}".format(accuracy_dt))
print('\n--- Classification Report (Decision Tree) ---')
print(classification_report(y_test, y_pred_dt, zero_division=0))

# Bảng so sánh
comparison_data = {
    'Model': ['Random Forest', 'Decision Tree'],
    'Accuracy': [accuracy_rf, accuracy_dt]
}
comparison_df = pd.DataFrame(comparison_data)
print("\n--- Model Comparison ---")
print(comparison_df.sort_values(by='Accuracy', ascending=False).to_markdown(index=False))


# --- 6. Trực quan hóa Đặc trưng quan trọng (Feature Importance) ---
feature_importance = rf_classifier.feature_importances_

importance_df = pd.DataFrame(
    {'Feature': X.columns, 'Importance': feature_importance}
)

importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("\n--- Random Forest Feature Importance ---")
print(importance_df)

plt.figure(figsize=(10, 6))
importance_df.plot(
    kind="bar", 
    x="Feature", 
    y="Importance", 
    color="darkred",
    legend=False,
    ax=plt.gca() 
)
# Cập nhật tiêu đề
plt.title("Random Forest Feature Importance for Red Wine Quality Prediction")
plt.ylabel("Importance Score")
plt.xlabel("Features")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show() 


# --- 7. Trực quan hóa Cơ chế và Ma trận Nhầm lẫn ---

### A. Trực quan hóa Cây Đơn lẻ (Minh họa cơ chế Bagging)
# Chỉ vẽ 3 cấp độ để cây dễ đọc
plt.figure(figsize=(20, 10))
# Trích xuất cây đầu tiên trong rừng
single_tree = rf_classifier.estimators_[0] 
plot_tree(
    single_tree, 
    feature_names=X.columns.tolist(), 
    class_names=[str(c) for c in rf_classifier.classes_], 
    filled=True, 
    rounded=True, 
    max_depth=3 
)
plt.title("Visualizing One Decision Tree from the Random Forest (Max Depth 3)")
plt.show()


### B. Trực quan hóa Ma trận Nhầm lẫn (Confusion Matrix)
cm = confusion_matrix(y_test, y_pred_rf)

plt.figure(figsize=(10, 8))
sns.heatmap(
    cm, 
    annot=True, 
    fmt='d', 
    cmap='Blues', 
    xticklabels=rf_classifier.classes_, 
    yticklabels=rf_classifier.classes_
)
plt.title('Confusion Matrix for Random Forest (Wine Quality)')
plt.ylabel('Actual Quality')
plt.xlabel('Predicted Quality')
plt.show()


