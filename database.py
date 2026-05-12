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


def get_category_counts(col):
    conn = sql.connect(db_name)
    result = pd.read_sql_query(f"""
        SELECT "{col}", COUNT(*) as count
        FROM data
        GROUP BY "{col}"
        ORDER BY count DESC
    """, conn)
    conn.close()
    return result


def get_top_categories(cat_col, num_col):
    conn = sql.connect(db_name)
    result = pd.read_sql_query(f"""
        SELECT "{cat_col}", ROUND(SUM("{num_col}"), 2) as total
        FROM data
        GROUP BY "{cat_col}"
        ORDER BY total DESC
        LIMIT 10
    """, conn)
    conn.close()
    return result


def get_numeric_summary(col):
    conn = sql.connect(db_name)
    result = pd.read_sql_query(f"""
        SELECT
            COUNT("{col}") as count,
            ROUND(AVG("{col}"), 2) as average,
            ROUND(MIN("{col}"), 2) as minimum,
            ROUND(MAX("{col}"), 2) as maximum,
            ROUND(SUM("{col}"), 2) as total
        FROM data
    """, conn)
    conn.close()
    return result


def get_date_trend(date_col, value_col):
    conn = sql.connect(db_name)
    df = pd.read_sql_query("SELECT * FROM data", conn)
    conn.close()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])
    df["month"] = df[date_col].dt.strftime("%Y-%m")
    return df.groupby("month")[value_col].sum().reset_index()


def get_monthly_cashflow():
    conn = sql.connect(db_name)
    result = pd.read_sql_query("""
        SELECT
            strftime('%Y-%m', date) as month,
            SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as expenses,
            SUM(amount) as net
        FROM data
        GROUP BY month
        ORDER BY month
    """, conn)
    conn.close()
    return result


def get_numeric_distribution(col):
    conn = sql.connect(db_name)
    df = pd.read_sql_query(f'SELECT "{col}" FROM data', conn)
    conn.close()
    return df[col].dropna()
