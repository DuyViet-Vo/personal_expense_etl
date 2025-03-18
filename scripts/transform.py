import pandas as pd

def transform_data(df):
    # Đảm bảo cột 'date' ở định dạng datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Thêm cột tuần và tháng
    df['week'] = df['date'].dt.isocalendar().week
    df['month'] = df['date'].dt.month
    
    # Làm sạch dữ liệu: loại bỏ giá trị null ở cột 'amount'
    df = df.dropna(subset=['amount'])
    
    # Chuẩn hóa cột 'category' (nếu có)
    df['category'] = df['category'].str.lower().str.strip()
    
    return df

def generate_reports(df):
    # Báo cáo hàng tuần
    weekly_report = df.groupby(['week', 'category'])['amount'].sum().reset_index()
    # Báo cáo hàng tháng
    monthly_report = df.groupby(['month', 'category'])['amount'].sum().reset_index()
    
    return weekly_report, monthly_report