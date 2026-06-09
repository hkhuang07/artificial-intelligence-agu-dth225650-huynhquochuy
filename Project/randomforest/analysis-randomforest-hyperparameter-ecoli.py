import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time # Thêm thư viện để đo thời gian

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Thiết lập chế độ hiển thị cho pandas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# --- 1. Data Loading and Preprocessing ---
file_path = '../Data/ecoli.data'

try:
    # Đọc dữ liệu Ecoli, không có header, sử dụng khoảng trắng làm separator
    data = pd.read_csv(file_path, sep='\s+', header=None, engine='python') 
except FileNotFoundError:
    print(f"Error: File not found at {file_path}. Please check the path.")
    exit()

if data.empty:
    print("Error: DataFrame is empty after loading.")
    exit()

# Dữ liệu Ecoli có cột đầu tiên (tên) và cột cuối cùng (mục tiêu) là dạng object/string.
le = preprocessing.LabelEncoder()

# Cột 0 là tên, cột n-1 là mục tiêu
data.iloc[:, 0] = le.fit_transform(data.iloc[:, 0])
# Cột cuối cùng (mục tiêu)
data.iloc[:, -1] = le.fit_transform(data.iloc[:, -1])


# Định nghĩa X và y
n = len(data.columns) 
y = data.iloc[:,-1] # Biến mục tiêu (location) đã được mã hóa
X = data.iloc[:, 0:n-1] # Tất cả các cột trừ cột mục tiêu

# Ép kiểu rõ ràng biến mục tiêu y thành integer (classification target)
y = y.astype(np.int64) 
# Ép kiểu rõ ràng các đặc trưng X thành float (các giá trị là float)
X = X.astype(np.float64) 

# Tách tập dữ liệu
X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.20, 
    random_state=42, 
    stratify=y 
)

# --- 2. Huấn luyện Mô hình Random Forest (RF) Ban đầu ---
rf_classifier = RandomForestClassifier(
    n_estimators=100, 
    oob_score=True, 
    random_state=42,
    class_weight='balanced' # Hỗ trợ cân bằng lớp (Ecoli có phân bố lớp không đều)
)

print("="*80)
print("              RANDOM FOREST (ECOLI PROTEIN LOCALIZATION) ANALYSIS ")
print("="*80)

# Đo thời gian huấn luyện RF
start_time_rf = time.time()
rf_classifier.fit(X_train, y_train)
end_time_rf = time.time()
training_time_rf = end_time_rf - start_time_rf

# Đánh giá RF
oob_accuracy = rf_classifier.oob_score_
y_pred_rf = rf_classifier.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)

print("--- 🔬 KẾT QUẢ CƠ SỞ (RANDOM FOREST) ---")
print(f"Thời gian huấn luyện: {training_time_rf:.4f} giây")
print(f"OOB Accuracy (Ưu điểm của Bagging): {oob_accuracy:.4f}")
print(f"Test Accuracy: {accuracy_rf:.4f}")

print('\n--- Classification Report ---')
print("Note: Phân loại vị trí Protein (E.coli). Các nhãn số là các lớp đã được mã hóa.")
print(classification_report(y_test, y_pred_rf, zero_division=0))

# --- 3. PHÂN TÍCH CHUYÊN SÂU: ĐỘ MẠNH MẼ VÀ NHƯỢC ĐIỂM ---

## A. Độ Sâu (Depth) và Quá khớp (Overfitting) - So sánh DT vs RF
dt_overfit = DecisionTreeClassifier(random_state=42) # Mặc định max_depth=None (sâu tối đa)

# Đo thời gian huấn luyện DT
start_time_dt = time.time()
dt_overfit.fit(X_train, y_train)
end_time_dt = time.time()
training_time_dt = end_time_dt - start_time_dt

# Đánh giá DT
y_pred_train_dt = dt_overfit.predict(X_train)
y_pred_test_dt = dt_overfit.predict(X_test)
train_accuracy_dt = accuracy_score(y_train, y_pred_train_dt)
test_accuracy_dt = accuracy_score(y_test, y_pred_test_dt)

print("\n--- ✨ CHỐNG QUÁ KHỚP (OVERFITTING) ---")
print("RF giúp giảm phương sai, chống quá khớp tốt hơn DT.")
print(f"DT (sâu tối đa) - Train Accuracy: {train_accuracy_dt:.4f} (Xu hướng Overfitting)")
print(f"DT (sâu tối đa) - Test Accuracy:  {test_accuracy_dt:.4f}")
print(f"RF (n=100) - Test Accuracy: {accuracy_rf:.4f} (Duy trì hiệu suất kiểm tra tốt)")

