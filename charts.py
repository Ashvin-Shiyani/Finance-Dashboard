import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

CARD_BG = "#1a1a2e"
TEXT = "white"
MUTED = "#888888"


def dollar_formatter():
    def fmt(x, pos):
        if abs(x) >= 1_000_000:
            return f"${x/1_000_000:.1f}M"
        elif abs(x) >= 1_000:
            return f"${x/1_000:.0f}K"
        else:
            return f"${x:.0f}"
    return mticker.FuncFormatter(fmt)


def smart_label(val):
    if abs(val) >= 1_000_000:
        return f"${val/1_000_000:.1f}M"
    elif abs(val) >= 1_000:
        return f"${val/1_000:.0f}K"
    else:
        return f"${val:.0f}"


def apply_dark_style(ax):
    ax.set_facecolor(CARD_BG)
    ax.tick_params(colors=TEXT, labelsize=9)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.title.set_color(TEXT)
    for spine in ax.spines.values():
        spine.set_color("#2a2a3a")


def make_canvas(fig, parent):
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    plt.close(fig)
    return canvas


def no_data(ax, message="No data available"):
    ax.text(0.5, 0.5, message, ha="center", va="center",
            color=MUTED, fontsize=12, transform=ax.transAxes)
    ax.set_facecolor(CARD_BG)
    ax.axis("off")


def draw_pie_chart(parent, df, label_col, value_col, title):
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)

    if df.empty:
        no_data(ax)
    else:
        wedges, texts, autotexts = ax.pie(
            df[value_col],
            labels=df[label_col],
            autopct="%1.1f%%",
            colors=COLORS[:len(df)],
            pctdistance=0.85,
            wedgeprops={"linewidth": 2, "edgecolor": CARD_BG}
        )
        for text in texts:
            text.set_color(TEXT)
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_color(TEXT)
            autotext.set_fontsize(8)

    ax.set_title(title, color=TEXT, fontsize=13, pad=15)
    fig.tight_layout()
    return make_canvas(fig, parent)


def draw_bar_chart(parent, df, cat_col, num_col, title):
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor(CARD_BG)

    if df.empty:
        no_data(ax)
    else:
        x_labels = df[cat_col].astype(str)
        y_values = df[num_col]

        bars = ax.bar(range(len(x_labels)), y_values,
                      color=COLORS[:len(x_labels)], edgecolor="none")

        for bar, val in zip(bars, y_values):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(y_values) * 0.01,
                    smart_label(val),
                    ha="center", va="bottom", color=TEXT, fontsize=7)

        ax.set_xticks(range(len(x_labels)))
        ax.set_xticklabels(x_labels, rotation=45, ha="right", fontsize=8)
        ax.set_xlabel(cat_col.replace("_", " ").title(), color=TEXT)
        ax.set_ylabel("Amount ($)", color=TEXT)
        ax.yaxis.set_major_formatter(dollar_formatter())
        apply_dark_style(ax)

    ax.set_title(title, color=TEXT, fontsize=13, pad=15)
    fig.tight_layout()
    return make_canvas(fig, parent)


def draw_line_chart(parent, df, title):
    fig, ax = plt.subplots(figsize=(9, 3.5))
    fig.patch.set_facecolor(CARD_BG)

    if df.empty:
        no_data(ax)
    else:
        try:
            import sqlite3
            import pandas as pd
            conn = sqlite3.connect("finance.db")
            full_df = pd.read_sql_query("""
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

            if full_df.empty:
                no_data(ax, "No date or amount data found")
            else:
                full_df["month_dt"] = pd.to_datetime(
                    full_df["month"], format="%Y-%m")
                full_df = full_df.sort_values("month_dt")
                month_labels = full_df["month_dt"].dt.strftime("%b %Y")
                x = range(len(full_df))

                ax.plot(list(x), full_df["income"], color="#68A357",
                        linewidth=2, marker="o", markersize=4, label="Income")
                ax.plot(list(x), full_df["expenses"], color="#C97064",
                        linewidth=2, marker="o", markersize=4, label="Expenses")
                ax.plot(list(x), full_df["net"], color="#427AA1",
                        linewidth=2, marker="o", markersize=4, label="Net")

                ax.fill_between(list(x), full_df["income"],
                                color="#68A357", alpha=0.08)
                ax.fill_between(list(x), full_df["expenses"],
                                color="#C97064", alpha=0.08)

                ax.set_xticks(list(x))
                ax.set_xticklabels(month_labels, rotation=45,
                                   ha="right", fontsize=8)
                ax.set_xlabel("Month", color=TEXT)
                ax.set_ylabel("Amount ($)", color=TEXT)
                ax.yaxis.set_major_formatter(dollar_formatter())
                ax.legend(facecolor=CARD_BG, labelcolor=TEXT,
                          fontsize=9, loc="upper left")

        except Exception as e:
            no_data(ax, f"Error: {e}")

        apply_dark_style(ax)

    ax.set_title(title, color=TEXT, fontsize=13, pad=15)
    fig.tight_layout()
    return make_canvas(fig, parent)


def draw_histogram(parent, series, col, title):
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor(CARD_BG)

    if series.empty:
        no_data(ax)
    else:
        ax.hist(series.dropna(), bins=20,
                color="#427AA1", edgecolor=CARD_BG, alpha=0.85)
        ax.set_xlabel(col.replace("_", " ").title(), color=TEXT)
        ax.set_ylabel("Number of Transactions", color=TEXT)
        ax.xaxis.set_major_formatter(dollar_formatter())
        apply_dark_style(ax)

    ax.set_title(title, color=TEXT, fontsize=13, pad=15)
    fig.tight_layout()
    return make_canvas(fig, parent)


def draw_donut_chart(parent, df, col, title):
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)

    if df.empty or col not in df.columns:
        no_data(ax)
    else:
        counts = df[col].value_counts()
        wedges, texts, autotexts = ax.pie(
            counts.values,
            labels=[str(v).title() for v in counts.index],
            autopct="%1.1f%%",
            colors=COLORS[:len(counts)],
            pctdistance=0.75,
            wedgeprops={"linewidth": 2, "edgecolor": CARD_BG, "width": 0.5}
        )
        for text in texts:
            text.set_color(TEXT)
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_color(TEXT)
            autotext.set_fontsize(8)

    ax.set_title(title, color=TEXT, fontsize=13, pad=15)
    fig.tight_layout()
    return make_canvas(fig, parent)


def draw_stats_table(parent, df, title):
    fig, ax = plt.subplots(figsize=(9, 2))
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)
    ax.axis("off")

    if df.empty:
        no_data(ax)
    else:
        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            cellLoc="center",
            loc="center"
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.8)

        for (row, col), cell in table.get_celld().items():
            cell.set_facecolor("#1a1a2e" if row % 2 == 0 else "#16213e")
            cell.set_text_props(color=TEXT)
            cell.set_edgecolor("#2a2a3a")
            if row == 0:
                cell.set_facecolor("#064789")
                cell.set_text_props(color=TEXT, fontweight="bold")

    ax.set_title(title, color=TEXT, fontsize=13, pad=15)
    fig.tight_layout()
    return make_canvas(fig, parent)
