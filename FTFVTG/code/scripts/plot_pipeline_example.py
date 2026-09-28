"""Illustrate every FTF-VTG stage on the DiDeMo example bundled in ../examples.

Runs the maintained package functions (ftf_vtg.*) with the historical defaults of
ftf_vtg/src/model/FTF_VTG.py (kernel 7, sigma 1, min_seg_len 3, gap 10, alpha 0.5,
lambda 0.5) and theta_high = 0.0015, the VidSTG setting recorded in the result notes.
It checks that the step-by-step reconstruction equals FTF_VTG(...) before plotting.

This is an illustration on ONE example, not a benchmark result.

Usage (from 02_Paper/FTFVTG/code):  python scripts/plot_pipeline_example.py
Writes ../assets/hero.png, hero_dark.png, observation.png, observation_dark.png
"""
import glob
import json
import os
import sys

import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.dirname(HERE)
ASSETS = os.path.join(os.path.dirname(CODE), "assets")
sys.path[:0] = [CODE, HERE]

from ftf_vtg import FTF_VTG  # noqa: E402
from ftf_vtg.segment_detector import detect_event_segments_with_gradient  # noqa: E402
from ftf_vtg.segment_merger import generate_all_merge_candidates_by_gap  # noqa: E402
from ftf_vtg.segment_scorer import compute_segment_score  # noqa: E402
from ftf_vtg.src.utils.eval_metrics import compute_iou  # noqa: E402
from _viz import plt, render_both, style_axes  # noqa: E402

PARAMS = dict(kernel_size=7, sigma=1.0, theta_high=0.0015, theta_low_ratio=0.5,
              min_seg_len=3, alpha=0.5)
GAP, LAMBDA = 10, 0.5

# ------------------------------------------------------------------ compute
path = sorted(glob.glob(os.path.join(CODE, "examples", "vmr_DiDeMo_json", "*.json")))[0]
rec = json.load(open(path, encoding="utf-8"))
x = np.asarray(rec["similarities"], dtype=np.float32)
fps, total = rec["fps"], rec["total_frames"]
t = np.arange(len(x)) / fps

segments, grad, smoothed = detect_event_segments_with_gradient(torch.as_tensor(x), **PARAMS)
candidates = generate_all_merge_candidates_by_gap(segments, GAP)
scored = [(s, e, compute_segment_score(x, s, e, lambda_weight=LAMBDA)) for s, e in candidates]
best = max(scored, key=lambda c: c[2])
assert FTF_VTG(x, gap_threshold=GAP, lambda_weight=LAMBDA, **PARAMS) == (best[0], best[1])

# DiDeMo ground truth: 5-second bins; the historical adapter caps the last bin at the video end
gt_frames = [(int(a * 5 * fps), int(min((b + 1) * 5 * fps, total))) for a, b in rec["gt_times"]]
iou = max(compute_iou(best[0], best[1], s, e) for s, e in gt_frames)
b0, b1 = best[0] / fps, best[1] / fps
theta_low = PARAMS["theta_high"] * PARAMS["theta_low_ratio"]
print(f"query={rec['query']!r} segments={len(segments)} candidates={len(candidates)} "
      f"best={best[0]}-{best[1]} ({b0:.2f}-{b1:.2f} s) score={best[2]:.3f} IoU={iou:.2f}")


def gt_track(ax, th, y, h):
    """Annotation track: 5-15 s marked by 3 annotators, 5-10 s by 1."""
    ax.broken_barh([(5, 10)], (y, h), facecolors=th["deemph"], edgecolor="none", zorder=3)
    ax.text(15.3, y + h / 2, "annotated 5–15 s (3 of 4 annotators; 1 marks 5–10 s)",
            va="center", ha="left", fontsize=9, color=th["ink2"])


def pred_track(ax, th, y, h):
    ax.broken_barh([(b0, b1 - b0)], (y, h), facecolors=th["s2"], edgecolor="none", zorder=3)
    ax.text(b1 + 0.3, y + h / 2, f"FTF-VTG prediction {b0:.2f}–{b1:.2f} s  (IoU {iou:.2f})",
            va="center", ha="left", fontsize=9, color=th["ink2"])


def similarity_panel(ax, th, title):
    lo, hi = float(x.min()), float(x.max())
    span = hi - lo
    ax.axvspan(b0, b1, color=th["s2"], alpha=0.10, lw=0, zorder=0)
    ax.plot(t, x, color=th["muted"], lw=0.6, label="raw similarity (one value per frame)", zorder=1)
    ax.plot(t, smoothed, color=th["s1"], lw=1.6, label="Gaussian-smoothed", zorder=2)
    h = span * 0.07
    gt_track(ax, th, hi + span * 0.30, h)
    pred_track(ax, th, hi + span * 0.14, h)
    ax.set_ylim(lo - span * 0.05, hi + span * 0.42)
    ax.set_ylabel("cosine similarity")
    style_axes(ax, th)
    ax.set_title(title, loc="left", fontsize=11, color=th["ink"], pad=8)


