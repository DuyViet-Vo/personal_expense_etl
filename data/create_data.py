import pandas as pd
import random
from datetime import datetime, timedelta

# Danh sách danh mục chi tiêu
categories = [
    "food",
    "transport",
    "entertainment",
    "shopping",
    "bills",
    "health",
    "others",
]

# Tạo danh sách dữ liệu
data = []
start_date = datetime(2025, 1, 1)
for i in range(1000):
    # Ngẫu nhiên ngày trong năm 2025 (từ 1/1 đến 31/12)
    days_in_year = random.randint(0, 364)  # 365 ngày trong năm 2025
    date = start_date + timedelta(days=days_in_year)
    category = random.choice(categories)  # Chọn ngẫu nhiên danh mục
    amount = round(
        random.uniform(5.0, 100.0), 2
    )  # Số tiền từ 5 đến 100, làm tròn 2 chữ số
    data.append([date.strftime("%Y-%m-%d"), category, amount])

# Tạo DataFrame và sắp xếp theo ngày
df = pd.DataFrame(data, columns=["date", "category", "amount"])
df = df.sort_values(by="date")  # Sắp xếp theo thứ tự ngày tăng dần

# Lưu vào file CSV
df.to_csv("expenses.csv", index=False)
print("Đã tạo file expenses.csv với 1000 dòng dữ liệu cho 12 tháng!")