# Bảng so sánh
comparison_df_overfit = pd.DataFrame({
    'Model': ['Decision Tree (Overfit)', 'Random Forest'],
    'Train Accuracy': [train_accuracy_dt, accuracy_score(y_train, rf_classifier.predict(X_train))],
    'Test Accuracy': [test_accuracy_dt, accuracy_rf],
    'Training Time (s)': [training_time_dt, training_time_rf]
})
print("\n--- BẢNG SO SÁNH HIỆU SUẤT VÀ TỐC ĐỘ ---")
print(comparison_df_overfit.to_markdown(index=False))


## B. Ảnh hưởng của n_estimators (Số lượng cây)
estimators = [10, 50, 100, 200, 500]
oob_scores = []
test_accuracies = []

for n in estimators:
    rf = RandomForestClassifier(n_estimators=n, oob_score=True, random_state=42, class_weight='balanced')
    # Huấn luyện mô hình
    rf.fit(X_train, y_train)
    oob_scores.append(rf.oob_score_)
    test_accuracies.append(accuracy_score(y_test, rf.predict(X_test)))

plt.figure(figsize=(10, 6))
plt.plot(estimators, oob_scores, label='OOB Score', marker='o')
plt.plot(estimators, test_accuracies, label='Test Accuracy', marker='o')
plt.title('Ảnh hưởng của Số lượng cây (n_estimators) lên Độ chính xác')
plt.xlabel('Số lượng cây (n_estimators)')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True, linestyle='--')
plt.show()



## C. Ảnh hưởng của max_features (Tính ngẫu nhiên về đặc trưng)
# Làm rõ Subspace Sampling
max_features_list = [1.0, 'sqrt', 'log2']
accuracy_max_features = []

for mf in max_features_list:
    rf = RandomForestClassifier(n_estimators=100, oob_score=False, random_state=42, max_features=mf, class_weight='balanced')
    # Huấn luyện mô hình
    rf.fit(X_train, y_train)
    accuracy_max_features.append(accuracy_score(y_test, rf.predict(X_test)))

plt.figure(figsize=(8, 5))
sns.barplot(x=['Full Features (Bagging)', 'sqrt (RF Default)', 'log2'], y=accuracy_max_features, palette='viridis')
plt.title('Ảnh hưởng của max_features (Subspace Sampling) lên Accuracy')
plt.xlabel('Cấu hình max_features')
plt.ylabel('Test Accuracy')
plt.show()


# --- 4. TRỰC QUAN HÓA CƠ CHẾ VÀ ĐÁNH GIÁ ---

## A. Trực quan hóa Cây Đơn lẻ (Minh họa Cơ chế Bagging)
print("\n---  TRỰC QUAN HÓA CÂY ĐƠN LẺ (Minh họa cơ chế Bagging) ---")
plt.figure(figsize=(20, 10))
single_tree = rf_classifier.estimators_[0] 
# Lấy tên cột để hiển thị rõ ràng
feature_names = X.columns.astype(str).tolist()

plot_tree(
    single_tree, 
    feature_names=feature_names, 
    class_names=[str(c) for c in rf_classifier.classes_], 
    filled=True, 
    rounded=True, 
    max_depth=3 
)
plt.title("Visualizing One Decision Tree from the Random Forest (Max Depth 3)")
plt.show()

## B. Trực quan hóa Ma trận Nhầm lẫn (Confusion Matrix)
print("\n--- 📊 MA TRẬN NHẦM LẪN (CONFUSION MATRIX) ---")
# RF Confusion Matrix
plt.figure(figsize=(10, 8))
sns.heatmap(
    confusion_matrix(y_test, y_pred_rf), 
    annot=True, 
    fmt='d', 
    cmap='Blues', 
    xticklabels=rf_classifier.classes_, 
    yticklabels=rf_classifier.classes_
)
plt.title('Confusion Matrix for Random Forest (Ecoli Data)')
plt.ylabel('Actual Label')
plt.xlabel('Predicted Label')
plt.show()

# DT Confusion Matrix
plt.figure(figsize=(10, 8))
sns.heatmap(
    confusion_matrix(y_test, y_pred_test_dt), 
    annot=True, 
    fmt='d', 
    cmap='Oranges', 
    xticklabels=dt_overfit.classes_, 
    yticklabels=dt_overfit.classes_
)
plt.title('Confusion Matrix for Decision Tree (Ecoli Data)')
plt.ylabel('Actual Label')
plt.xlabel('Predicted Label')
plt.show()
