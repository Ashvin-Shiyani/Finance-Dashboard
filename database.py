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


def detect_columns(df):
    numeric_cols = []
    categorical_cols = []
    date_cols = []
    boolean_cols = []

    for col in df.columns:
        if df[col].dtype == object:
            try:
                pd.to_datetime(df[col], errors="raise")
                date_cols.append(col)
                continue
            except:
                pass

        unique_vals = df[col].dropna().unique()
        unique_lower = [str(v).strip().lower() for v in unique_vals]
        if set(unique_lower).issubset({"yes", "no", "true", "false", "1", "0"}):
            boolean_cols.append(col)
            continue

        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)
            continue

        if df[col].dtype == object:
            if df[col].nunique() <= 20:
                categorical_cols.append(col)

    return {
        "numeric": numeric_cols,
        "categorical": categorical_cols,
        "date": date_cols,
        "boolean": boolean_cols
    }
