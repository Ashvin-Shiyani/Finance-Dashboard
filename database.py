import sqlite3 as sql
import pandas as pd

db_name = "finance.db"


def init_db():
    conn = sql.connect(db_name)
    conn.close()


def load_csv_to_db(filepath):
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    conn = sql.connect(db_name)
    df.to_sql("data", conn, if_exists="replace", index=False)
    conn.close()
    return df, len(df)


def get_department_counts():
    conn = sql.connect(db_name)
    result = pd.read_sql_query("""
        SELECT department, COUNT(*) as count
        FROM data
        GROUP BY department
        ORDER BY count DESC
    """, conn)
    conn.close()
    return result
