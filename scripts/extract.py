import pandas as pd

def extract_data(file_path):
    # Đọc dữ liệu từ file CSV (có thể thay bằng nguồn khác)
    df = pd.read_csv(file_path)
    return df