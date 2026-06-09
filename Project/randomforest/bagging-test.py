#4. Baggging Ensemble Learing Using Decision Tree
# Nhập thư viện cần thiết cho mô hình Ensemble (Bagging) và Cây Quyết Định
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import BaggingRegressor
from sklearn.tree import DecisionTreeClassifier
# Nhập các thư viện để đánh giá hiệu suất mô hình
from sklearn.metrics import accuracy_score, classification_report
    
# Khởi tạo bộ ước tính cơ sở (Base Estimator) là Cây Quyết Định
# random_state=42 để đảm bảo tính tái lập của quá trình huấn luyện
base_elf = DecisionTreeClassifier(random_state = 42)

# Khởi tạo mô hình Bagging Ensemble
# Tham số:
# - n_estimators=100: Số lượng cây quyết định sẽ được xây dựng
# - oob_score=True: Kích hoạt tính toán điểm ngoài túi (Out-of-Bag Score)
# - random_state=42: Đảm bảo tính tái lập
bg_elf = BaggingClassifier(base_elf, n_estimators=100, oob_score=True, random_state=42)
# (tùy chọn sử dụng Bagging không OOB)
# bg_elf = BaggingClassifier(base_elf, n_estimators=100, random_state=42)

# Huấn luyện mô hình Bagging trên tập dữ liệu huấn luyện (X_train, y_train)
bg_elf.fit(X_train,y_train)

# Tính toán và lưu trữ độ chính xác OOB
oob_accuracy = bg_elf.oob_score_
# In kết quả độ chính xác OOB
print("Accuracy of OOB (Out-of-Bag Score): {}".format(oob_accuracy))

# Dự đoán nhãn trên tập dữ liệu kiểm tra (X_test)
y_pred = bg_elf.predict(X_test)

# Đánh giá độ chính xác tổng thể bằng cách so sánh nhãn dự đoán và nhãn thực tế
accuracy = accuracy_score(y_test, y_pred)
# In kết quả độ chính xác của mô hình Ensemble trên tập kiểm tra
print("Accuracy (Bagging Ensemble): {:.4f}".format(accuracy))

# In kết quả chi tiết của tập kiểm tra
print("\n--- Detailed Test Results ---")
print(f"Number of test data points: {len(X_test)}")
# In nhãn thực tế của tập kiểm tra (reset_index(drop=True) để hiển thị sạch hơn)
print("Ground Truth (Actual Labels):\n", y_test.reset_index(drop=True))
# In nhãn dự đoán của mô hình
print("Predicted Labels (Model Output):", y_pred)

# In báo cáo phân loại chi tiết (Classification Report)
print('\n--- Classification Report ---')
print("Note: '0' corresponds to 'no', '1' corresponds to 'yes' for the 'play' target.")
# Sử dụng classification_report để in precision, recall, f1-score cho từng lớp
# zero_division=0 để tránh cảnh báo khi không có mẫu nào được dự đoán cho một lớp
print(classification_report(y_test, y_pred, zero_division=0))