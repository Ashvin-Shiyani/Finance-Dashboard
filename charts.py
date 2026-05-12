import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

COLORS = ["#A9DDD6", "#7A8B99", "#91ADC2", "#9BA0BC", "#C1B8C8",
          "#DBF9F4", "#E6FDFF", "#D9D7DD", "#B07BAC", "#5F7367"]

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
