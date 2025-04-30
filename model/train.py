import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_model(features, labels):
    """
    Huấn luyện mô hình RandomForestClassifier với dữ liệu đầu vào.

    Args:
        features (DataFrame): Đặc trưng (features).
        labels (Series): Nhãn (labels).

    Returns:
        float: Độ chính xác (accuracy) của mô hình trên tập kiểm tra.
    """
    # Chia dữ liệu thành tập huấn luyện và kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # Huấn luyện mô hình
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Dự đoán và đánh giá
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return accuracy