import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns # Thêm thư viện để vẽ Confusion Matrix

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import plot_tree, DecisionTreeClassifier # Thêm plot_tree và DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Thiết lập chế độ hiển thị cho pandas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# --- 1. Data Loading and Preprocessing ---
file_path = '../Data/winequality-white.csv'

try:
    # Đọc dữ liệu Wine Quality White, separator là ';'
    data = pd.read_csv(file_path, sep=';') 
except FileNotFoundError:
    print(f"Error: File not found at {file_path}. Please check the path.")
    exit()

if data.empty:
    print("Error: DataFrame is empty after loading.")
    exit()

# Mã hóa các cột phân loại (Giữ lại cho tính tổng quát, mặc dù dữ liệu này không có cột object)
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

# --- 2. Huấn luyện Mô hình Random Forest (RF) ---
rf_classifier = RandomForestClassifier(
    n_estimators=100, 
    oob_score=True,        # BẬT TÍNH NĂNG OOB
    random_state=42,
    class_weight='balanced',
    max_features='sqrt'    # Mặc định của Scikit-learn, làm rõ Subspace Sampling
)

print("="*80)
print("             💎 RANDOM FOREST (WINE QUALITY WHITE) ANALYSIS 💎")
print("="*80)

rf_classifier.fit(X_train, y_train)

# --- 3. PHÂN TÍCH ĐẶC TRƯNG VÀ ƯU ĐIỂM CỦA RANDOM FOREST ---

## A. OOB Error (Ưu điểm của Bagging)
oob_accuracy = rf_classifier.oob_score_
print("--- 🔬 PHÂN TÍCH OOB ERROR (OUT-OF-BAG) ---")
print("Ưu điểm: OOB Score cho phép đánh giá hiệu suất mô hình mà KHÔNG cần tập validation riêng biệt.")
print("OOB Accuracy (Ước tính lỗi nội tại): {:.4f}".format(oob_accuracy))

y_pred_rf = rf_classifier.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)

print("Test Accuracy (Độ chính xác trên tập kiểm tra): {:.4f}".format(accuracy_rf))
print("------------------------------------------------------------------")

## B. Tính ngẫu nhiên (Subspace Sampling) và Feature Importance
feature_importance = rf_classifier.feature_importances_

importance_df = pd.DataFrame(
    {'Feature': X.columns, 'Importance': feature_importance}
)

importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("\n--- 💡 FEATURE IMPORTANCE (Làm rõ Subspace Sampling) ---")
print("RF chọn ngẫu nhiên các đặc trưng tại mỗi lần tách (split), giúp giảm tương quan giữa các cây.")
print("Feature Importance cho thấy các yếu tố quan trọng nhất đối với kết quả dự đoán chất lượng rượu:")
print(importance_df.to_markdown(index=False))

# Trực quan hóa Feature Importance (Cập nhật tiêu đề)
plt.figure(figsize=(10, 6))
importance_df.plot(
    kind="bar", 
    x="Feature", 
    y="Importance", 
    color="darkorange",
    legend=False,
    ax=plt.gca() 
)
plt.title("Random Forest Feature Importance for White Wine Quality Prediction")
plt.ylabel("Importance Score")
plt.xlabel("Features")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show() 


# --- 4. TRỰC QUAN HÓA CƠ CHẾ VÀ SO SÁNH ---

## A. Trực quan hóa Cây Đơn lẻ (Minh họa Cơ chế Bagging)
print("\n--- 🌲 TRỰC QUAN HÓA CÂY ĐƠN LẺ (Minh họa cơ chế Bagging) ---")
print("Mỗi cây được huấn luyện độc lập trên một tập mẫu con (bootstrap sample) của dữ liệu.")
print("Vẽ cây đầu tiên (chỉ 3 cấp) để minh họa cơ chế quyết định của một thành viên trong rừng:")

plt.figure(figsize=(20, 10))
single_tree = rf_classifier.estimators_[0] # Lấy cây đầu tiên
plot_tree(
    single_tree, 
    feature_names=X.columns.tolist(), 
    class_names=[str(c) for c in rf_classifier.classes_], 
    filled=True, 
    rounded=True, 
    max_depth=3 # Giới hạn độ sâu để dễ nhìn
)
plt.title("Visualizing One Decision Tree from the Random Forest (Max Depth 3)")
plt.show()


## B. So sánh với Decision Tree Đơn lẻ (Ưu điểm Chống Overfitting)
dt_classifier = DecisionTreeClassifier(random_state=42)
dt_classifier.fit(X_train, y_train)

y_pred_dt = dt_classifier.predict(X_test)
accuracy_dt = accuracy_score(y_test, y_pred_dt)

print("\n--- 🆚 SO SÁNH VỚI BASELINE: DECISION TREE ---")
print("Decision Tree có xu hướng Overfitting cao.")
print(f"Test Accuracy (Single Decision Tree): {accuracy_dt:.4f}")

# Tạo bảng so sánh
comparison_data = {
    'Model': ['Random Forest', 'Decision Tree'],
    'Accuracy': [accuracy_rf, accuracy_dt]
}
comparison_df = pd.DataFrame(comparison_data)

plt.figure(figsize=(8, 5))
sns.barplot(x='Model', y='Accuracy', data=comparison_df, palette=['lightgreen', 'skyblue'])
plt.title('Accuracy Comparison: Random Forest vs. Decision Tree')
plt.ylim(0.5, 0.7)
plt.ylabel('Test Accuracy')
plt.show()


## C. Trực quan hóa Ma trận Nhầm lẫn (Bổ sung đánh giá)
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
plt.title('Confusion Matrix for Random Forest (White Wine Quality)')
plt.ylabel('Actual Quality')
plt.xlabel('Predicted Quality')
plt.show()