"""Charts of the numbers reported in the FTF-VTG result notes (see ../../results/).

Nothing is re-computed here: the CSVs are transcriptions of the paper's result notes.
Usage (from 02_Paper/FTFVTG/code):  python scripts/plot_reported_results.py
Writes ../assets/results_comparison(.png|_dark.png) and ../assets/theta_sensitivity(.png|_dark.png)
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # 02_Paper/FTFVTG
RESULTS = os.path.join(ROOT, "results")
ASSETS = os.path.join(ROOT, "assets")
sys.path.insert(0, HERE)
from _viz import plt, render_both, style_axes  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

rows = list(csv.DictReader(open(os.path.join(RESULTS, "reported_results.csv"), encoding="utf-8")))
LABELS = {"Off-the-shelf (Diwan et al. 2022)": "Off-the-shelf",
          "TFVTG without LLM stage (Zheng et al. 2024)": "TFVTG (no LLM)",
          "FTF-VTG (ours)": "FTF-VTG (ours)",
          "TA-STVG (trained reference)": "TA-STVG (trained)"}
names = [LABELS[r["method"]] for r in rows]
PANELS = [("didemo_r1_iou0.5_pct", "DiDeMo · R@1, IoU ≥ 0.5 (%)  ↑", "{:.2f}"),
          ("vidstg_miou_pct", "VidSTG · mIoU (%)  ↑", "{:.2f}"),
          ("gpu_memory_mib", "GPU memory (MiB)  ↓", "{:,.0f}")]


def draw_results(th):
    fig, axes = plt.subplots(1, 3, figsize=(9, 2.9), sharey=True)
    fig.subplots_adjust(left=0.16, right=0.975, top=0.83, bottom=0.08, wspace=0.28)
    ypos = list(range(len(rows)))[::-1]
    for ax, (key, title, fmt) in zip(axes, PANELS):
        vals = [float(r[key]) if r[key] else None for r in rows]
        vmax = max(v for v in vals if v is not None)
        for y, name, v in zip(ypos, names, vals):
            if v is None:
                ax.text(0, y, " not reported", va="center", ha="left", fontsize=9, color=th["muted"])
                continue
            ours = name.startswith("FTF-VTG")
            ax.barh(y, v, height=0.52, color=th["s1"] if ours else th["deemph"], edgecolor="none")
            ax.text(v + vmax * 0.02, y, fmt.format(v), va="center", ha="left", fontsize=9.5,
                    color=th["ink"] if ours else th["ink2"], fontweight="bold" if ours else "normal")
        ax.set_xlim(0, vmax * 1.32)
        ax.set_title(title, loc="left", fontsize=10.5, color=th["ink"], pad=6)
        style_axes(ax, th, grid_axis="x")
        ax.tick_params(axis="x", labelsize=8)
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
        ax.set_yticks(ypos)
        ax.set_yticklabels(names, fontsize=9.5)
    return fig


theta = list(csv.DictReader(open(os.path.join(RESULTS, "vidstg_theta_sweep.csv"), encoding="utf-8")))
tx = [float(r["theta_high"]) * 1e3 for r in theta]
ty = [float(r["vidstg_miou_pct"]) for r in theta]


def draw_theta(th):
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    fig.subplots_adjust(left=0.12, right=0.97, top=0.84, bottom=0.17)
    ax.plot(tx, ty, color=th["s1"], lw=2, solid_joinstyle="round", solid_capstyle="round", zorder=2)
    ax.scatter(tx, ty, s=22, color=th["s1"], edgecolors=th["surface"], linewidths=1.2, zorder=3)
    i = ty.index(max(ty))
    ax.scatter([tx[i]], [ty[i]], s=70, color=th["s1"], edgecolors=th["surface"], linewidths=2, zorder=4)
    ax.annotate(f"θ_high = {tx[i] / 1e3:g} → {ty[i]:.2f}\n(plateau ≥ 38.4 for θ_high 0.5–2.5 ×10⁻³)",
                (tx[i], ty[i]), xytext=(0.9, 13), textcoords="data", fontsize=9, color=th["ink"],
                va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color=th["muted"], lw=0.8, shrinkA=2, shrinkB=5))
    ax.set_xlabel("θ_high (×10⁻³)")
    ax.set_ylabel("VidSTG mIoU (%)")
    ax.set_ylim(0, 45)
    style_axes(ax, th, grid_axis="y")
    fig.text(0.12, 0.935, "Sensitivity to the boundary threshold θ_high", fontsize=11.5, color=th["ink"])
    fig.text(0.12, 0.875, "VidSTG mIoU from the result notes · λ = 0.9, α = 0.05 · same data as the reported score",
             fontsize=8.5, color=th["ink2"])
    return fig


if __name__ == "__main__":
    os.makedirs(ASSETS, exist_ok=True)
    print(render_both(draw_results, os.path.join(ASSETS, "results_comparison"), dpi=170))
    print(render_both(draw_theta, os.path.join(ASSETS, "theta_sensitivity"), dpi=170))
