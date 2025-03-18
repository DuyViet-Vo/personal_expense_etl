import psycopg2
from config.db_config import db_config

def load_to_postgres(df, table_name):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    
    # Tạo bảng nếu chưa tồn tại
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        date DATE,
        category VARCHAR(50),
        amount FLOAT,
        week INT,
        month INT
    );
    """
    cur.execute(create_table_query)
    
    # Chèn dữ liệu vào bảng
    for _, row in df.iterrows():
        insert_query = f"""
        INSERT INTO {table_name} (date, category, amount, week, month)
        VALUES (%s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, (row['date'], row['category'], row['amount'], row['week'], row['month']))
    
    conn.commit()
    cur.close()
    conn.close()

def save_reports(weekly_report, monthly_report):
    weekly_report.to_csv('reports/weekly_report.csv', index=False)
    monthly_report.to_csv('reports/monthly_report.csv', index=False)