# ------------------------------------------------------------------ figures
def draw_hero(th):
    fig, axes = plt.subplots(3, 1, figsize=(9, 7.4), sharex=True,
                             gridspec_kw=dict(height_ratios=[1.35, 1, 1], hspace=0.42))
    fig.subplots_adjust(left=0.085, right=0.985, top=0.95, bottom=0.075)
    a, b, c = axes
    similarity_panel(a, th, f"a · Frame–query similarity for “{rec['query']}” "
                     "(grey: raw per frame, blue: smoothed)")

    # b: boundary evidence
    b.axvspan(b0, b1, color=th["s2"], alpha=0.10, lw=0, zorder=0)
    b.plot(t, grad, color=th["ink2"], lw=0.9, zorder=1)
    for level, name in ((PARAMS["theta_high"], "θ_high"), (theta_low, "θ_low")):
        b.axhline(level, color=th["s1"], lw=1.0, alpha=0.8, zorder=2)
        b.text(0.15, level, f"{name} = {level:g}", va="bottom", ha="left", fontsize=8,
               color=th["ink2"], zorder=2.5,
               bbox=dict(boxstyle="square,pad=0.15", fc=th["surface"], ec="none"))
    starts = np.array([s for s, _ in segments])
    ends = np.array([e for _, e in segments])
    b.scatter(starts / fps, grad[starts], marker="^", s=38, color=th["s3"], edgecolors=th["surface"],
              linewidths=1.2, zorder=3, label="start boundary")
    b.scatter(ends / fps, grad[ends], marker="v", s=38, color=th["s2"], edgecolors=th["surface"],
              linewidths=1.2, zorder=3, label="end boundary")
    b.set_ylabel("hybrid gradient")
    style_axes(b, th)
    b.set_title(f"b · Boundary evidence (hybrid gradient) → {len(segments)} elementary segments",
                loc="left", fontsize=11, color=th["ink"], pad=8)
    leg = b.legend(loc="lower right", bbox_to_anchor=(1.0, 1.0), fontsize=8.5, frameon=False,
                   ncol=2, borderaxespad=0.2, handletextpad=0.3)
    for txt in leg.get_texts():
        txt.set_color(th["ink2"])

    # c: candidates by score (emphasis: best in accent, rest de-emphasised)
    c.axvspan(b0, b1, color=th["s2"], alpha=0.10, lw=0, zorder=0)
    for s, e, sc in scored:
        if (s, e) != (best[0], best[1]):
            c.hlines(sc, s / fps, e / fps, color=th["deemph"], lw=2.2, zorder=1)
    c.hlines(best[2], b0, b1, color=th["s1"], lw=3.2, zorder=3)
    c.scatter([b0, b1], [best[2]] * 2, s=40, color=th["s1"], edgecolors=th["surface"],
              linewidths=1.5, zorder=4)
    c.annotate(f"selected: score {best[2]:.3f}", (b1, best[2]), xytext=(8, 0),
               textcoords="offset points", va="center", fontsize=9, color=th["ink"])
    c.set_ylabel("segment score")
    c.set_xlabel("time (s)")
    style_axes(c, th)
    c.set_title(f"c · {len(candidates)} gap-merged candidates scored by inside/outside contrast",
                loc="left", fontsize=11, color=th["ink"], pad=8)
    c.set_xlim(0, t[-1])
    return fig


def draw_observation(th):
    fig, ax = plt.subplots(figsize=(9, 3.5))
    fig.subplots_adjust(left=0.085, right=0.985, top=0.80, bottom=0.16)
    similarity_panel(ax, th, "")
    ax.set_xlabel("time (s)")
    ax.set_xlim(0, t[-1])
    fig.text(0.085, 0.935, "Frame–query similarity rises inside the described moment",
             fontsize=12, color=th["ink"], ha="left")
    fig.text(0.085, 0.865, f"DiDeMo example bundled with the code · query “{rec['query']}” · "
             "grey: raw CLIP similarity per frame, blue: smoothed", fontsize=9, color=th["ink2"], ha="left")
    return fig


if __name__ == "__main__":
    os.makedirs(ASSETS, exist_ok=True)
    print(render_both(draw_hero, os.path.join(ASSETS, "hero"), dpi=170))
    print(render_both(draw_observation, os.path.join(ASSETS, "observation"), dpi=170))
