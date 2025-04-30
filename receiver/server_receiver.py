import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.train import train_model
import socket
import json
import pandas as pd

def start_receiver():
    host = '127.0.0.1'  # Địa chỉ IP của server
    port = 5000         # Cổng giao tiếp

    # Tạo socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Connected to sender server at {host}:{port}...")

        # Nhận dữ liệu
        data = s.recv(1024 * 1024).decode('utf-8')  # Tăng kích thước buffer nếu cần
        print(f"Raw data received: {data}")  # In dữ liệu nhận được
        if not data:
            print("No data received!")
            return

        # Xử lý dữ liệu
        data = json.loads(data)
        features = pd.DataFrame(data['features'], columns=['Junction'])
        labels = pd.Series(data['labels'], name='Vehicles')

        # Huấn luyện mô hình
        accuracy = train_model(features, labels)
        print(f"Model trained with accuracy: {accuracy:.2f}")

if __name__ == '__main__':
    start_receiver()