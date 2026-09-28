<sub>[🏠 Portfolio](https://github.com/heoneyzi) › [📄 Paper](../../README.md) › [FTF-VTG](../README.md) › **Results**</sub>

# 📊 FTF-VTG · reported results

> **Question —** how does a frame-level, training-free pipeline compare with heavier training-free baselines on accuracy and GPU memory, and how sensitive is it to its boundary threshold?

| | |
|---|---|
| **Status** | ✅ reported (2025, IEIE paper result notes) — transcribed here, not re-run |
| **Model / data** | CLIP ViT-B/32 frame–query similarities · DiDeMo (moment grounding and moment retrieval) · VidSTG (temporal grounding) |
| **Compute** | GPU memory recorded with `nvidia-smi` (values below) |
| **Headline** | DiDeMo R@1 (IoU ≥ 0.5) **19.30** · VidSTG mIoU **39.01** · **788 MiB** |

## Setup

- **Tasks.** *Temporal grounding (VTG)* — predict one span per query; report R@1 at IoU ≥ 0.5 (DiDeMo) and mean IoU (VidSTG). *Moment retrieval (VMR)* on DiDeMo — rank DiDeMo's 21 candidate moments (contiguous runs of its six 5-second bins) by IoU with the predicted span; report R@1.
- **Baselines** (training-free): an off-the-shelf pipeline (CLIP + PySceneDetect shot detection + watershed; Diwan et al., 2022) and TFVTG (Zheng et al., ECCV 2024) run **without its LLM stage** (BLIP-2 + sliding-window proposals). TA-STVG, a trained spatio-temporal grounding model, is listed as a reference point only.
- The evaluation adapters in [`../code/ftf_vtg/evaluation.py`](../code/ftf_vtg/evaluation.py) implement these protocols with the historical endpoint conventions; they are not official benchmark evaluators.

## Results

| Method | Training | DiDeMo R@1 (IoU ≥ 0.5) | VidSTG mIoU | GPU memory (MiB) |
|---|---|---:|---:|---:|
| Off-the-shelf | training-free | 13.31 | 24.22 | 1,300 |
| TFVTG without LLM stage | training-free | 15.56 | 24.94 | 9,537 |
| **FTF-VTG** | **training-free** | **19.30** | **39.01** | **788** |
| TA-STVG (reference) | trained | — | 51.01 | 29,035 |

File: [`reported_results.csv`](reported_results.csv). Differences for FTF-VTG: +3.74 / +5.99 points R@1 on DiDeMo and +14.07 / +14.79 points mIoU on VidSTG over TFVTG (no LLM) / off-the-shelf, with about 12× less GPU memory than the TFVTG row.

**Memory detail (FTF-VTG, CLIP ViT-B/32).** 788.00 MiB without batching; 828.00 (batch 16), 884.67 (32), 1,027.23 (64), 1,362 (128), 3,986.00 (1024) and 6,295.43 MiB (2048). Other readings in the notes for BLIP-2/TFVTG (15,351 MiB at batch 64; "12.2G") were taken under different settings and are not used in the table.

**Moment retrieval (DiDeMo VMR).** R@1 **36.90**, next to an upper bound of 74.75 listed in the same table. The notes place it beside fine-tuned video-retrieval models (ClipBERT, Frozen, TMVM, CLIP4Clip) that appear to be evaluated under a different protocol, so no ranking is claimed here.

### Hyper-parameter sweeps

VidSTG mIoU as a function of the boundary threshold θ_high (λ = 0.9, α = 0.05) — [`vidstg_theta_sweep.csv`](vidstg_theta_sweep.csv):

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/theta_sensitivity_dark.png">
  <img src="../assets/theta_sensitivity.png" width="520" alt="VidSTG mIoU against theta_high: 0.36 at zero, a plateau between 38.4 and 39.04 from 0.0005 to 0.0025, then a decline to 8.16 at 0.01.">
</picture>
</p>

- Plateau: mIoU ≥ 38.41 for θ_high ∈ [0.0005, 0.0025], peak 39.04 at 0.0015. With θ_high = 0 every sample becomes an edge and mIoU collapses to 0.36; above 0.003 fewer boundaries survive and mIoU falls to 8.16 at 0.01.
- λ and α — [`vidstg_lambda_alpha_sweep.csv`](vidstg_lambda_alpha_sweep.csv): at θ_high = 0.0015, λ ∈ [0.1, 0.5] gives 39.01 (38.81 at λ = 0); α ∈ {0, 0.05, 0.1, 0.2} gives 38.88–39.02. The score is flat in λ and α compared with θ_high.

## Takeaway

- A single frozen image–text model plus 1-D post-processing is competitive with, and on these two datasets ahead of, heavier training-free pipelines, at a fraction of their GPU memory.
- The method is not a replacement for trained grounding models (TA-STVG: 51.01 mIoU on VidSTG).
- The θ_high curve shows a broad plateau, but it was measured on the same data as the reported score; treat 39.01 as a tuned-on-evaluation number until it is re-run with a validation split.

## Files

| File | What it is |
|---|---|
| [`reported_results.csv`](reported_results.csv) | Main comparison (method, training, backbone, proposal strategy, DiDeMo R@1, VidSTG mIoU, GPU MiB) |
| [`vidstg_theta_sweep.csv`](vidstg_theta_sweep.csv) | 22-point θ_high sweep on VidSTG (λ 0.9, α 0.05) |
| [`vidstg_lambda_alpha_sweep.csv`](vidstg_lambda_alpha_sweep.csv) | λ sweeps at θ_high 0.0015 and 0.003, α sweep at 0.0015. One λ = 0.8 cell written as "3788" in the notes is left out; the α sweep's λ value is not recorded |

<sub>Provenance: all numbers are copied from the result tables in the team's Notion paper notes (2025); the manuscript draft itself is not published here.</sub>
