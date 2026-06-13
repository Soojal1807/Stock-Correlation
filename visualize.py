#this is is a vibe-coded heatmap to understand co-relations between stock data we took out earlier.


import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import numpy as np

COLORS = {
    "bg":     "#0f1117",
    "panel":  "#1a1d27",
    "border": "#2a2d3a",
    "text":   "#e8e8f0",
    "muted":  "#8888aa",
}

def _style_ax(ax):
    ax.set_facecolor(COLORS["panel"])
    for spine in ax.spines.values():
        spine.set_edgecolor(COLORS["border"])
    ax.tick_params(colors=COLORS["muted"], labelsize=9)
    ax.xaxis.label.set_color(COLORS["muted"])
    ax.yaxis.label.set_color(COLORS["muted"])

def plot_correlation_heatmap(corr: pd.DataFrame, save_path: str = None):
    fig, ax = plt.subplots(figsize=(7, 6))
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["panel"])

    mask = np.zeros_like(corr.values, dtype=bool)
    mask[np.triu_indices_from(mask, k=1)] = True

    sns.heatmap(
        corr,
        ax=ax,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        vmin=-1, vmax=1,
        linewidths=0.5,
        linecolor=COLORS["bg"],
        annot_kws={"size": 11, "weight": "bold", "color": COLORS["bg"]},
        cbar_kws={"shrink": 0.75},
    )

    ax.set_title("Pairwise Correlation Matrix", color=COLORS["text"],
                 fontsize=13, fontweight="bold", pad=14)
    ax.tick_params(axis="x", rotation=0, labelsize=10, colors=COLORS["text"])
    ax.tick_params(axis="y", rotation=0, labelsize=10, colors=COLORS["text"])

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(colors=COLORS["muted"], labelsize=8)
    cbar.outline.set_edgecolor(COLORS["border"])

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig




def plot_cumulative_returns(returns: pd.DataFrame, save_path: str = None):
    cumulative = (1 + returns).cumprod()

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(COLORS["bg"])
    _style_ax(ax)

    palette = ["#7c6af7", "#44c9a2", "#f76c6c", "#f7b94e", "#6ec6f7"]
    for i, col in enumerate(cumulative.columns):
        ax.plot(cumulative.index, cumulative[col],
                label=col, color=palette[i], linewidth=1.6)

    ax.set_title("Cumulative Returns — Last 500 Days",
                 color=COLORS["text"], fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Growth of $1", color=COLORS["muted"], fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.1f}"))
    ax.legend(frameon=False, labelcolor=COLORS["text"], fontsize=9)
    ax.grid(axis="y", color=COLORS["border"], linewidth=0.5, alpha=0.6)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig





def plot_volatility_bar(returns: pd.DataFrame, save_path: str = None):
    ann_vol = returns.std() * np.sqrt(252) * 100

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor(COLORS["bg"])
    _style_ax(ax)

    palette = ["#7c6af7", "#44c9a2", "#f76c6c", "#f7b94e", "#6ec6f7"]
    bars = ax.bar(ann_vol.index, ann_vol.values, color=palette, width=0.5)

    for bar, val in zip(bars, ann_vol.values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f"{val:.1f}%", ha="center", va="bottom",
                color=COLORS["text"], fontsize=9, fontweight="bold")

    ax.set_title("Annualised Volatility", color=COLORS["text"],
                 fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Volatility (%)", color=COLORS["muted"], fontsize=9)
    ax.set_ylim(0, ann_vol.max() * 1.2)
    ax.grid(axis="y", color=COLORS["border"], linewidth=0.5, alpha=0.6)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig
