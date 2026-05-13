import customtkinter as ctk
from tkinter import filedialog
import database as db
import charts

# app setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Auto Analytics Dashboard")
root.geometry("1100x750")
root.resizable(True, True)
root.configure(fg_color="#0f0f17")

sidebar = ctk.CTkFrame(root, width=220, corner_radius=0, fg_color="#111118")
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

ctk.CTkLabel(sidebar, text="Auto", font=("Arial", 20, "bold")).pack()
ctk.CTkLabel(sidebar, text="Analytics", font=("Arial", 12),
             text_color="#888888").pack(pady=(0, 30))

ctk.CTkFrame(sidebar, height=1, fg_color="#2a2a3a").pack(
    fill="x", padx=20, pady=10)


file_label = ctk.CTkLabel(sidebar, text="No file loaded",
                          font=("Arial", 10), text_color="#888888",
                          wraplength=180)
file_label.pack(pady=10, padx=10)

rows_label = ctk.CTkLabel(sidebar, text="",
                          font=("Arial", 10), text_color="#6affb0")
rows_label.pack()

cols_label = ctk.CTkLabel(sidebar, text="",
                          font=("Arial", 10), text_color="#aaaaaa")
cols_label.pack(pady=(0, 10))


def upload_csv():
    filepath = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv")]
    )
    if not filepath:
        return

    df, rows = db.load_csv_to_db(filepath)
    filename = filepath.split("/")[-1]
    file_label.configure(text=f"{filename}")
    rows_label.configure(text=f"{rows:,} rows loaded")
    cols_label.configure(text=f"{len(df.columns)} columns detected")

    show_dashboard(df)


ctk.CTkButton(
    sidebar,
    text="Upload CSV",
    font=("Arial", 13, "bold"),
    height=45,
    corner_radius=12,
    fg_color="#7c6aff",
    hover_color="#6a58e0",
    command=upload_csv
).pack(pady=15, padx=20, fill="x")

ctk.CTkFrame(sidebar, height=1, fg_color="#2a2a3a").pack(
    fill="x", padx=20, pady=10)

ctk.CTkLabel(sidebar, text="Detected Columns",
             font=("Arial", 10), text_color="#888888").pack(pady=(10, 5))

ctk.CTkLabel(sidebar, text="Upload a file to see columns",
             font=("Arial", 9), text_color="#555555",
             wraplength=180).pack(padx=10)


content_outer = ctk.CTkFrame(root, fg_color="#0f0f17")
content_outer.pack(side="right", fill="both", expand=True)

scrollable = ctk.CTkScrollableFrame(content_outer, fg_color="#0f0f17")
scrollable.pack(fill="both", expand=True, padx=15, pady=15)


welcome_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
welcome_frame.pack(fill="both", expand=True)

ctk.CTkLabel(welcome_frame, text="Auto Analytics Dashboard",
             font=("Arial", 28, "bold")).pack(pady=(60, 10))

ctk.CTkLabel(welcome_frame, text="Upload any CSV — charts generated automatically!",
             font=("Arial", 14), text_color="#888888").pack(pady=10)

ctk.CTkLabel(welcome_frame, text="Works with any data:",
             font=("Arial", 12), text_color="#888888").pack(pady=(20, 5))

for example in ["Credit card data", "Financial transactions",
                "Sales data", "HR data", "Banking data"]:
    ctk.CTkLabel(welcome_frame, text=f"   {example}",
                 font=("Arial", 12), text_color="#aaaaaa").pack()


dashboard_frame = ctk.CTkFrame(scrollable, fg_color="transparent")


def show_dashboard(df):
    welcome_frame.pack_forget()
    dashboard_frame.pack(fill="both", expand=True)

    for widget in dashboard_frame.winfo_children():
        widget.destroy()

    col_types = db.detect_columns(df)

    if col_types["categorical"]:
        row1 = ctk.CTkFrame(dashboard_frame, fg_color="transparent")
        row1.pack(fill="x", pady=10, padx=20)

        cat1 = col_types["categorical"][0]
        card1 = ctk.CTkFrame(row1, fg_color="#1a1a2e", corner_radius=15)
        card1.pack(side="left", fill="both", expand=True, padx=(0, 8))
        cat1_data = db.get_category_counts(cat1)
        charts.draw_pie_chart(card1, cat1_data, cat1, "count",
                              f"{cat1.replace('_',' ').title()} Breakdown")

        if len(col_types["categorical"]) > 1:
            cat2 = col_types["categorical"][1]
            card2 = ctk.CTkFrame(row1, fg_color="#1a1a2e", corner_radius=15)
            card2.pack(side="left", fill="both", expand=True, padx=(8, 0))
            cat2_data = db.get_category_counts(cat2)
            charts.draw_pie_chart(card2, cat2_data, cat2, "count",
                                  f"{cat2.replace('_',' ').title()} Breakdown")

    if col_types["date"] and col_types["numeric"]:
        try:
            line_card = ctk.CTkFrame(
                dashboard_frame, fg_color="#1a1a2e", corner_radius=15)
            line_card.pack(fill="x", pady=10, padx=20)
            cashflow_data = db.get_monthly_cashflow()
            charts.draw_line_chart(
                line_card, cashflow_data, "Cash Flow by Month")
        except:
            pass

    if col_types["numeric"]:
        row3 = ctk.CTkFrame(dashboard_frame, fg_color="transparent")
        row3.pack(fill="x", pady=10, padx=20)

        num_col = col_types["numeric"][0]

        hist_card = ctk.CTkFrame(row3, fg_color="#1a1a2e", corner_radius=15)
        hist_card.pack(side="left", fill="both", expand=True, padx=(0, 8))
        amount_data = db.get_numeric_distribution(num_col)
        charts.draw_histogram(hist_card, amount_data, num_col,
                              f"{num_col.replace('_',' ').title()} Distribution")

        if col_types["categorical"]:
            cat_col = col_types["categorical"][0]
            bar_card = ctk.CTkFrame(row3, fg_color="#1a1a2e", corner_radius=15)
            bar_card.pack(side="left", fill="both", expand=True, padx=(8, 0))
            bar_data = db.get_top_categories(cat_col, num_col)
            charts.draw_bar_chart(bar_card, bar_data, cat_col, "total",
                                  f"Top {cat_col.replace('_',' ').title()} by {num_col.replace('_',' ').title()}")

    if col_types["boolean"]:
        row4 = ctk.CTkFrame(dashboard_frame, fg_color="transparent")
        row4.pack(fill="x", pady=10, padx=20)
        df_full = db.get_dataframe()
        for bool_col in col_types["boolean"][:2]:
            donut_card = ctk.CTkFrame(
                row4, fg_color="#1a1a2e", corner_radius=15)
            donut_card.pack(side="left", fill="both", expand=True, padx=5)
            charts.draw_donut_chart(donut_card, df_full, bool_col,
                                    f"{bool_col.replace('_',' ').title()} Split")

    if col_types["numeric"]:
        table_card = ctk.CTkFrame(
            dashboard_frame, fg_color="#1a1a2e", corner_radius=15)
        table_card.pack(fill="x", pady=10, padx=20)
        num_col = col_types["numeric"][0]
        summary = db.get_numeric_summary(num_col)
        charts.draw_stats_table(table_card, summary,
                                f"{num_col.replace('_',' ').title()} Summary")


db.init_db()
root.mainloop()
