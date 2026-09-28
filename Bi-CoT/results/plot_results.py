"""Chart of the draft-reported HotpotQA ablation (reported_results.csv -> ../assets/ablation*.png).

Nothing is re-computed: the CSV transcribes the Bi-CoT manuscript's first results table.
Usage (from 02_Paper/Bi-CoT/results):  python plot_results.py   (needs matplotlib)
"""
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
THEMES = {  # validated categorical slots 1-2 + neutral inks, light and dark surfaces
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
                  grid="#e1e0d9", axis="#c3c2b7", s1="#2a78d6", s2="#eb6834"),
    "dark": dict(surface="#1a1a19", ink="#ffffff", ink2="#c3c2b7", muted="#898781",
                 grid="#2c2c2a", axis="#383835", s1="#3987e5", s2="#d95926"),
}
rows = list(csv.DictReader(open(os.path.join(HERE, "reported_results.csv"), encoding="utf-8")))
LABELS = ["Retrieve + QA\nbaseline", "+ self-aware\nforward CoT", "Full Bi-CoT\n(+ reverse verification)"]


def draw(t):
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    fig.subplots_adjust(left=0.1, right=0.98, top=0.8, bottom=0.2)
    width = 0.17
    for k, (key, name, color) in enumerate((("answer_em_pct", "EM", t["s1"]),
                                            ("answer_f1_pct", "F1", t["s2"]))):
        xs = [i + (k - 0.5) * (width + 0.025) for i in range(len(rows))]
        vals = [float(r[key]) for r in rows]
        ax.bar(xs, vals, width=width, color=color, edgecolor=t["surface"], linewidth=2, label=name, zorder=2)
        for x, v in zip(xs, vals):
            ax.text(x, v + 1.2, f"{v:.2f}", ha="center", va="bottom", fontsize=9, color=t["ink2"])
    ax.set_xticks(range(len(rows)))
    ax.set_xticklabels(LABELS, fontsize=9, color=t["ink2"])
    ax.set_ylim(0, 65)
    ax.set_ylabel("answer score (%)", color=t["ink2"])
    ax.set_facecolor(t["surface"])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(t["axis"])
    ax.tick_params(colors=t["muted"], labelcolor=t["ink2"], labelsize=9)
    ax.grid(axis="y", color=t["grid"], linewidth=0.8)
    ax.set_axisbelow(True)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=9, ncol=2)
    for txt in leg.get_texts():
        txt.set_color(t["ink2"])
    fig.text(0.1, 0.93, "Each stage adds answer accuracy", fontsize=11.5, color=t["ink"])
    fig.text(0.1, 0.865, "HotpotQA full wiki · answer EM / F1 · draft-reported, not re-run",
             fontsize=8.5, color=t["ink2"])
    return fig


if __name__ == "__main__":
    os.makedirs(ASSETS, exist_ok=True)
    for mode, suffix in (("light", ""), ("dark", "_dark")):
        t = THEMES[mode]
        fig = draw(t)
        fig.patch.set_facecolor(t["surface"])
        out = os.path.join(ASSETS, f"ablation{suffix}.png")
        fig.savefig(out, dpi=170, facecolor=t["surface"])
        plt.close(fig)
        print(out)
