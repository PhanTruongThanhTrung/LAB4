import socket
import json
from pyspark.sql import SparkSession

def load_data(file_path):
    """
    Đọc dữ liệu từ file CSV bằng PySpark và chuyển thành JSON.

    Args:
        file_path (str): Đường dẫn tới file CSV.

    Returns:
        str: Dữ liệu JSON chứa đặc trưng và nhãn.
    """
    # Tạo SparkSession
    spark = SparkSession.builder.appName("Sender").getOrCreate()

    # Đọc file CSV
    data = spark.read.csv(file_path, header=True, inferSchema=True)

    # Kiểm tra dữ liệu
    if data.count() == 0:
        print("No data found in the CSV file!")
        return json.dumps({})  # Trả về JSON rỗng nếu không có dữ liệu

    # Chuyển đổi dữ liệu thành danh sách
    features = data.select("Junction").rdd.map(lambda row: row[0]).collect()
    labels = data.select("Vehicles").rdd.map(lambda row: row[0]).collect()

    # Đóng SparkSession
    spark.stop()

    # Trả về dữ liệu dưới dạng JSON
    return json.dumps({"features": features, "labels": labels})

def start_sender():
    host = '127.0.0.1'  # Địa chỉ IP của server
    port = 5000         # Cổng giao tiếp

    # Tạo socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Sender server is running on {host}:{port}...")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            # Đọc dữ liệu từ file CSV
            file_path = r'c:\du lieu\PTDLL\LAB\Lab4\data\train.csv'
            data = load_data(file_path)
            print(f"Data to send: {data}")  # In dữ liệu JSON trước khi gửi
            conn.sendall(data.encode('utf-8'))  # Gửi dữ liệu qua socket
            print("Data sent!")

if __name__ == '__main__':
    start_sender()