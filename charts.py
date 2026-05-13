import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

COLORS = ["#C97064", "#BCA371", "#A6B07E", "#68A357", "#32965D",
          "#064789", "#427AA1", "#A31F94", "#679436", "#A5BE00"]

CARD_BG = "#1a1a2e"
TEXT = "white"


def draw_pie_chart(parent, df):
    """
    Takes a dataframe with department and count columns
    Draws a pie chart showing each department's share
    """
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)

    wedges, texts, autotexts = ax.pie(
        df["count"],
        labels=df["department"],
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

    ax.set_title("Transactions by Department",
                 color=TEXT, fontsize=13, pad=15)

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    plt.close(fig)


def draw_bar_chart(parent, df, cat_col, num_col, title):
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)

    x_labels = df[cat_col].astype(str)
    y_values = df[num_col]

    bars = ax.bar(range(len(x_labels)), y_values,
                  color=COLORS[:len(x_labels)], edgecolor="none")

    for bar, val in zip(bars, y_values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(y_values) * 0.01,
                f"${val:,.0f}",
                ha="center", va="bottom", color=TEXT, fontsize=7)

    ax.set_xticks(range(len(x_labels)))
    ax.set_xticklabels(x_labels, rotation=45, ha="right", fontsize=8)
    ax.set_xlabel(cat_col.replace("_", " ").title(), color=TEXT)
    ax.set_ylabel("Amount ($)", color=TEXT)
    ax.tick_params(colors=TEXT)
    ax.title.set_color(TEXT)
    for spine in ax.spines.values():
        spine.set_color("#2a2a3a")

    ax.set_title(title, color=TEXT, fontsize=13, pad=15)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    plt.close(fig)


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


def draw_line_chart(parent, df, title):
    fig, ax = plt.subplots(figsize=(9, 3.5))
    fig.patch.set_facecolor(CARD_BG)

    if df.empty:
        ax.text(0.5, 0.5, "No data", ha="center",
                va="center", color=TEXT, fontsize=12)
    else:
        x = range(len(df))

        ax.plot(list(x), df["income"], color="#68A357",
                linewidth=2, marker="o", markersize=4, label="Income")
        ax.plot(list(x), df["expenses"], color="#C97064",
                linewidth=2, marker="o", markersize=4, label="Expenses")
        ax.plot(list(x), df["net"], color="#427AA1",
                linewidth=2, marker="o", markersize=4, label="Net")

        ax.fill_between(list(x), df["income"], color="#68A357", alpha=0.08)
        ax.fill_between(list(x), df["expenses"], color="#C97064", alpha=0.08)

        ax.set_xticks(list(x))
        ax.set_xticklabels(df["month"], rotation=45, ha="right", fontsize=8)
        ax.set_xlabel("Month", color=TEXT)
        ax.set_ylabel("Amount ($)", color=TEXT)
        ax.legend(facecolor=CARD_BG, labelcolor=TEXT, fontsize=9)

    ax.set_title(title, color=TEXT, fontsize=13, pad=15)
    apply_dark_style(ax)
    fig.tight_layout()
    return make_canvas(fig, parent)


def draw_histogram(parent, series, col, title):
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor(CARD_BG)

    ax.hist(series.dropna(), bins=20,
            color="#427AA1", edgecolor=CARD_BG, alpha=0.85)
    ax.set_xlabel(col.replace("_", " ").title(), color=TEXT)
    ax.set_ylabel("Number of Transactions", color=TEXT)
    ax.set_title(title, color=TEXT, fontsize=13, pad=15)
    apply_dark_style(ax)
    fig.tight_layout()
    return make_canvas(fig, parent)


def draw_donut_chart(parent, df, col, title):
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)

    counts = df[col].value_counts()

    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=[str(v).title() for v in counts.index],
        autopct="%1.1f%%",
        colors=["#68A357", "#C97064"],
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
        ax.text(0.5, 0.5, "No data", ha="center",
                va="center", color=TEXT, fontsize=12)
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
                cell.set_facecolor("#427AA1")
                cell.set_text_props(color=TEXT, fontweight="bold")

    ax.set_title(title, color=TEXT, fontsize=13, pad=15)
    fig.tight_layout()
    return make_canvas(fig, parent)
